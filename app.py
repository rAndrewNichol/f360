
from flask import Flask, jsonify, request, render_template, redirect
gui = Flask(__name__)
gui.config.from_object('config')

# @gui.route('/')
# def home():
# 	return render_template('homepage.html',
# 							title = "Home")
@gui.route('/')
# @gui.route('/home')
def test():
	return render_template('test.html')

@gui.route('/<team>')
def team1(team):
	#keep params somehow?
	return render_template(team + '.html')

if __name__ == "__main__":
	gui.run()