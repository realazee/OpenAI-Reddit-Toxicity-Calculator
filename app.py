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

mysql = MySQL()
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "super secret key"
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
openai.api_key = secrets['secretKey']

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

@app.route("/oauth", methods=["POST"])
def oauthHelper():
    nameToCheck = request.form.get('nameToCheck')
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
    return render_template("openAI.html", hate=hate, hate_threatening=hate_threatening, self_harm=self_harm, sexual=sexual, sexual_minors=sexual_minors, violence=violence, violence_graphic=violence_graphic)
    


if __name__ == "__main__":    
    app.debug = True
    app.run(port=5003)
    webbrowser.open_new("127.0.0.1:5003")

    