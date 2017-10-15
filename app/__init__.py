from flask import Flask 

gui = Flask(__name__)
gui.config.from_object('config')

import views
