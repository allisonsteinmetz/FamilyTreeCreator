import os
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response
from treehouse import TreeSQL

app = Flask(__name__)

loggedIn = False
username = ''
database = TreeSQL()
database.connect()

@app.route('/')
def controlpanel():
	# database connection
	if loggedIn == False:
		return redirect(url_for('login'))
	else:
		return render_template('controlpanel.html', name=username)

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
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

@app.route('/tree')
def tree():
	return render_template('regions_modal_included.html')

if __name__ == '__main__':
    app.run(debug=False, port = 8000)
