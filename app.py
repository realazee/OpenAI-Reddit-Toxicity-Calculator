import webbrowser
import requests
import os
import json
import openai
from flask import Flask, Response, request, render_template, redirect, url_for
from oauth import getUserComments

app = Flask(__name__, template_folder="templates", static_folder="static")
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
openai.api_key = secrets['secretKey']
print(openai.api_key)


@app.route("/", methods=["GET", "POST"])
def redirToLogin():
    return redirect(url_for('loginHelper'))

@app.route("/home", methods=["GET", "POST"])
def homeHelper():
    return render_template("homepage.html")


#page doesnt exist yet. will be created later
@app.route("/login", methods=["GET", "POST"])
def loginHelper():
    return render_template("login.html")

@app.route("/redditAuth", methods=["GET", "POST"])
def redditHelper():
    username = request.form.get('username')
    password = request.form.get('password')
    commentList = getUserComments(username, password, '')
    print(commentList)
    return render_template("homepage.html")

@app.route("/oauth", methods=["POST"])
def oauthHelper():
    nameToCheck = request.form.get('nameToCheck')
    redditUsername = secrets['redditUsername']
    redditPassword = secrets['redditPassword']
    commentList = getUserComments(redditUsername, redditPassword, nameToCheck)

    response = openai.Moderation.create(input=str(commentList))
    output = response["results"][0]
    hate = str(output["category_scores"]["hate"])
    hate_threatening = str(output["category_scores"]["hate/threatening"])
    self_harm = str(output["category_scores"]["self-harm"])
    sexual = str(output["category_scores"]["sexual"])
    sexual_minors = str(output["category_scores"]["sexual/minors"])
    violence = str(output["category_scores"]["violence"])
    violence_graphic = str(output["category_scores"]["violence/graphic"])
    print(output)
    return render_template("openAI.html", hate=hate, hate_threatening=hate_threatening, self_harm=self_harm, sexual=sexual, sexual_minors=sexual_minors, violence=violence, violence_graphic=violence_graphic)
    


if __name__ == "__main__":    
    app.debug = True
    app.run(port=5002)
    webbrowser.open_new("127.0.0.1:5002")

    
