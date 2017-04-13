import os
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response
from treehouse import TreeSQL

app = Flask(__name__)

loggedIn = False
username = ''
email = ''
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
			if (database.select_account(email, password) == False):
				database.insert_account(email, username, password)
				print("registered")
			else:
				print("error: user already exists")
		else:
			print("error: retry password")
		return render_template('login.html')

@app.route('/<family>')
def tree(family):
	return render_template('regions_modal_included.html', familyName = family)

@app.route('/addTree', methods=['POST'])
def addTree():
	if request.method == 'POST':
		treeName = request.form['treeName']
		database.insert_treehouse(email, treeName)
		return redirect(url_for('controlpanel'))

if __name__ == '__main__':
    app.run(debug=False, port = 8000)
