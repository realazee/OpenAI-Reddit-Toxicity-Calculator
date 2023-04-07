import requests
import requests.auth
import json
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
redditId = secrets['redditId']
redditSecret = secrets['redditSecret']
client_auth = requests.auth.HTTPBasicAuth(redditId, redditSecret)
