from studydriveapi import *
from functions import *

# master
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

# main
token = login(mainUsername, mainPassword)

# alts
file = open("alts.txt")
alts = file.read().splitlines()
file.close()

for alt in alts:
    username = alt.split(":")[0]
    password = alt.split(":")[1]
    tokenAlt = login(username,password)
    print "Alt: " + str(username)

    diff = getCourseDifference(token,tokenAlt)

    for courseID in diff:
        joinCourse(courseID,tokenAlt)
    sortCourses(tokenAlt)
