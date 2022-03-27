import re
import requests
import json
from datetime import datetime
from tqdm import tqdm

def getStats(userID):
    r = requests.get("https://www.studydrive.net/de/profile/sauron/{}#documents".format(userID))
    html = r.text
    result = re.search('sdWindow.profile = (.*);sdWindow.isTablet', html)
    return json.loads(result.group(1))

for i in tqdm(range(10)):
    currentDate = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
    try:
        hauser = getStats(i)
        print(str(i) + "," + currentDate + "," + str(i) + ",\"" + str(hauser["name"]) + "\"," + str(hauser["karma"]) + ",\"" + str(hauser["karma_ranking"]) + "\"," + str(hauser["credits"]))
    except:
        pass