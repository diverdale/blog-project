from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_user, login_required, logout_user
from src import app, db
from src.models import User
from src.users.forms import LoginForm, RegistrationForm

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates/users')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()

        if user.check_password(form.user_password.data) and user is not None:

            login_user(user)
            flash('Login Successful')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('blog.list')

            return redirect(next)
    return render_template('login.html', form=form)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(user_email=form.user_email.data,
                    user_username=form.user_username.data,
                    user_password=form.user_password.data,
                    user_role='User')
        if form.check_email(form.user_email.data):
            flash('Email already exists')

        elif form.check_username(form.user_username.data):
            flash('username exists')

        else:
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering!')

            return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))
