from studydriveapi import *
from functions import *

baseurl = "https://api.studydrive.net/"


def uploadInit(token): #returns all courses of the university
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/documents/upload/init'.format(baseurl), headers=headers)
    req.raise_for_status()
    return req.json()

def uploadDocument(token,name,description,professor,courseID,semesterID,type,anonymous,self_made,upload_hash,file):
    headers={"authorization": "Bearer "+token}
    parameters={'name': name, 'description': description, 'professor': professor, 'course_id': courseID, 'semester_id': semesterID, 'type': type, 'anonymous': anonymous, 'self_made': self_made, 'upload_hash': upload_hash}
    files = {'file': file}
    req = requests.post('{}api/app/v1/documents/upload'.format(baseurl), headers=headers, data=parameters, files = files)
    req.raise_for_status()
    return req.text

def uploadDocumentFinalize(token,upload_hash):
    headers={"authorization": "Bearer "+token}
    parameters={'upload_hash': upload_hash}
    req = requests.post('{}api/app/v1/documents/upload/{}/finalize'.format(baseurl, upload_hash), headers=headers, params=parameters)
    req.raise_for_status()
    return req.text

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

hash = uploadInit(token)["upload_hash"]
print(hash)
f = open("document3.pdf", "rb")
result = makeReadyForJSON(uploadDocument(token, "test.pdf", "desc", "prof", 326006, 45, 30, 0, 0, hash, f))
print(result)
print(makeReadyForJSON(uploadDocumentFinalize(token, hash)))