from flask_login import LoginManager

login = LoginManager()


def configure_authentication(app):
    # authentication
    login.init_app(app)
    login.login_view = 'pages.login'
