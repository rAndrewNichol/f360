from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField
from wtforms.validators import DataRequired

class LoginForm(Form):
	company = StringField('Company:')
	person = StringField('Your Name:')

class otherForm(Form):
	titles_or_skills = RadioField('Title', choices =[('1', 'Titles'), ('2','Skills')])
