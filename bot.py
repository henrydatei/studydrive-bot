from studydriveapi import *
from functions import *

# master
try:
    file = open("main-account.txt")
    loginData = file.read()
    mainUsername = loginData.split(":")[0]
    mainPassword = loginData.split(":")[1]
except:
    print("main-account.txt not found")
    print("I'll create the file main-account.txt with your credentials.")
    file = open("main-account.txt", "w+")
    mainUsername = input('Username: ')
    mainPassword = input('Password: ')
    file.write(str(mainUsername) + ":" + str(mainPassword))
finally:
    file.close()

token = login(mainUsername, mainPassword)
#print token

myself = getMyself(token)
myselfJSON = json.loads(makeReadyForJSON(myself))
masterID = myselfJSON["userid"]
masterName = str(myselfJSON["first_name"]) + " " + str(myselfJSON["last_name"])

print("Crawl for information")
crawlForInformation(token, masterID, masterName)

# alts
file = open("alts.txt")
alts = file.read().splitlines()
file.close()
randomAlt = random.randint(0,len(alts)-1)
username = alts[randomAlt].split(":")[0]
password = alts[randomAlt].split(":")[1]
folderName = username.split("@")[0]
print("Use alt: " + str(username))
try:
    tokenAlt = login(username, password)

    # download documents
    added = getAdditionsFromFiles(folderName + "/downloadedDocuments.txt", "documents.txt")
    print('not downloaded documents:')
    for line in added:
        print(line)
    #select 2 un-downloaded documents to download
    if len(added) >= 2:
        choice = random.sample(added, 2)
        #download the documents
        print("Downloading documents:")
        f = open(folderName + "/downloadedDocuments.txt", "a+")
        for docID in choice:
            print(docID)
            document = getDocument(docID, tokenAlt)
            f.write(str(docID) + "\n")
        f.close()

    # upvote Documents
    added = getAdditionsFromFiles(folderName + "/upvotedDocuments.txt", "documents.txt")
    print('not upvoted documents:')
    for line in added:
        print(line)
    #select 4 un-upvoted documents to upvote
    if len(added) >= 4:
        choice = random.sample(added, 4)
        #upvote the documents
        print("Upvoting documents:")
        f = open(folderName + "/upvotedDocuments.txt", "a+")
        for docID in choice:
            print(docID)
            document = upvoteDocument(tokenAlt, docID)
            f.write(str(docID) + "\n")
        f.close()

    # upvote and play Flashcards
    added = getAdditionsFromFiles(folderName + "/upvotedFlashcards.txt", "flashcards.txt")
    print('not upvoted and played flashcards:')
    for line in added:
        print(line)
    #select 2 un-upvoted flashcards to upvote
    if len(added) >= 2:
        choice = random.sample(added, 2)
        #upvote the flashcards
        print("Upvoting and playing flashcards:")
        f = open(folderName + "/upvotedFlashcards.txt", "a+")
        for flashcardID in choice:
            print(flashcardID)
            flashcard = upvoteFlashcard(tokenAlt, flashcardID)
            f.write(str(flashcardID) + "\n")

            # play flashcard
            startFlashcard(tokenAlt,flashcardID)
            finishFlashcard(tokenAlt,flashcardID)
        f.close()

    # upvote Questions
    added = getAdditionsFromFiles(folderName + "/upvotedQuestions.txt", "questions.txt")
    print('not upvoted questions:')
    for line in added:
        print(line)
    #select 2 un-upvoted answers to upvote
    if len(added) >= 2:
        choice = random.sample(added, 2)
        #upvote the answers
        print("Upvoting questions:")
        f = open(folderName + "/upvotedQuestions.txt", "a+")
        for toUpvote in choice:
            print(toUpvote)
            type = toUpvote.split("|")[0]
            id = toUpvote.split("|")[1]
            answer = upvoteQuestion(tokenAlt, type, id)
            f.write(str(toUpvote) + "\n")
        f.close()

    # upvote Answers
    added = getAdditionsFromFiles(folderName + "/upvotedAnswers.txt", "answers.txt")
    print('not upvoted answers:')
    for line in added:
        print(line)
    #select 4 un-upvoted answers to upvote
    if len(added) >= 4:
        choice = random.sample(added, 4)
        #upvote the answers
        print("Upvoting answers:")
        f = open(folderName + "/upvotedAnswers.txt", "a+")
        for toUpvote in choice:
            print(toUpvote)
            type = toUpvote.split("|")[0]
            id = toUpvote.split("|")[1]
            answer = upvoteAnswer(tokenAlt, type, id)
            f.write(str(toUpvote) + "\n")
        f.close()
except Exception as e:
    pass
