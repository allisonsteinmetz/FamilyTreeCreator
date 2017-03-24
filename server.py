import os
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response

app = Flask(__name__)

loggedIn = False

@app.route('/')
def home():
	if loggedIn == False:
		return redirect(url_for('login'))
	else:
		return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['pwd']
		print(username)
		print(password)
		# check username and password combo with database here!
		# if confirmed set loggedIn to true and redirect to home
		global loggedIn
		loggedIn = True
		return redirect(url_for('home'))
	else:
		return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False, port = 8000)
