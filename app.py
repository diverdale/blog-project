from src import app, db
from sqlalchemy.orm import relationship, backref
from src.models import Post, User
from flask import render_template, url_for, current_app
from _sqlite3 import OperationalError


@app.route('/')
@app.route('/index/<int:page>')
def index(page=1):

    posts = db.session.query(Post, User).outerjoin(Post, User.id == Post.post_author).filter_by()\
        .order_by(Post.post_date.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
    app.run(debug=True)
