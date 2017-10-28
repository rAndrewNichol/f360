from flask import Flask, jsonify, request, render_template, session, abort, redirect, url_for, Response
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#ADD TO HEROKU TODO
from datetime import datetime
from numpy import mean, std

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
			if username.strip() == user[1] and password.strip() == user[2]:
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
	to_week = {
		"10-26":"Project","10-27":"Project","10-28":"Project","10-29":"Project","10-30":"Project",
		"10-31":"Project","11-01":"Project",
		"11-02":"10-31","11-03":"10-31","11-04":"10-31","11-05":"10-31","11-06":"10-31",
		"11-07":"11-07","11-08":"11-07","11-09":"11-07","11-10":"11-07","11-11":"11-07","11-12":"11-07","11-13":"11-07",
		"11-14":"11-14","11-15":"11-14","11-16":"11-14","11-17":"11-14","11-18":"11-14","11-19":"11-14","11-20":"11-14",
		"11-21":"11-21","11-22":"11-21","11-23":"11-21","11-24":"11-21","11-25":"11-21","11-26":"11-21","11-27":"11-21",
		# "11-28":"11-28","11-29":"11-28","11-30":"11-28","12-01":"11-28","12-02":"11-28","12-03":"11-28","12-04":"11-28",
		# "12-05":"12-05","12-06":"12-05","12-07":"12-05","12-08":"12-05","12-09":"12-05","12-10":"12-05","12-11":"12-05",
		# "12-12":"12-12","12-13":"12-12","12-14":"12-12","12-15":"12-12","12-16":"12-12","12-17":"12-12","12-18":"12-12"
	}
	teams = {
		1:['devina darmawan','kevin van der eijk','austin vuong','adam dada','tanvi mongia','aneesha lugani'],
		2:['franklin rice','william sheng','fiona xie','dong eun suh','bryce king'],
		3:['judith syau','andrew nichol','dana wu','christofe survian','palak thakur'],
		4:['rhett gentile','ishan sharma','pouriya bagheri','pedro pablo correa hucke','manar safi'],
		5:['gwynevere hunger','faraz kahen','keith sollers','varun agarwal','anthony blair'],
		6:['siew hong ma','itzel romero','mingyang zhou','aayush patel','jenny liu'],
		8:['neha burli','nitin manivasagan','monica kumaran', 'yoonji lu','aneesh chimbili'],
		9:['sid iyer','alexander wing','anushree bhimani','arturo roman ordaz','bradford bruenell'],
		10:['amy philip','samantha cristol','vanessa salas','kyle geitner','jonathan archer','henry keenan']
	}

	def get_week(timestamp):
		date = timestamp.split()[0].split('-')[1:]
		hour = int(timestamp.split()[1].split(':')[0])
		if hour <= 7:
			date[1] = str(int(date[1]) - 1)
			if date[1] == '0':
				if date[0] == '11':
					date = ['10','31']
				elif date[0] == '12':
					date = ['11','30']
		date = "-".join(date)
		return to_week[date]

	def hundredize(rates):
		return (sum(rates[:7]) * float(2.5), {"strong":rates[7],"improve":rates[8]})

	def process(data, people):
		processed = {}
		persons_covered = set(people)
		scores = {}
		for person in persons_covered:
			scores[person] = {}
		for entry in data:
			submitter = entry[1].strip().lower()
			if submitter not in persons_covered:
				continue
			self_ratings = entry[5:14]
			mems = [entry[14:24], entry[24:35], entry[34:44], entry[44:54], entry[54:64]]
			scores[submitter]["self_rating"], scores[submitter]["self_qual"] = hundredize(self_ratings)
			for mem in mems:
				if not mem[0]:
					continue
				mem_name = mem[0].strip().lower()
				if mem_name not in teams[teamNumber]:
					#ignore it lol
					continue
				score, qual = hundredize(mem[1:])
				if "others_rating" not in scores[mem_name]:
					scores[mem_name]["others_rating"], scores[mem_name]["others_qual"] = (score,1), {"strong":[qual["strong"],],"improve":[qual["improve"],]}
				else:
					scores[mem_name]["others_rating"] = ((score + scores[mem_name]["others_rating"][0] * scores[mem_name]["others_rating"][1]) / 
														(scores[mem_name]["others_rating"][1] + 1),
															scores[mem_name]["others_rating"][1] + 1)
					scores[mem_name]["others_qual"]["strong"].append(qual["strong"])
					scores[mem_name]["others_qual"]["improve"].append(qual["improve"])

			persons_covered.remove(submitter)
			if not persons_covered:
				return scores

		return scores		

	teams = {
		1:['devina darmawan','kevin van der eijk','austin vuong','adam dada','tanvi mongia','aneesha lugani'],
		2:['franklin rice','william sheng','fiona xie','dong eun suh','bryce king'],
		3:['judith syau','andrew nichol','dana wu','christofe survian','palak thakur'],
		4:['rhett gentile','ishan sharma','pouriya bagheri','pedro pablo correa hucke','manar safi'],
		5:['gwynevere hunger','faraz kahen','keith sollers','varun agarwal','anthony blair'],
		6:['siew hong ma','itzel romero','mingyang zhou','aayush patel','jenny liu'],
		8:['neha burli','nitin manivasagan','monica kumaran', 'yoonji lu','aneesh chimbili'],
		9:['sid iyer','alexander wing','anushree bhimani','arturo roman ordaz','bradford bruenell'],
		10:['amy philip','samantha cristol','vanessa salas','kyle geitner','jonathan archer','henry keenan']
	}

	team = team.lower()

	if team not in ['team1','team2','team3','team4','team5','team6','team8','team9','team10']:
		return redirect('/')

	try:
		teamNumber = int(team.replace('team',''))
	except:
		return render_template('/')

	current_week = request.args.get('week')
	if not current_week:
		current_week = '0';

	db = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',port='',user='bda0f11ccb424e',passwd='1e1bf253',db='heroku_55f2adb0c8d05ac')
	cur = db.cursor()
	cur.execute("""SELECT * FROM responses WHERE team = {};""".format(teamNumber))
	data = cur.fetchall()
	db.close()

	weeks = {}
	for line in data:
		week = get_week(line[64])
		if week in weeks:
			weeks[week].append(line)
		else:
			weeks[week] = [line,]

	all_weeks = ["Project","10-31","11-07","11-14","11-21"]
	weeks_found = [week for week in all_weeks if week in weeks.keys()]

	people = teams[teamNumber]

	scores = {}
	for each_week in weeks_found:
		scores[each_week] = process(sorted([line for line in weeks[each_week] if line[1].strip().lower() in people],reverse = True, 
											key = lambda x:datetime.strptime(x[64], '%Y-%m-%d %H:%M:%S')),people)

	names = [" ".join(name.split()[:-1]).title() for name in people]
	overall = {person:[0,0] for person in people}
	for week in weeks_found:
		for person in people:
			if person in scores[week] and 'others_rating' in scores[week][person]:
				overall[person][0] += scores[week][person]['others_rating'][0] * scores[week][person]['others_rating'][1]
				overall[person][1] += scores[week][person]['others_rating'][1]

	overall_scores = []
	for person in people:
		if not overall[person][1]:
			overall_scores.append(0)
		else:
			overall_scores.append(round(float(overall[person][0]) / overall[person][1],1))

	return render_template('team.html', weeks_found = weeks_found, current_week = current_week, names = names, 
							overall_scores=overall_scores, teamNumber=str(teamNumber), scores = scores, full_names=people)

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
