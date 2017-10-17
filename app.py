from flask import Flask, jsonify, request, render_template, redirect
import pymysql

gui = Flask(__name__)
gui.config.from_object('config')

# url = 'mysql://bda0f11ccb424e:1e1bf253@us-cdbr-iron-east-05.cleardb.net/heroku_55f2adb0c8d05ac?reconnect=true'

# @gui.route('/')
# def home():
# 	return render_template('homepage.html',
# 							title = "Home")

@gui.route('/')
# @gui.route('/home')
def test():
	return render_template('test.html')

@gui.route('/<team>',methods=['GET'])
def team1(team):
	# db = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',port='',user='bda0f11ccb424e',passwd='1e1bf253',db='heroku_55f2adb0c8d05ac')
	# cur = db.cursor()
	# cur.execute("SELECT * FROM responses;")
	# dat = cur.fetchall()
	# db.close()
	week = request.args.get('week')
	data = [[3, "Andrew Nichol",5,3],[1, "Will Sheng",2,4]]
	return render_template(team + '.html', data=data, week = week)

if __name__ == "__main__":
	gui.run()
