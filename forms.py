from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
