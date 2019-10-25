from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, SpellCheckForm
from models import User
from database import db
from subprocess import check_output
import os


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
    # if current_user.is_authenticated:
        # return redirect(url_for('pages.spellcheck'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, phone=form.phone.data)
        if User.query.filter_by(username=form.username.data).first() is not None:
            return render_template('register.html', title='Register', form=form, registration="failure")
        user.set_password(form.phone.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash('Congratulations, you are now a registered user!')
        # return redirect(url_for('pages.login'))
        # TODO - show failure element on failed registration?
        return render_template('register.html', title='Register', form=form, registration="success")
    return render_template('register.html', title='Register', form=form)


@pages.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
        # return redirect(url_for('pages.spellcheck'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.phone.data, form.password.data):
            # flash('Invalid username or password')
            # return redirect(url_for('pages.login'))
            # TODO - 2.factor custom failure code
            return render_template('login.html', title='Sign In', form=form, authenticated="Incorrect")
        login_user(user, remember=form.remember_me.data)
        # return redirect(url_for('pages.spellcheck'))
        return render_template('login.html', title='Sign In', form=form, authenticated="success")
    return render_template('login.html', title='Sign In', form=form)


@pages.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.index'))


@pages.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spellcheck():
    form = SpellCheckForm()
    if request.method == 'POST' and form.validate_on_submit():
        # create file to store user content
        file = open("input.txt", "w")
        file.write(form.content.data)
        file.close()

        # use subprocess to execute spell_check binary
        # windows implementation
        # cmd = ["wsl.exe", "/mnt/c/Users/Brandon/PycharmProjects/appsec/spell_check", "/mnt/c/Users/Brandon/PycharmProjects/appsec/input.txt", "/mnt/c/Users/Brandon/PycharmProjects/appsec/wordlist.txt"]

        # linux implementation
        cmd = ['./spell_check', 'input.txt', 'wordlist.txt']

        # convert result to csv, slice last two characters
        result = check_output(cmd).decode("utf-8").replace('\n', ', ')[:-2]

        # delete the file
        os.remove("input.txt")

        # clear text box
        original = form.content.data
        form.content.data = ""

        return render_template('spellcheck.html', title='Spell Check', form=form, input=original, output=result)
    else:
        return render_template('spellcheck.html', title='Spell Check', form=form)
