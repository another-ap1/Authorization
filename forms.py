from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    """form for users to register"""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])

class LoginForm(FlaskForm):
    """form for users to register"""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form for posting feedback"""
    title = StringField('Feedback Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """emtpy form for deleting feedback"""