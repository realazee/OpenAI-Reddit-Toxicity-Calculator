import webbrowser
import requests
import os
import json
import openai
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flask_login import *
import flask_login
from flaskext.mysql import MySQL
from oauth import *
import sys
import numpy as np
import bisect

mysql = MySQL()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "super secret key"
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
openai.api_key = secrets['secretKey']

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = secrets['sqlPassword']
app.config['MYSQL_DATABASE_DB'] = 'toxicitycalc'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()



#authentication stuff
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_token):
     user = User()
     user.id = user_token
     return user

class User(flask_login.UserMixin):
	pass

@app.route("/", methods=["GET", "POST"])
def redirToLogin():
    return redirect(url_for('loginHelper'))

@flask_login.login_required
@app.route("/home", methods=["GET", "POST"])
def homeHelper():
    return render_template("homepage.html")

#page doesnt exist yet. will be created later
@app.route("/login", methods=["GET", "POST"])
def loginHelper():
    #if login successful, run flask_login.login_user(user) and login the user
    #if login unsuccessful, redirect to login page
    
    return render_template("login.html")

@app.route("/redditAuth", methods=["GET", "POST"])
def redditHelper():
    username = request.form.get('username')
    password = request.form.get('password')

    token = reddit_login(username, password)
    if token == 'error':
         return render_template("login.html", error="didn't work")

    user = User()
    user.id = token
    login_user(user)
    return render_template("homepage.html")

@app.route("/history", methods=["GET"])
def historyHelper():
    cursor.execute("SELECT username from searchedUsers")
    searchedUsers = cursor.fetchall()
    return render_template("history.html", searchedUsers=searchedUsers)

@app.route("/oauth", methods=["POST"])
def oauthHelper():
    nameToCheck = request.form.get('nameToCheck')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO searchedUsers (userName) VALUES ('{0}') ON DUPLICATE KEY UPDATE username=username".format(nameToCheck))
    commentList = getUserComments(nameToCheck, current_user.id)

    response = openai.Moderation.create(input=str(commentList))
    output = response["results"][0]
    hate = str(output["category_scores"]["hate"])
    hate_threatening = str(output["category_scores"]["hate/threatening"])
    self_harm = str(output["category_scores"]["self-harm"])
    sexual = str(output["category_scores"]["sexual"])
    sexual_minors = str(output["category_scores"]["sexual/minors"])
    violence = str(output["category_scores"]["violence"])
    violence_graphic = str(output["category_scores"]["violence/graphic"])

    #code to take results from openAI and round to 6 decimal places for ease of usability
    hate_formatted = float("{:.3f}".format(float(hate)))
    hate_threatening_formatted = float("{:.3f}".format(float(hate_threatening)))
    self_harm_formatted = float("{:.3f}".format(float(self_harm)))
    sexual_formatted = float("{:.3f}".format(float(sexual)))
    sexual_minors_formatted = float("{:.3f}".format(float(sexual_minors)))
    violence_formatted = float("{:.3f}".format(float(violence)))
    violence_graphic_formatted = float("{:.3f}".format(float(violence_graphic)))

    # Define a list and add data field into it
    openAI_data = []
    openAI_data.append(hate_formatted)
    openAI_data.append(hate_threatening_formatted)
    openAI_data.append(self_harm_formatted)
    openAI_data.append(sexual_formatted)
    openAI_data.append(sexual_minors_formatted)
    openAI_data.append(violence_formatted)
    openAI_data.append(violence_graphic_formatted)

    #print("Hate Pre Format", hate)
    #print("Hate Formatted", hate_formatted)
    #print("Sexual Pre Format", sexual)
    #print("Sexual Formatted", sexual_formatted)

    # Define the intervals
    #intervals = [1e-6, 1.995e-6, 3.981e-6, 7.943e-6, 1.585e-5, 3.162e-5, 6.310e-5, 1.259e-4, 2.512e-4, 5.012e-4, 1e-3, 1.995e-3, 3.981e-3, 7.943e-3, 1.585e-2, 3.162e-2, 6.310e-2, 1.259e-1, 2.512e-1, 5.012e-1]
    intervals = np.linspace(0.01,1,20)
    openAI_data_interval_score = []

    # Use a for loop to loop through values in openAI_data and find which interval they fall under
    for index, value in enumerate(openAI_data):
         # Find the index of the interval that the value belongs to
        intervalVal = bisect.bisect_left(intervals, value)
        
        # The 100 data range of gauge diagram is split apart into 20 regions
        openAI_data_interval_score.append(intervalVal * 5)


    #return render_template("openAI.html", hate=hate, hate_threatening=hate_threatening, self_harm=self_harm, sexual=sexual, sexual_minors=sexual_minors, violence=violence, violence_graphic=violence_graphic)

    return render_template("results.html", hate=openAI_data_interval_score[0], hate_threatening=openAI_data_interval_score[1], self_harm=openAI_data_interval_score[2], sexual=openAI_data_interval_score[3], sexual_minors=openAI_data_interval_score[4], violence=openAI_data_interval_score[5], violence_graphic=openAI_data_interval_score[6])

    


if __name__ == "__main__":    
    app.debug = True
    app.run(port=5003)
    webbrowser.open_new("127.0.0.1:5003")

    