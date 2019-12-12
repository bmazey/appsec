import os
from get_docker_secret import get_docker_secret

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # secret key
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'wouldnt-you-like-to-know'
    SECRET_KEY = get_docker_secret('my_secret', default='oops very secret!')
    print('secret key: ' + str(SECRET_KEY))

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
