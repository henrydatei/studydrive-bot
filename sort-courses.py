from studydriveapi import *

try:
    file = open("main-account.txt")
    loginData = file.read()
    mainUsername = loginData.split(":")[0]
    mainPassword = loginData.split(":")[1]
except IOError:
    print "main-account.txt not found"
    print "I'll create the file main-account.txt with your credentials."
    file = open("main-account.txt", "w+")
    mainUsername = raw_input('Username: ')
    mainPassword = raw_input('Password: ')
    file.write(str(mainUsername) + ":" + str(mainPassword))
finally:
    file.close()

token = login(mainUsername, mainPassword)

list = []
ids = []
courses = json.loads(makeReadyForJSON(getLeftSidebar(token)))
for courseData in courses['courses']:
    courseID = courseData['course_id']
    courseName = courseData['course_name']
    list.append([courseID,courseName])
#print str(list)
### sort
sortedList = sorted(list, key=lambda tup: tup[1])
#print str(sortedList)
for courseData in sortedList:
    id = courseData[0]
    ids.append(id)
#print str(ids)
print setCourseOrder(ids,token)
