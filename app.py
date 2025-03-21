from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"User: {self.username}\nEmail: {self.email}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    posted_by = db.relationship('User')
    posted = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    reads = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    post = db.relationship('Post', backref='comments')
    content = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def increment_post_read(post):
    post.reads += 1
    db.session.commit()

@app.route('/')
def home():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts.html', posts=posts)


@app.route('/post/<int:post_id>')
def display_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        increment_post_read(post)
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
        return render_template('post.html', post=post, comments=comments)
    return "Post not found", 404


@app.route('/users')
def display_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/user/<int:user_id>')
def display_user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('user_profile.html', user=user) if user else ("User not found", 404)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(username='admin', email='admin@example.com', age=42)
            db.session.add(admin)

        if not User.query.filter_by(email='user@example.com').first():
            regular_user = User(username='user', email='user@example.com', age=20)
            db.session.add(regular_user)

        if not Post.query.filter_by(title="First Post").first():
            post1 = Post(user_id=1, posted=datetime.utcnow(), title="First Post", body="Welcome to the blog!")
            db.session.add(post1)

        if not Post.query.filter_by(title="Another Day").first():
            post2 = Post(user_id=1, posted=datetime.utcnow(), title="Another Day", body="This is the second blog post.")
            db.session.add(post2)

        if not Comment.query.filter_by(content="Great post!").first():
            comment1 = Comment(post_id=1, content="Great post!", author="John")
            db.session.add(comment1)

        if not Comment.query.filter_by(content="Very informative.").first():
            comment2 = Comment(post_id=1, content="Very informative.", author="Jane")
            db.session.add(comment2)

        db.session.commit()

    app.run(debug=True)

