import pytest
import app as main


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_login(app):
    res = app.get("/login")
    assert res.status_code == 200


def test_registration(app):
    res = app.get("/register")
    assert res.status_code == 200
