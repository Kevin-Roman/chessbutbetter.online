import sqlite3

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[
                            DataRequired(), Length(min=1, max=20)])

    surname = StringField('Surname', validators=[
                          DataRequired(), Length(max=20)])

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=5, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        conn = sqlite3.connect('./accounts.db')
        curs = conn.cursor()

        curs.execute("SELECT * FROM Users WHERE username = (?);",
                     [username.data.lower()])

        user = curs.fetchone()

        conn.close()

        if user is not None:
            raise ValidationError(
                'That username is take. Please choose a different one.')

    def validate_email(self, email):
        conn = sqlite3.connect('./accounts.db')
        curs = conn.cursor()

        curs.execute("SELECT * FROM Users WHERE email = (?);",
                     [email.data.lower()])

        user = curs.fetchone()

        conn.close()

        if user is not None:
            raise ValidationError(
                'That email is take. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
