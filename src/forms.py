from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(), Length(min = 2, max = 26)])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Email()])
	submit = SubmitField('Registrar')

