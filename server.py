import os
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response, jsonify
from treehouse import TreeSQL, TreeJSON

app = Flask(__name__)

HOST = '127.0.0.1'

loggedIn = False
username = ''
email = ''
familyName = ''
database = TreeSQL()
database.connect()

@app.route('/')
def controlpanel():
	# database connection
	if loggedIn == False:
		return redirect(url_for('login'))
	else:
		fams = database.select_families_for_account(email)
		return render_template('controlpanel.html', name=username, families = fams)

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		global email
		email = request.form['email']
		password = request.form['pwd']
		response = database.select_account(email, password)
		if(response != False):
			global loggedIn
			loggedIn = True
			global username
			username = response
			return redirect(url_for('controlpanel'))
		else:
			print("Username and password do not match")
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		repassword = request.form['repassword']
		if(password == repassword):
			database.insert_account(email, username, password)
			print("registered")
		else:
			print("error: retry password")
		return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
	print("Logout")
	global loggedIn
	loggedIn = False
	return json.dumps(loggedIn)

@app.route('/<family>')
def tree(family):
	members = []
	memNames = []
	familyGraph = ""
	if(family != 'favicon.ico'):
		global familyName
		familyName = database.get_family_name(email, family)
		members = database.select_family(familyName)
		for member in members:
			memNames.append(member.name)
		graphObj = TreeJSON(familyName)
		familyGraph = graphObj.get_JSON()

	return render_template('regions.html', family = family, members = memNames, familyGraph = familyGraph)


@app.route('/addTree', methods=['POST'])
def addTree():
	if request.method == 'POST':
		treeName = request.form['treeName']
		database.insert_treehouse(email, treeName)
		return redirect(url_for('controlpanel'))

@app.route('/removeTree', methods=['POST'])
def removeTree():
	if request.method == 'POST':
		treeName = request.form['treeName']
		print(treeName)
		database.delete_treehouse(email, treeName)
		return redirect(url_for('controlpanel'))

@app.route('/addMember', methods=['POST'])
def addMember():
	if request.method == 'POST':
		gender = request.form['gender']
		name = request.form['name']
		mother = request.form['mother']
		father = request.form['father']
		spouse = request.form['spouse']
		database.insert_person(familyName, name, gender)
		if(mother != 'None'):
			database.update_mother(familyName, name, mother)
		if(father != 'None'):
			database.update_father(familyName, name, father)
		if(spouse != 'None'):
			database.update_spouse(familyName, name, spouse)
		tree = TreeJSON(familyName)
		return json.dumps(tree.get_JSON())

@app.route('/editMember', methods=['POST'])
def editMember():
	if request.method == 'POST':
		name = request.form['editName']
		newName = request.form['newName']
		newGender = request.form['newGender']
		tree = TreeJSON(familyName)
		return json.dumps(tree.get_JSON())

@app.route('/removeMember', methods=['POST'])
def removeMember():
	if request.method == 'POST':
		name = request.form['deleteName']
		database.delete_person(familyName, name)
		tree = TreeJSON(familyName)
		return json.dumps(tree.get_JSON())

@app.route('/getMembers', methods=['POST'])
def getMembers():
	members = database.select_family(familyName)
	memNames = []
	for member in members:
		memNames.append(member.name)
	return json.dumps(memNames)

if __name__ == '__main__':
    app.run(debug=False, host=HOST, port = 8000)
