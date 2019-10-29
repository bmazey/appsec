import pytest
import app as main


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_login_page(app):
    res = app.get("/login")
    assert res.status_code == 200


def test_registration_page(app):
    res = app.get("/register")
    assert res.status_code == 200


def test_registration(app):
    username = "test_user"
    phone = "8675309"
    password = "top-secret-password"
    res = app.post("/register", data=dict(
        username=username,
        phone=phone,
        password=password
    ))
    print(res.data)
    assert res.status_code == 200


def test_login(app):
    username = "test_user"
    phone = "8675309"
    password = "top-secret-password"
    res = app.post("/login", data=dict(
        username=username,
        phone=phone,
        password=password
    ))
    assert res.status_code == 200
