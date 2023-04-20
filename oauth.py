import requests
import requests.auth
import json
secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
redditId = secrets['redditId']
redditSecret = secrets['redditSecret']


#given redditUsername of the user who is logged in, redditPassword of the user who is logged in, 
#and searchedUser of the user whose comments we want to fetch, this function authenticates redditUsername 
#and returns an array of comments left by searchedUser.
def getUserComments(redditUsername, redditPassword, searchedUser):

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

    #this fetches the reddit comments left by searchedUser, filters it to 10 comments and stores it into userComments as a csv.
    userComments = requests.get('https://oauth.reddit.com/u/'+searchedUser+'/comments', headers=headers, params={'limit': '`10`'})
    commentResponse = userComments.json()
    #commentlist is an array of comments left by searchedUser, each element is one comment. This is ultimately what gets passed into openAI.
    #front end for this still needs to be done.
    commentList = [post['data']['body'] for post in commentResponse['data']['children']]

    return commentList
