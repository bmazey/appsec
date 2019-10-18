from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    # serializable properties
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    # TODO - check the VARCHAR space on the phone number (64)
    phone = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # password hashing methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # string representation dunder
    def __repr__(self):
        return '<User {}>'.format(self.username)


# used to load user from database for login purposes
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
