import os
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response

app = Flask(__name__)

loggedIn = False
username = ''

@app.route('/')
def home():
	if loggedIn == False:
		return redirect(url_for('login'))
	else:
		return render_template('controlpanel.html', name=username)

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['pwd']
		print(email)
		print(password)
		# check email and password combo with database here!
		# if confirmed set loggedIn to true, retrieve username and redirect to home
		global loggedIn
		loggedIn = True
		global username
		username = 'allisonsteinmetz'
		#-----------
		return redirect(url_for('home'))
	else:
		return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False, port = 8000)
