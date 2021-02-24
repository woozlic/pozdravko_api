from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from databaser import get_user
from flask_login import logout_user, login_user, current_user, login_required
from .forms import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user(username)

        if not user or not check_password_hash(user.password, password):
            flash('Неправильный логин и/или пароль')
            return redirect(url_for('auth.login'))
        login_user(user, True)
        return redirect(url_for('main.add_category'))
    else:
        flash('Заполните поля')


@auth.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    if current_user.is_anonymous:
        return render_template('login.html', form=form)
    else:
        return redirect(url_for('main.index'))

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
