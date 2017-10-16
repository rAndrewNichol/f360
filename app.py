
from flask import Flask, jsonify, request, render_template, redirect
gui = Flask(__name__)
gui.config.from_object('config')

@gui.route('/')
def home():
	return render_template('homepage.html',
							title = "Home")
@gui.route('/test')
def test():
	return render_template('test.html',title='ya')

if __name__ == "__main__":
	api.run()