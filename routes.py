from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, SpellCheckForm
from models import User
from database import db
import subprocess


pages = Blueprint('pages', __name__)


@pages.route('/')
@pages.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@pages.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.phone.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('pages.login'))
    return render_template('register.html', title='Register', form=form)


@pages.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.phone.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('pages.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('pages.index'))
    return render_template('login.html', title='Sign In', form=form)


@pages.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.index'))


@pages.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spellcheck():
    form = SpellCheckForm()
    if form.validate_on_submit():
        # strategy: create test file from user input, run spell_check binary, get console output, and delete temp file
        with open("input.txt", "w") as text_file:
            print(form.text.data, file=text_file)
