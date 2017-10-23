from flask import Flask, jsonify, request, render_template, session, abort, redirect, url_for, Response
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

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
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		for user in users:
			if username == user[1] and password == user[2]:
				login_user(User(user[0]))
				return redirect(request.args.get("next"))
		return abort(401)
	else:
		return Response('''
		<form action="" method="post">
			<p><input type=text name=username>
			<p><input type=password name=password>
			<p><input type=submit value=Login>
		</form>
		''')

@gui.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/login')

@gui.route('/None')
@gui.route('/')
@login_required
def home():
	return render_template('test.html')

@gui.errorhandler(401)
def page_not_found(e):
	return redirect('/login')

@gui.route('/<team>',methods=['GET'])
@login_required
def teams(team):
	# db = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',port='',user='bda0f11ccb424e',passwd='1e1bf253',db='heroku_55f2adb0c8d05ac')
	# cur = db.cursor()
	# cur.execute("SELECT * FROM responses;")
	# dat = cur.fetchall()
	# db.close()
	week = request.args.get('week')
	data = [[3, "Andrew Nichol",5,3],[3, "Palak Thakur",2,4]]
	people = ["Andrew","Palak","Cristofe","Judith","Dana"]
	return render_template(team + '.html', data=data, week = week, people = people)

if __name__ == "__main__":
	# gui.secret_key = os.urandom(12)
	gui.run()
