from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from security import login
import datetime


class User(UserMixin, db.Model):
    # serializable properties
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    # TODO - check the VARCHAR space on the phone number (64)
    phone = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    # assignment 3
    submissions = db.relationship('Submission', backref='author', lazy='dynamic')
    authentications = db.relationship('Authentication', backref='logger', lazy='dynamic')

    # password hashing methods
    def set_password(self, phone, password):
        self.password_hash = generate_password_hash(phone + password)

    def check_password(self, phone, password):
        return check_password_hash(self.password_hash, phone + password)

    # string representation dunder
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(140))
    result = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # string representation dunder
    def __repr__(self):
        return '<Submission {}>'.format(self.original)


class Authentication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    last_logout = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # string representation dunder
    def __repr__(self):
        return '<Authentication {}>'.format(self.last_login)


# used to load user from database for login purposes
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
