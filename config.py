import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # secret key
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'wouldnt-you-like-to-know'
    try:
        SECRET_KEY = open("/run/secrets/my_secret", "r").read().strip()
    except Exception:
        SECRET_KEY = 'wouldnt-you-like-to-know'

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
