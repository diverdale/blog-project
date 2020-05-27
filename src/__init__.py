import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_misaka import Misaka
from flask_moment import Moment

login_manager = LoginManager()

app = Flask(__name__)
moment = Moment(app)
Misaka(app)
Bootstrap(app)


app.config['SECRET_KEY'] = 'supersecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'blog.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'users.login'


from src.users.views import users_blueprint
from src.blog.views import post_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(post_blueprint, url_prefix='/blog')
