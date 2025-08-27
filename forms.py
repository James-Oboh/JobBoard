# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    is_employer = BooleanField('I am an employer')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class JobPostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    salary = StringField('Salary (Optional)')
    submit = SubmitField('Post Job')
    
class ApplicationForm(FlaskForm):
    resume = FileField('Resume (PDF only)', validators=[
        FileAllowed(['pdf'], 'PDF files only!'),
        DataRequired()
    ])
    cover_letter = TextAreaField('Cover Letter (Optional)')
    submit = SubmitField('Submit Application')