from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(), Length(min = 2, max = 26)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(), Length(min = 2, max = 26)])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Email()])
	submit = SubmitField('Register')

