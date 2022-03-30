import requests
import json
import os
from datetime import datetime
import unicodedata
import re

baseurl = "https://api.studydrive.net/"

def makeReadyForJSON(data):
    data = data.replace('\u00e4', 'ae')
    data = data.replace('\u00f6', 'oe')
    data = data.replace('\u00fc', 'ue')
    data = data.replace('\u00c4', 'Ae')
    data = data.replace('\u00d6', 'Oe')
    data = data.replace('\u00dc', 'Ue')
    data = data.replace('\u0308', 'e')
    data = data.replace('\u2019', '-')
    data = data.replace('\/', '/')
    return data

def login(user, passwd):
    param = {"client_id": 3,
             "client_secret": "s4lMeCEkNyZcztmpycUlAkSvzAq3gSNjGhGoToDV",
             "grant_type":"password",
             "username": user,
             "password": passwd}
    req = requests.post('{}oauth/token'.format(baseurl), data=param)
    req.raise_for_status()
    return json.loads(req.text)['access_token']

def getTime():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def getUniversityData(universityid, token): #returns all courses of the university
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/universities/{}/courses'.format(baseurl,universityid), headers=headers)
    req.raise_for_status()
    return json.loads(req.text)

def getCourseData(courseid, token, page=0, reference_time=None):
    #reference_time="2019-09-24 14:52:08"
    param = {"sort": "time",
            "page": page,
            "semester_from":0,
            "semester_until":0,
            "type_ids":0}
    if page>0:
        if reference_time is None:
            reference_time = getTime()
        param["reference_time"] = reference_time
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/feed/courses/{}/documents'.format(baseurl,courseid), params=param, headers=headers)
    req.raise_for_status()
    return json.loads(req.text)

# def getFullCourseData(courseid, token, until=None): # until is of type date, e.g. datetime.now()
#   reference_time = getTime()
#   init_data = getCourseData(courseid, token, page=0, reference_time=reference_time)
#   last_page = int(init_data["last_page"])
#   files = init_data["files"]
#   for i in range(1,last_page+1):
#       if (until != None) and (len([f for f in files datetime.strptime(f["uploaded"], '%Y-%m-%d %H:%M:%S')>until])==0):
#           break
#       files.extend(getCourseData(courseid, token, page=i, reference_time=reference_time)["files"])
#   init_data["files"] = files
#   return init_data

def getMyself(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/myself'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def followUser(token, userID): #seems to be broken
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/profiles/{}/follow'.format(baseurl,userID), headers=headers)
    req.raise_for_status()
    return req.text

def getDocument(docid, token):
    headers={"authorization": "Bearer "+token}
    #uploadDate = datetime.strptime(data["files"][0]["uploaded"], '%Y-%m-%d %H:%M:%S')
    req = requests.get('{}api/app/v1/documents/{}/download'.format(baseurl,docid), headers=headers)
    req.raise_for_status()
    return req.content

def getProfileDocuments(profileID, token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/profiles/{}/documents'.format(baseurl,profileID), headers=headers)
    req.raise_for_status()
    return req.text

def getProfileFlashcards(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/feed/my_flashcard_sets'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def getDocumentDetails(docid, token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/documents/{}/details'.format(baseurl,docid), headers=headers)
    req.raise_for_status()
    return req.text

def getMyDocuments(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/feed/my_documents'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def getMyInteractionFeed(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/feed/my_answers_feed'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def getMyStats(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/users/right_sidebar_stats'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def getInformationAboutQuestion(token, questionType, questionID):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/{}/questions/{}'.format(baseurl,questionType,questionID), headers=headers)
    req.raise_for_status()
    return req.text

def getMyQuestions(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/feed/my_questions_feed'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def upvoteAnswer(token, answerType, answerID):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/{}/answers/{}/upvote'.format(baseurl,answerType,answerID), headers=headers)
    req.raise_for_status()
    return req.text

def upvoteQuestion(token, questionType, questionID):
    headers={"authorization": "Bearer "+token}
    params={'question_id': questionID, 'question_type': questionType}
    req = requests.post('{}api/app/v1/questions/upvote'.format(baseurl), headers=headers, params=params)
    req.raise_for_status()
    return req.text

def upvoteDocument(token, fileID):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/documents/{}/upvote'.format(baseurl,fileID), headers=headers)
    req.raise_for_status()
    return req.text

def upvoteFlashcard(token, flashcardID):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/flashcards/sets/{}/vote/up'.format(baseurl,flashcardID), headers=headers)
    req.raise_for_status()
    return req.text

def startFlashcard(token, flashcardID):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/flashcards/sets/{}/study/start'.format(baseurl,flashcardID), headers=headers)
    req.raise_for_status()
    return req.text

def finishFlashcard(token, flashcardID):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/flashcards/sets/{}/study/finish'.format(baseurl,flashcardID), headers=headers)
    req.raise_for_status()
    return req.text

def getLeftSidebar(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/users/left_sidebar'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def setCourseOrder(courses, token):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/community/order'.format(baseurl), headers=headers, data={'context':'course', 'ids[]': courses})
    req.raise_for_status()
    return req.text

def joinCourse(courseID, token):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/courses/{}/join'.format(baseurl,courseID), headers=headers)
    req.raise_for_status()
    return req.text

def getMyCourses(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/myself/courses'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.text

def getMajors(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}/api/app/v1/users/majors'.format(baseurl), headers = headers)
    req.raise_for_status()
    return req.text

def getAllMajors(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}/api/app/v1/majors'.format(baseurl), headers = headers)
    req.raise_for_status()
    return req.text

def giveKarma(token):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}/api/app/v1/users/give-karma'.format(baseurl), headers = headers)
    req.raise_for_status()
    return req.text

def courseExpertDashboard(token):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}/api/app/v1/ke/dashboard'.format(baseurl), headers = headers)
    req.raise_for_status()
    return req.text

def getCredits(userID):
    r = requests.get("https://www.studydrive.net/de/profile/sauron/{}#documents".format(userID))
    html = r.text
    result = re.search('sdWindow.profile = (.*);sdWindow.isTablet', html)
    return json.loads(result.group(1))["credits"]

def getStats(token, userID):
    headers={"authorization": "Bearer "+token}
    params = {"user_id": userID}
    req = requests.get('{}api/app/v1/profiles/{}'.format(baseurl, userID), headers = headers, params = params)
    req.raise_for_status()
    return req.json()

def switchNotification(token, id, notificationType):
    headers={"authorization": "Bearer "+token}
    params = {"id": id, "notification_type": notificationType}
    req = requests.post('{}api/app/v1/users/settings'.format(baseurl), headers = headers, params = params)
    req.raise_for_status()
    return req.json()

def switchPushNotification(token):
    ids = [8, 10, 11, 14, 15, 28, 29, 45, 46, 44]
    for id in ids:
        switchNotification(token, id, "app")

def switchMitteilungen(token):
    ids = [9, 12, 13, 48, 49, 50]
    for id in ids:
        switchNotification(token, id, "app")

def switchEmail(token):
    ids = [39, 40, 41, "mailsummery", "newsletter", "partner", "exam_dates"]
    types = ["app", "app", "app", "email", "email", "email", "email"]
    for id, type in zip(ids, types):
        switchNotification(token, id, type)

def switchNewsfeed(token):
    ids = [1, 2, 3, 4, 5, 6, 7]
    for id in ids:
        switchNotification(token, id, "app")

def crawlForInformation(token, masterID, masterName):
    # search for documents
    documentFile = open("documents.txt", "w+")
    documents = getMyDocuments(token)
    rawData = makeReadyForJSON(documents)
    JSON = json.loads(rawData)
    length = len(JSON["files"])
    for i in range(length):
        documentID = JSON["files"][i]["file_id"]
        documentFile.write(str(documentID) + "\n")
        #documentName = JSON["files"][i]["file_name"]
        #documentFile.write(str(documentID))
    documentFile.close()

    # search for flashcards
    flashcardFile = open("flashcards.txt", "w+")
    flashcards = json.loads(makeReadyForJSON(getProfileFlashcards(token)))
    for flashcard in flashcards['data']:
        flashcardID = flashcard['id']
        flashcardFile.write(str(flashcardID) + "\n")
    flashcardFile.close()

    # search for questions/answers
    answerFile = open("answers.txt", "w+")
    questionFile = open("questions.txt", "w+")
    answers = getMyInteractionFeed(token)
    answersJSON = json.loads(makeReadyForJSON(answers))
    length = len(answersJSON["notifications"])
    for i in range(length):
        questionType = answersJSON["notifications"][i]["question_item"]["questionType"]
        questionID = answersJSON["notifications"][i]["question_item"]["data"]["id"]
        author = answersJSON["notifications"][i]["question_item"]["data"]["user_data"]["name"]
        #print str(author) + ": " + str(questionType) + " | " + str(questionID)
        if author != masterName:
            # I gave an answer
            information = getInformationAboutQuestion(token, questionType, questionID)
            informationJSON = json.loads(makeReadyForJSON(information))
            NumberOfAnswers = len(informationJSON["data"]["answers"])
            for j in range(NumberOfAnswers):
                answerAuthor = informationJSON["data"]["answers"][j]["user_data"]["name"]
                if answerAuthor == masterName:
                    answerID = informationJSON["data"]["answers"][j]["id"]
                    #print "   " + str(answerAuthor) + " | " + str(answerID)
                    answerFile.write(str(questionType) + "|" + str(answerID) + "\n")
        else:
            #print "   Upvote Me!"
            questionFile.write(str(questionType) + "|" + str(questionID) + "\n")
    answerFile.close()
    questionFile.close()
