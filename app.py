import webbrowser
import requests
import os
import json
import openai
from flask import Flask, Response, request, render_template, redirect, url_for

app = Flask(__name__, template_folder="templates", static_folder="static")
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
openai.api_key = os.getenv(secrets['secretKey'])


@app.route("/", methods=["GET", "POST"])
def homeHelper():
    return render_template("homepage.html")


#page doesnt exist yet. will be created later
@app.route("/login", methods=["GET", "POST"])
def loginHelper():
    return render_template("template.html")

@app.route("/openAI", methods=["GET", "POST"])
def openAIHelper():
    openAIText = request.form.get('checkText')
    response = openai.Moderation.create(
    input=openAIText,
)
    return render_template("openAI.html")



if __name__ == "__main__":
    
    app.debug = True
    app.run(port=5002)
    webbrowser.open_new("127.0.0.1:5002")

    
