from flask import Flask, jsonify, request, render_template, session, abort, redirect, url_for, Response
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from numpy import std, arange, mean
from pytz import timezone, utc

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

users = [(1,'mudit','fuckinglit'),(2,'thomas','tankengine'),
		(3,'stephen','bestdamnclass')]

@login_manager.user_loader
def load_user(user_id):
	return User(user_id)
 
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
	current_week = request.args.get('week')
	if not current_week:
		current_week = '0';
	return render_template('home.html',current_week=current_week)

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
			date[1] = "{0:0>2}".format(int(date[1]) - 1)
			if date[1] == '00':
				if date[0] == '11':
					date = ['10','31']
				elif date[0] == '12':
					date = ['11','30']
		date = "-".join(date)
		try: 
			return to_week[date]
		except:
			return None

	def hundredize(rates):
		if len(filter(None,rates)) == len(rates):
			return (sum(rates[:7]) * float(2.5), {"strong":rates[7].decode('utf-8','ignore'),"improve":rates[8].decode('utf-8','ignore')})
		else:
			return (None, None)

	def process(data, people):
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
					continue
				score, qual = hundredize(mem[1:])
				if not score:
					continue
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
		if not week:
			continue
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

	names = []
	for name in people:
		if name == 'kevin van der eijk':
			names.append("Kevin")
		elif name == 'pedro pablo correa hucke':
			names.append("Pablo")
		else:
			names.append(" ".join(name.split()[:-1]).title())


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
	print teamNumber
	return render_template('team.html', weeks_found = weeks_found, current_week = current_week, names = names, 
							overall_scores=overall_scores, teamNumber=str(teamNumber), scores = scores, 
							full_names=people, num_people = len(people))

@gui.route('/grades')
@login_required
def grades():
	now = datetime.now(tz=timezone('US/Pacific')).replace(tzinfo=None)
	# print now
	to_due = {"Project":datetime.strptime("2017-11-02 00:00:00","%Y-%m-%d %H:%M:%S"),
				"10-31":datetime.strptime("2017-11-07 00:00:00","%Y-%m-%d %H:%M:%S"),
				"11-07":datetime.strptime("2017-11-14 00:00:00","%Y-%m-%d %H:%M:%S"),
				"11-14":datetime.strptime("2017-11-21 00:00:00","%Y-%m-%d %H:%M:%S"),
				"11-21":datetime.strptime("2017-11-28 00:00:00","%Y-%m-%d %H:%M:%S"),}
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
			date[1] = "{0:0>2}".format(int(date[1]) - 1)
			if date[1] == '00':
				if date[0] == '11':
					date = ['10','31']
				elif date[0] == '12':
					date = ['11','30']
		date = "-".join(date)
		try:
			return to_week[date]
		except:
			return None

	def hundredize(rates):
		if len(filter(None,rates)) == len(rates):
			return (sum(rates[:7]) * float(2.5), {"strong":rates[7].decode('utf-8','ignore'),"improve":rates[8].decode('utf-8','ignore')})
		else:
			return (None, None)

	def process(data, people, week):
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
			scores[submitter]['scores_given'] = []
			scores[submitter]["self_rating"], scores[submitter]["self_qual"] = hundredize(self_ratings)
			for mem in mems:
				if not mem[0]:
					continue
				mem_name = mem[0].strip().lower()
				if mem_name not in people:
					continue
				score, qual = hundredize(mem[1:])
				if not score:
					continue
				scores[submitter]['scores_given'].append(score)
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

		for person in people:
			if person in persons_covered and now > to_due[week]:
				scores[person]['missed'] = 1
			else:
				scores[person]['missed'] = 0

		return scores	

	db = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',port='',user='bda0f11ccb424e',passwd='1e1bf253',db='heroku_55f2adb0c8d05ac')
	cur = db.cursor()
	alls = """SELECT * FROM responses;"""
	cur.execute(alls)
	data =  cur.fetchall() 
	alls = """SELECT * FROM previous;"""
	cur.execute(alls)
	previous_data = cur.fetchall()
	db.close()

	weeks = {}
	for line in data:
		week = get_week(line[64])
		if not week:
			continue
		if week in weeks:
			weeks[week].append(line)
		else:
			weeks[week] = [line,]

	all_weeks = ["Project","10-31","11-07","11-14","11-21"]
	weeks_found = [week for week in all_weeks if week in weeks.keys()]

	scores = {}
	for team in teams:
		scores[team] = {}
		for week in weeks_found:
			scores[team][week] = process(sorted([line for line in weeks[week] if line[1].strip().lower() in teams[team]],reverse = True, 
													key = lambda x:datetime.strptime(x[64], '%Y-%m-%d %H:%M:%S')),teams[team], week)

	previous_teams = {
	1:['william sheng','austin vuong','keith sollers','kevin van der eijk','andrew nichol'],
	2:['aneesh chimbili','bryce king','dong eun suh','fiona xie','mingyang zhou'],
	3:['alexander wing','anushree bhimani','christofe survian','judith syau','palak thakur'],
	4:['bradford bruenell','ishan sharma','pedro pablo correa hucke','pouriya bagheri','samantha cristol'],
	5:['aneesha lugani','anthony blair','gwynevere hunger','kyle geitner','rhett gentile'],
	6:['aayush patel','adam dada','devina darmawan','siew hong ma','manar safi'],
	7:['henry keenan','monica kumaran'],
	8:['amy philip','jenny liu','neha burli','nitin manivasagan','tanvi mongia'],
	9:['arturo roman ordaz','dana wu','franklin rice','sid iyer','yoonji lu'],
	10:['faraz kahen','itzel romero','jonathan archer','vanessa salas','varun agarwal']
	}

	previous_scores = {}
	for team in previous_teams:
		previous_scores[team] = process(sorted([line for line in previous_data if line[1].strip().lower() in previous_teams[team] and get_week(line[64])=="Project"],reverse = True, 
													key = lambda x:datetime.strptime(x[64], '%Y-%m-%d %H:%M:%S')),previous_teams[team], week = "Project")

	# print previous_scores

	overall = {}
	for team in previous_teams:
		for person in previous_teams[team]:
			overall[person] = [0,0,0,[]]
			if 'others_rating' in previous_scores[team][person]:
				overall[person][0] += previous_scores[team][person]['others_rating'][0] * previous_scores[team][person]['others_rating'][1]
				overall[person][1] += previous_scores[team][person]['others_rating'][1]
			if 'missed' in previous_scores[team][person]:
				overall[person][2] += previous_scores[team][person]['missed']
			if 'scores_given' in previous_scores[team][person]:
				overall[person][3].extend(previous_scores[team][person]['scores_given'])

	# print overall

	for team in teams:
		for week in scores[team]:
			for person in scores[team][week]:
				if 'others_rating' in scores[team][week][person]:
					overall[person][0] += scores[team][week][person]['others_rating'][0] * scores[team][week][person]['others_rating'][1]
					overall[person][1] += scores[team][week][person]['others_rating'][1]
				if 'missed' in scores[team][week][person]:
					overall[person][2] += scores[team][week][person]['missed']
				if 'scores_given' in scores[team][week][person]:
					overall[person][3].extend(scores[team][week][person]['scores_given']) 

	# print overall

	team_avgs = []
	for team in teams:
		team_sum = 0
		for person in teams[team]:
			if overall[person][3]:
				overall[person][3] = std(overall[person][3])
			else:
				overall[person][3] = 0
			if overall[person][1]:
				team_sum += overall[person][0] / float(overall[person][1])
				overall[person][1] = round(overall[person][0] / float(overall[person][1]),1)
		team_avgs.append(team_sum/float(len(teams[team])))

	team_sd = std(team_avgs)
	team_mean = mean(team_avgs)
	team_zs = [(each - team_mean)/team_sd for each in team_avgs]
	each_team_scale_factor = []
	for i in xrange(len(team_avgs)):
		if team_avgs[i] != 0:
			each_team_scale_factor.append((team_mean+(8*team_zs[i]))/team_avgs[i])
		else:
			each_team_scale_factor.append(1.0)

	for i in xrange(len(teams)):
		for person in teams[teams.keys()[i]]:
			overall[person][0] = overall[person][1] * each_team_scale_factor[i]


	class_avg = mean([team_mean + (8*z) for z in team_zs])
	class_sd = std([value[0] for (key,value) in overall.iteritems()])


	for person in overall:
		overall[person][0] = 85 + (8 * ( (overall[person][0] - class_avg )/class_sd ))

	sd_adjustments = [round(step - 4.6,1) for step in arange(0,9.4,.2)]

	sorted_by_sd = sorted(overall.keys(), key = lambda x: overall[x][3])
	for i in xrange(len(sorted_by_sd)):
		try:
			overall[sorted_by_sd[i]][0] += sd_adjustments[i]
		except:
			pass
		overall[sorted_by_sd[i]][0] -= 5 * overall[sorted_by_sd[i]][2]
		if overall[sorted_by_sd[i]][0] >= 100:
			overall[sorted_by_sd[i]][0] = 100
		overall[sorted_by_sd[i]][0] = round(overall[sorted_by_sd[i]][0],1)

	return render_template('grades.html', overall = overall)

if __name__ == "__main__":
	gui.run()
