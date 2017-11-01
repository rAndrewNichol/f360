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

alls = set()
for team in teams:
	for person in teams[team]:
		alls.add(person)
balls = set()
for team in previous_teams:
	for person in previous_teams[team]:
		balls.add(person)

print balls ^ alls
