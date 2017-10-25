from flask import Flask, jsonify, request, render_template, session, abort, redirect, url_for, Response
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

gui = Flask(__name__)
gui.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(gui)
login_manager.login_view = "login"

class User(UserMixin):

	def __init__(self, id):
		self.id = id
		self.data = {1:"Mudit",2:"Thomas",3:"Stephen"}
		self.name = self.data[int(self.id)]
		self.password = self.name + "_secret"

	def __repr__(self):
		return "%d/%s/%s" % (self.id, self.name, self.password)

users = [(1,'mudit','muditspassword'),(2,'thomas','thomasspassword'),
		(3,'stephen','stephenspassword')]

@login_manager.user_loader
def load_user(user_id):
	return User(user_id)

# url = 'mysql://bda0f11ccb424e:1e1bf253@us-cdbr-iron-east-05.cleardb.net/heroku_55f2adb0c8d05ac?reconnect=true'
# table creation : cursor.execute('create table responses(id int auto_increment primary key,dat VARCHAR(12),
#what int,start_time VARCHAR(20),end_time VARCHAR(20),net_id VARCHAR(12));')
 
@gui.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
			return redirect('/')
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		for user in users:
			if username == user[1] and password == user[2]:
				login_user(User(user[0]))
				# return redirect(request.args.get("next"))
				return redirect('/')
		return abort(401)
	else:
		return render_template('login.html')

@gui.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/login')

@gui.route('/')
@login_required
def home():
	return render_template('home.html')

@gui.errorhandler(401)
def page_not_found(e):
	return redirect('/login')

@gui.route('/<team>',methods=['GET'])
@login_required
def teams(team):
	team = team.lower()
	if team not in ['team1','team2','team3','team4','team5','team6','team8','team9','team10']:
		return redirect('/')
	#TODO: control for invalid index
	# db = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',port='',user='bda0f11ccb424e',passwd='1e1bf253',db='heroku_55f2adb0c8d05ac')
	# cur = db.cursor()
	# cur.execute("SELECT * FROM responses;")
	# dat = cur.fetchall()
	# db.close()
	week = request.args.get('week')
	if not week:
		week = '0';
	data = [[3, "Andrew Nichol",5,3],[3, "Palak Thakur",2,4]]
	people = ["Andrew","Palak","Cristofe","Judith","Dana"]
	student = 'Andrew'
	score = 57
	scores = [57,64,12,23,80]
	teamNumber = team.replace('team','')
	return render_template('team.html', data=data, week = week, people = people,student=student.title(), score = score,scores= scores, teamNumber=teamNumber)

# @gui.route('/<team>/<student>',methods=['GET'])
# @login_required
# def students(team,student):
# 	team = team.lower()
# 	if team not in ['team1','team2','team3','team4','team5','team6','team8','team9','team10']:
# 		return redirect('/')
# 	student = student.lower()
# 	if student not in ['devina','franklin','andrew','rhett','gwynevere','siew','neha','sid','amy','kevin',
# 						'william','judith','ishan','anthony','aayush','nitin','alex','sam','austin','fiona',
# 						'christofe','pouriya','varun','mingyang','monika','anushree','vanessa','adam','dong eung',
# 						'palak','pablo','faraz','jenny','yoonji','arturo','henry','tanvi','bryce','dana','manar',
# 						'keith','itzel','aneesh','brad','kyle','aneesha','jonathan']:
# 		return redirect('/')
# 	scores = [57,64,12,23,80,96]
# 	return render_template('student.html',student=student.title(), scores = scores)

@gui.route('/grades')
@login_required
def grades():
	return render_template('grades.html')
if __name__ == "__main__":
	gui.run()
