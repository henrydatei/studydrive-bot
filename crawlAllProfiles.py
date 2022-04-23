import re
import requests
import json
from datetime import datetime

baseurl = "https://api.studydrive.net/"

def getCredits(userID):
    r = requests.get("https://www.studydrive.net/de/profile/sauron/{}#documents".format(userID))
    html = r.text
    result = re.search('sdWindow.profile = (.*);sdWindow.isTablet', html)
    return json.loads(result.group(1))["credits"]

def login(user, passwd):
    param = {"client_id": 3,
             "client_secret": "s4lMeCEkNyZcztmpycUlAkSvzAq3gSNjGhGoToDV",
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

def produceOutput(i):
    print(i)
    try:
        stats = getStats(token, i)
        credits = getCredits(i)
        currentDate = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
        try:
            university = stats["studies"][0]["university"]["name"].replace('"', '')
        except:
            university = ""
        try:
            semester = stats["studies"][0]["semester"]["display_field"]
        except:
            semester = ""
        try:
            program = stats["studies"][0]["programs"][0]["name"].replace('"', '')
        except:
            program = ""
        return str(i) + "," + currentDate + "," + str(i) + ",\"" + str(stats["full_name"].replace('"', '')) + "\"," + str(stats["karma_points"]) + ",\"" + str(stats["karma_animal"]) + "\"," + str(credits) + ",\"" + str(stats["avatar_picture_large"]) + "\",\"" + str(stats["picture_large"]) + "\"," + str(int(stats["is_admin"])) + "," + str(stats["karma_rank"]) + "," + str(stats["total_uploads"]) + "," + str(stats["total_flashcard_sets"]) + "," + str(stats["total_downloads_generated"]) + "," + str(stats["total_upvotes"]) + "," + str(stats["total_posts"]) + "," + str(stats["total_answers"]) + "," + str(stats["total_best_answers"]) + "," + str(stats["followed_posts"]) + "," + str(stats["followed_files"]) + ",\"" + university + "\",\"" + semester + "\",\"" + program + "\",\"" + str(stats["share_link"]) + "\""
    except:
        return ""

import multiprocessing

cpus = multiprocessing.cpu_count()
p = multiprocessing.Pool(20)
token = login("email", "password")
# The below 2 lines populate the list. This listX will later be accessed parallely. This can be replaced as long as listX is passed on to the next step.
listX = range(3000000)
with open('output.csv', 'w') as f:
    for result in p.imap(produceOutput, listX):
        # (item, count) tuples from worker
        f.write(result + "\n")
