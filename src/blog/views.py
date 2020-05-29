from flask import (Blueprint, render_template, redirect, url_for,
                   request, abort, flash, current_app)
from flask_login import login_required, current_user
from src import db
from src.models import Post, User
from src.blog.forms import AddForm, EditForm
import datetime

post_blueprint = Blueprint('blog', __name__,
                           template_folder='templates/blog')


@post_blueprint.route('/')
@post_blueprint.route('/blog/<int:page>')
def list(page=1):

    posts = Post.query.filter_by(post_author=current_user.id).order_by(Post.post_date.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('blog.list', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog.list', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('list_posts.html', posts=posts.items, next_url=next_url, prev_url=prev_url)


@post_blueprint.route('/<post_id>')
def details(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('details.html', post=post)


@post_blueprint.route('/add_post', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()

    if form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data
        post_author = current_user.id
        post_date = datetime.datetime.now()
        new_post = Post(post_title, post_content, post_author, post_date)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('blog.list'))
    return render_template('add_post.html', form=form)


@post_blueprint.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):

    post = Post.query.get_or_404(post_id)
    if post.post_author != current_user.id:
        abort(403)
    form = EditForm()

    if form.validate_on_submit():
        post.post_title = form.post_title.data
        post.post_content = form.post_content.data

        db.session.commit()

        return redirect(url_for('blog.details', post_id=post.id))
    elif request.method == 'GET':
        form.post_title.data = post.post_title
        form.post_content.data = post.post_content

    return render_template('edit_post.html', form=form)


@post_blueprint.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):

    post = Post.query.get_or_404(post_id)
    if post.post_author != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('blog.list'))


