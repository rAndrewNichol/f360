from app import gui
from flask import render_template, flash, redirect, request
from app.forms import *

# @gui.route('/login', methods=['GET', 'POST'])
# def login():
# 	name = ''
# 	form = LoginForm(request.form)
# 	stage = 1
# 	if request.method=='POST':
# 		person = request.form['person']
# 		company = request.form['company']
# 		name = person + " from " + company
# 		form = otherForm(request.form)
# 		stage = 2
#   		# return redirect('/')

# 	return render_template('login.html',
# 							title = 'Sign In',
# 							form = form,
# 							name = name,
# 							stage = stage)


@gui.route('/')
def home():
	return render_template('homepage.html',
							title = "Home")
@gui.route('/test')
def test():
	return render_template('test.html',title='PLEASEWORK')


# @gui.route('/index')
# def index():
# 	user = {'nickname': 'Miguel'}
# 	# fake array of posts
# 	posts = [
# 		{ 
# 			'author': {'nickname': 'John'}, 
# 			'body': 'Beautiful day in Portland!' 
# 		},
# 		{ 
# 			'author': {'nickname': 'Susan'}, 
# 			'body': 'The Avengers movie was so cool!' 
# 		}
# 	]
# 	return render_template('index.html',
# 							title='Home',
# 							user = user,
# 							posts = posts)




# <html>
# 	<head>
# 		<title>Home Page</title>
# 	</head>
# 	<body>
# 		<h1>Hello, ''' + user['nickname'] + '''</h1>
# 	</body>
# </html>
