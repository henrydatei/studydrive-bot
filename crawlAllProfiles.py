import re
import requests
import json
from datetime import datetime
from tqdm import tqdm

baseurl = "https://api.studydrive.net/"

def getCredits(userID):
    r = requests.get("https://www.studydrive.net/de/profile/sauron/{}#documents".format(userID))
    html = r.text
    result = re.search('sdWindow.profile = (.*);sdWindow.isTablet', html)
    return json.loads(result.group(1))["credits"]

def login(user, passwd):
    param = {"client_id": 4,
             "client_secret": "nmGaT4rJ3VVGQXu75ymi5Cu5bdqb3tFnkWw9f1IX",
             "grant_type":"password",
             "username": user,
             "password": passwd}
    req = requests.post('{}oauth/token'.format(baseurl), data=param)
    req.raise_for_status()
    return json.loads(req.text)['access_token']

def getStats(token, userID):
    headers={"authorization": "Bearer "+token}
    params = {"user_id": userID}
    req = requests.get('{}api/app/v1/profiles/{}'.format(baseurl, userID), headers = headers, params = params)
    req.raise_for_status()
    return req.json()

# for i in tqdm(range(10)):
#     currentDate = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
#     try:
#         hauser = getStats(i)
#         print(str(i) + "," + currentDate + "," + str(i) + ",\"" + str(hauser["name"]) + "\"," + str(hauser["karma"]) + ",\"" + str(hauser["karma_ranking"]) + "\"," + str(hauser["credits"]))
#     except:
#         pass

token = login("email", "password")
for i in tqdm(range(2820602)):
    try:
        stats = getStats(token, i)
        currentDate = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
        try:
            university = stats["studies"][0]["university"]["name"]
        except:
            university = ""
        try:
            semester = stats["studies"][0]["semester"]["display_field"]
        except:
            semester = ""
        try:
            program = stats["studies"][0]["programs"][0]["name"]
        except:
            program = ""
        print(str(i) + "," + currentDate + "," + str(i) + ",\"" + str(stats["full_name"]) + "\"," + str(stats["karma_points"]) + ",\"" + str(stats["karma_animal"]) + "\"," + str(getCredits(1325403)) + ",\"" + str(stats["avatar_picture_large"]) + "\",\"" + str(stats["picture_large"]) + "\"," + str(int(stats["is_admin"])) + "," + str(stats["karma_rank"]) + "," + str(stats["total_uploads"]) + "," + str(stats["total_flashcard_sets"]) + "," + str(stats["total_downloads_generated"]) + "," + str(stats["total_upvotes"]) + "," + str(stats["total_posts"]) + "," + str(stats["total_answers"]) + "," + str(stats["total_best_answers"]) + "," + str(stats["followed_posts"]) + "," + str(stats["followed_files"]) + ",\"" + university + "\",\"" + semester + "\",\"" + program + "\",\"" + str(stats["share_link"]) + "\"")
    except:
        pass