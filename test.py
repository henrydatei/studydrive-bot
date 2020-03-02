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

token = login(mainUsername, mainPassword)
#print token

myself = getMyself(token)
myselfJSON = json.loads(makeReadyForJSON(myself))
masterID = myselfJSON["userid"]
masterName = str(myselfJSON["first_name"]) + " " + str(myselfJSON["last_name"])

print "Crawl for information"
crawlForInformation(token, masterID, masterName)

# alts
try:
    file = open("alts.txt")
    alts = file.read().splitlines()
    file.close()
    username = alts[0].split(":")[0]
    password = alts[0].split(":")[1]
    folderName = username.split("@")[0]

    # documents
    added = getAdditionsFromFiles(folderName + "/downloadedDocuments.txt", "documents.txt")
    print 'not downloaded documents:'
    for line in added:
        print line
    #select 50% of un-downloaded documents to download
    length = len(added)
    choice = random.sample(added, int(round(length/2)))
    #download the documents
    tokenAlt = login(username, password)
    print "Downloading documents:"
    f = open(folderName + "/downloadedDocuments.txt", "a+")
    for docID in choice:
        print docID
        document = getDocument(docID, tokenAlt)
        f.write(str(docID) + "\n")
    f.close()

    # upvote Documents
    added = getAdditionsFromFiles(folderName + "/upvotedDocuments.txt", "documents.txt")
    print 'not upvoted documents:'
    for line in added:
        print line
    #select 50% of un-upvoted documents to upvote
    length = len(added)
    choice = random.sample(added, int(round(length/2)))
    #upvote the documents
    tokenAlt = login(username, password)
    print "Upvoting documents:"
    f = open(folderName + "/upvotedDocuments.txt", "a+")
    for docID in choice:
        print docID
        document = upvoteDocument(tokenAlt, docID)
        f.write(str(docID) + "\n")
    f.close()

    # upvote Questions
    # Currently searching for an API-method. Maybe /api/app/v1/questions/upvote ?

    # upvote Answers
    added = getAdditionsFromFiles(folderName + "/upvotedAnswers.txt", "answers.txt")
    print 'not upvoted answers:'
    for line in added:
        print line
    #select 50% of un-upvoted answers to upvote
    length = len(added)
    choice = random.sample(added, int(round(length/2)))
    #upvote the answers
    tokenAlt = login(username, password)
    print "Upvoting answers:"
    f = open(folderName + "/upvotedAnswers.txt", "a+")
    for toUpvote in choice:
        print toUpvote
        type = toUpvote.split("|")[0]
        id = toUpvote.split("|")[1]
        answer = upvoteAnswer(tokenAlt, type, id)
        f.write(str(toUpvote) + "\n")
    f.close()
except IOError:
    print "alts.txt not found"
    print "Please run add-alts.py to add alts"
