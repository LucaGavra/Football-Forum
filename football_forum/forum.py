from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, Team, Post, Comment, PostVote, CommentVote

forum = Blueprint('forum', __name__, url_prefix='/teams')

@forum.route('/')
def list_teams():
    """Show all available teams (subforums)."""
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)


@forum.route('/<int:team_id>')
def team_posts(team_id):
    """Display all posts under a specific team (subforum)."""
    team = Team.query.get_or_404(team_id)
    posts = Post.query.filter_by(team_id=team_id).order_by(Post.timestamp.desc()).all()
    return render_template('team_posts.html', team=team, posts=posts)


@forum.route('/<int:team_id>/post/new', methods=['GET', 'POST'])
@login_required
def new_post(team_id):
    """Create a new post within a specific team."""
    team = Team.query.get_or_404(team_id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('forum.new_post', team_id=team_id))

        post = Post(
            title=title,
            content=content,
            user_id=current_user.id,
            team_id=team.id
        )
        db.session.add(post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('forum.team_posts', team_id=team.id))

    return render_template('new_post.html', team=team)


@forum.route('/<int:team_id>/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(team_id, post_id):
    """
    View a single post within a specific team, and handle new comments.
    """
    team = Team.query.get_or_404(team_id)
    post = Post.query.get_or_404(post_id)

    # Verify the post is actually in this team
    if post.team_id != team.id:
        flash('This post does not belong to this team.', 'error')
        return redirect(url_for('forum.team_posts', team_id=team.id))

    # Handle new comment submission (POST)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must be logged in to comment.', 'error')
            return redirect(url_for('auth.login'))

        comment_content = request.form.get('comment_content')
        if not comment_content:
            flash('Comment cannot be empty.', 'error')
            return redirect(url_for('forum.post_detail', team_id=team.id, post_id=post.id))

        new_comment = Comment(
            content=comment_content,
            user_id=current_user.id,
            post_id=post.id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', 'success')

        return redirect(url_for('forum.post_detail', team_id=team.id, post_id=post.id))

    # GET: Render the post detail page
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.asc()).all()
    return render_template('post_detail.html', team=team, post=post, comments=comments)


@forum.route('/<int:team_id>/post/<int:post_id>/upvote', methods=['POST'])
@login_required
def upvote_post(team_id, post_id):
    """
    Handle upvoting a post. We set 'value=1' for an upvote.
    If you want to allow toggling or removing votes, add logic for that here.
    """
    post = Post.query.get_or_404(post_id)

    # Ensure the user hasn't already upvoted
    existing_vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if existing_vote:
        flash('You have already upvoted this post.', 'info')
        return redirect(url_for('forum.post_detail', team_id=team_id, post_id=post_id))

    vote = PostVote(
        value=1,  # Upvote
        user_id=current_user.id,
        post_id=post.id
    )
    db.session.add(vote)
    db.session.commit()

    flash('Post upvoted!', 'success')
    return redirect(url_for('forum.post_detail', team_id=team_id, post_id=post_id))


@forum.route('/<int:team_id>/post/<int:post_id>/comment/<int:comment_id>/upvote', methods=['POST'])
@login_required
def upvote_comment(team_id, post_id, comment_id):
    """
    Handle upvoting a comment. Set 'value=1' for an upvote.
    """
    comment = Comment.query.get_or_404(comment_id)

    # Make sure the comment belongs to this post, which belongs to the correct team
    if comment.post_id != post_id:
        flash('This comment does not belong to this post.', 'error')
        return redirect(url_for('forum.post_detail', team_id=team_id, post_id=post_id))

    # Check if the user already upvoted
    existing_vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    if existing_vote:
        flash('You have already upvoted this comment.', 'info')
        return redirect(url_for('forum.post_detail', team_id=team_id, post_id=post_id))

    vote = CommentVote(
        value=1,
        user_id=current_user.id,
        comment_id=comment.id
    )
    db.session.add(vote)
    db.session.commit()

    flash('Comment upvoted!', 'success')
    return redirect(url_for('forum.post_detail', team_id=team_id, post_id=post_id))

