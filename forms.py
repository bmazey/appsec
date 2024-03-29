from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', id="uname", validators=[DataRequired()])
    password = PasswordField('Password', id="pword", validators=[DataRequired()])
    phone = StringField('Phone', id="2fa", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', id="uname", validators=[DataRequired()])
    password = PasswordField('Password', id="pword", validators=[DataRequired()])
    phone = StringField('Phone', id="2fa", validators=[DataRequired()])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')
    #
    # def validate_phone(self, phone):
    #     user = User.query.filter_by(phone=phone.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different phone number.')


class SpellCheckForm(FlaskForm):
    content = StringField('Text', id="inputtext", validators=[DataRequired()])
    submit = SubmitField('Submit')


class HistoryForm(FlaskForm):
    content = StringField('Text', id="userquery", validators=[DataRequired()])
    submit = SubmitField('Submit')


class AuthenticationHistoryForm(FlaskForm):
    content = StringField('Text', id="userid", validators=[DataRequired()])
    submit = SubmitField('Submit')
