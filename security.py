from flask_login import LoginManager

login = LoginManager()


def configure_authentication(app):
    # authentication
    login = LoginManager(app)
    login.login_view = 'login'
