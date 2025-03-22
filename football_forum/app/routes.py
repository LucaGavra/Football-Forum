from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User, Discussion, Comment, Category
from . import db

@app.route('/')
def index():
    discussions = Discussion.query.order_by(Discussion.timestamp.desc()).all()
    return render_template('index.html', discussions=discussions)

@app.route('/discussion/<int:id>')
def discussion(id):
    discussion = Discussion.query.get_or_404(id)
    comments = Comment.query.filter_by(discussion_id=id).all()
    return render_template('discussion.html', discussion=discussion, comments=comments)

