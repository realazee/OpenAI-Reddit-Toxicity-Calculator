import flask
from flask import Flask, Response, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!