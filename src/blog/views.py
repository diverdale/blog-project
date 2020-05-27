from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from src import db
from src.models import Post, User
from src.blog.forms import AddForm
import datetime

post_blueprint = Blueprint('blog', __name__,
                           template_folder='templates/blog')


@post_blueprint.route('/')
def list():
    posts = Post.query.filter_by(post_author=current_user.id)
    return render_template('list_posts.html', posts=posts)


@post_blueprint.route('/<post_id>')
def details(post_id):
    post = Post.query.filter_by(id=post_id).first()
    print(post)
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
