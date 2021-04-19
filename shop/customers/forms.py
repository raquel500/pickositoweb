from wtforms import TextField, SubmitField,PasswordField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Passwords do not match ')])
    confirm= PasswordField('Confirm password: ', [validators.DataRequired()])
    telephone = StringField('Phone numer: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    eircode = StringField('Eircode/Post Code: ', [validators.DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username already exists")

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email already exists")


class CustomerLoginForm(FlaskForm):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])


