from src import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(64), unique=True, index=True)
    user_username = db.Column(db.String(64), unique=True, index=True)
    user_posts = db.relationship('Post', cascade="all, delete-orphan", backref='author', lazy='dynamic')
    user_role = db.Column(db.String(10), index=True, default='User')
    password_hash = db.Column(db.String(128))

    def __init__(self, user_email, user_username, user_password, user_role):

        self.user_email = user_email
        self.user_username = user_username
        self.user_role = user_role
        self.password_hash = generate_password_hash(user_password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    post_author = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_title = db.Column(db.String(100))
    post_date = db.Column(db.DateTime)
    post_content = db.Column(db.Text)

    def __init__(self, post_title, post_content, post_author, post_date):
        self.post_title = post_title
        self.post_content = post_content
        self.post_author = post_author
        self.post_date = post_date

    def __repr__(self):
        return self.post_title



