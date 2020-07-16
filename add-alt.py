import os.path
from os import path
import os

username = raw_input("Username: ")
password = raw_input("Password: ")

# check if first part of mail exists already to prevent problems with folders
folderName = username.split("@")[0]
if path.exists(folderName):
    print "Please use another username"
else:
    os.mkdir(folderName)
    f = open(folderName + "/downloadedDocuments.txt", "w+")
    f.close()
    f = open(folderName + "/upvotedDocuments.txt", "w+")
    f.close()
    f = open(folderName + "/upvotedAnswers.txt", "w+")
    f.close()
    f = open(folderName + "/upvotedQuestions.txt", "w+")
    f.close()
    f = open(folderName + "/upvotedFlashcards.txt", "w+")
    f.close()
    f = open("alts.txt", "a+")
    f.write(username + ":" + password + "\n")
    f.close()
