import requests
import requests.auth
import json
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
redditId = secrets['redditId']
redditSecret = secrets['redditSecret']

def getUserComments(redditUsername, redditPassword, searchedUser):

    # redditUsername = 'cs411testacc'
    # redditPassword = 'cs411Tester.'

    if searchedUser == '':
        searchedUser = redditUsername

    client_auth = requests.auth.HTTPBasicAuth(redditId, redditSecret)

    data = {
        'grant_type': 'password',
        'username': redditUsername,
        'password': redditPassword,
    }

    headers = {'User-Agent': 'cs411 reddit script'}

    
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=data, headers=headers)

    js = res.json()

    token = js['access_token']


    headers['Authorization'] = 'bearer {}'.format(token)
    me = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    print(me.json())


    userComments = requests.get('https://oauth.reddit.com/u/'+searchedUser+'/comments', headers=headers, params={'limit': '`10`'})
    commentResponse = userComments.json()

    commentList = [post['data']['body'] for post in commentResponse['data']['children']]

    return commentList
