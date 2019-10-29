import pytest
import app as main
from database import db
from models import User


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True

    # disabling CSRF protection for testing purposes
    app.config['WTF_CSRF_ENABLED'] = False

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client  # magic happens here

    ctx.pop()


@pytest.fixture
def init_database():
    # create db
    db.create_all()

    #  let's make two users
    user1 = User(username='test1_user', phone='8675309')
    user2 = User(username='test2_user', phone='1111111')

    # set passwords
    user1.set_password('8675309', 'wouldnt-you-like-to-know')
    user2.set_password('1111111', 'deep-state-secrets')

    # add to db
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # magic happens here

    db.drop_all()


def test_login_page(app):
    res = app.get("/login")
    assert res.status_code == 200


def test_registration_page(app):
    res = app.get("/register")
    assert res.status_code == 200


def test_valid_registration(app, init_database):
    username = "new_user"
    phone = "2222222"
    password = "super-complex-password"
    res = app.post("/register", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'success' in res.data
    assert res.status_code == 200


def test_invalid_registration(app, init_database):
    # this test fails because of a duplicate user
    username = "test1_user"
    phone = "8675309"
    password = "wouldnt-you-like-to-know"
    res = app.post("/register", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'failure' in res.data
    assert res.status_code == 200


def test_valid_login(app, init_database):
    # authenticate a registered user successfully
    username = "test1_user"
    phone = "8675309"
    password = "wouldnt-you-like-to-know"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'success' in res.data
    assert res.status_code == 200


def test_invalid_2fa_login(app, init_database):
    # correct username and password, but wrong 2fa device
    username = "test2_user"
    phone = "3333333"
    password = "deep-state-secrets"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'Incorrect' in res.data
    assert res.status_code == 200


def test_spellcheck_functionality(app, init_database):
    # authenticate a registered user successfully
    username = "test1_user"
    phone = "8675309"
    password = "wouldnt-you-like-to-know"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'success' in res.data
    assert res.status_code == 200

    content = "Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta."
    res = app.post("/spell_check", data=dict(
        content=content
    ), follow_redirects=False)
    print(res.data)
