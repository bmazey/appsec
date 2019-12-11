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

    # let's make an admin
    admin = User(username='admin', phone='12345678901')

    # set passwords
    user1.set_password('8675309', 'wouldnt-you-like-to-know')
    user2.set_password('1111111', 'deep-state-secrets')
    admin.set_password('12345678901', 'Administrator@1')

    # add to db
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(admin)

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
    print(res)

    content = "Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta."
    res = app.post("/spell_check", data=dict(
        content=content
    ), follow_redirects=False)
    assert b'sogn, skyn, betta' in res.data
    assert res.status_code == 200


def test_cors_headers(app):
    res = app.options("/login")
    print(res)


def test_admin_login(app, init_database):
    username = "admin"
    phone = "12345678901"
    password = "Administrator@1"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'success' in res.data
    assert res.status_code == 200
    return


def test_user_history_query(app, init_database):
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
    print(res)

    content = "Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta."
    res = app.post("/spell_check", data=dict(
        content=content
    ), follow_redirects=False)
    assert b'sogn, skyn, betta' in res.data
    assert res.status_code == 200

    res = app.get("/history")
    assert b'Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta.' in res.data
    return


def test_admin_history_query(app, init_database):
    # create content
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
    print(res)

    content = "Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta."
    res = app.post("/spell_check", data=dict(
        content=content
    ), follow_redirects=False)
    assert b'sogn, skyn, betta' in res.data
    assert res.status_code == 200

    # log in admin
    username = "admin"
    phone = "12345678901"
    password = "Administrator@1"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'success' in res.data
    assert res.status_code == 200

    # query user
    res = app.get("/history/query1")
    assert b'Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta.' in res.data
    return

def test_unauthorized_view(app, init_database):
    # create content
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
    print(res)

    content = "Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta."
    res = app.post("/spell_check", data=dict(
        content=content
    ), follow_redirects=False)
    assert b'sogn, skyn, betta' in res.data
    assert res.status_code == 200

    # log in second user
    username = "test2_user"
    phone = "1111111"
    password = "deep-state-secrets"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ), follow_redirects=False)
    assert b'success' in res.data
    assert res.status_code == 200

    # query user
    res = app.get("/history/query1")
    assert b'Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta.' not in res.data
    return
