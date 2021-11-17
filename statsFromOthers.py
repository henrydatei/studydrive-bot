import re
import requests
import json
from datetime import datetime

def getStats(userID):
    r = requests.get("https://www.studydrive.net/de/profile/sauron/{}#documents".format(userID))
    html = r.text
    result = re.search('sdWindow.profile = (.*);sdWindow.isTablet', html)
    return json.loads(result.group(1))

currentDate = datetime.now().strftime('%Y-%m-%d %H:%m:%S')

hauser = getStats("1835660")
tom = getStats("1325403")

print(currentDate + "," + str(hauser["name"]) + "," + str(hauser["karma"]) + "," + str(hauser["karma_ranking"]) + "," + str(hauser["credits"]))
print(currentDate + "," + str(tom["name"]) + "," + str(tom["karma"]) + "," + str(tom["karma_ranking"]) + "," + str(tom["credits"]))