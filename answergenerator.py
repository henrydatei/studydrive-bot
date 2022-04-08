import requests
import json
import random

baseurl = "https://api.studydrive.net/"

def login(user, passwd):
    param = {"client_id": 3,
             "client_secret": "s4lMeCEkNyZcztmpycUlAkSvzAq3gSNjGhGoToDV",
             "grant_type":"password",
             "username": user,
             "password": passwd}
    req = requests.post('{}oauth/token'.format(baseurl), data=param)
    req.raise_for_status()
    return json.loads(req.text)['access_token']

token = login("", "")

def createGroupQuestion(token, text, groupID):
    headers={"authorization": "Bearer "+token}
    params = {"course_id": groupID, "file_id": groupID, "group_id": groupID, "question_type": "group"}
    req = requests.post('{}api/app/v1/group/questions/init'.format(baseurl), headers = headers, params = params)
    req.raise_for_status()
    questionID = req.json()["question_id"]

    params2 = {"is_anonymous": "true", "multi_vote": "false", "question_id": questionID, "question_type": "group", "text": text}
    req = requests.post('{}api/app/v1/group/questions/{}/create'.format(baseurl, questionID), headers = headers, params = params2)
    req.raise_for_status()
    return req.text

def CreateAnswerForGroupQuestion(token, text, questionID):
    headers={"authorization": "Bearer "+token}
    req = requests.post('{}api/app/v1/group/questions/{}/answers/init'.format(baseurl, questionID), headers = headers)
    req.raise_for_status()
    answerID = req.json()["answer_id"]

    params2 = {"is_anonymous": "true", "text": text}
    req = requests.post('{}api/app/v1/group/answers/{}/create'.format(baseurl, answerID), headers = headers, params = params2)
    req.raise_for_status()
    return req.text

def isAnsweredByMe(token, questionID):
    headers={"authorization": "Bearer "+token}
    req = requests.get('{}api/app/v1/group/questions/{}'.format(baseurl, questionID), headers = headers)
    req.raise_for_status()
    
    for answer in req.json()["data"]["answers"]:
        if answer["is_owner"]:
            return True
    return False

def getPage(token, pageNumber, groupID):
    headers={"authorization": "Bearer "+token}
    params = {"group_id": groupID, "page": pageNumber}
    req = requests.get('{}api/app/v1/feed/groups/{}/discussion'.format(baseurl, groupID), headers = headers, params = params)
    req.raise_for_status()
    return req.json()["notifications"]

def findPossibleQuestionsInPage(token, notifications):
    questions = []
    for idx, notification in enumerate(notifications):
        print(" - process question " + str(idx))
        questionID = notification["question_item"]["data"]["id"]
        text = notification["question_item"]["data"]["text"]
        if not isAnsweredByMe(token, questionID) and "corona" not in text.lower() and "impfen" not in text.lower() and "impfung" not in text.lower():
            questions.append((questionID, text))
    return questions

def findPossibleQuestions(token, groupID, maxPages = 20):
    questions = []
    for page in range(maxPages):
        print("Process page " + str(page))
        questions.extend(findPossibleQuestionsInPage(token, getPage(token, page, groupID)))
    return questions


#print(createGroupQuestion(token, "Wer hat heute Bock auf Uni?", 1808))
#print(CreateAnswerForGroupQuestion(token, "ja wirklich nieman", 819357))
#print(isAnsweredByMe(token, 819401))
possibleQuestons = findPossibleQuestions(token, 1808, 3)
possibleQuestons.extend(findPossibleQuestions(token, 2048, 3))
toSelect = 50
if toSelect > len(possibleQuestons):
    toSelect = len(possibleQuestons)
print("Found " + str(len(possibleQuestons)) + " possible questions to answer, selecting " + str(toSelect) + " questions for automatic answer")

import deepl
from deepl import *

def translate_ger_eng(input):
  output = deepl.translate(source_language="german", target_language="english", text=input, formality_tone="informal") #formal, informal möglich
  return output

def translate_eng_ger(input):
  output = deepl.translate(source_language="english", target_language="german", text=input, formality_tone="informal") #formal, informal möglich
  return output

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-large"
#model_name = "microsoft/DialoGPT-medium"
#model_name = "microsoft/DialoGPT-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def getResponse(text, chat_history_ids = []):
	text = translate_ger_eng(text)
	input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
	bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if len(chat_history_ids) > 0 else input_ids
	chat_history_ids_list = model.generate(
        bot_input_ids,
        max_length=1000,
        do_sample=True,
        top_p=0.95,
        top_k=50,
        temperature=0.75,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )
	output = tokenizer.decode(chat_history_ids_list[0][bot_input_ids.shape[-1]:], skip_special_tokens=True)
	output = translate_eng_ger(output)
	return output

for questionID, text in random.sample(possibleQuestons, toSelect):
    response = getResponse(text)
    try:
        print(CreateAnswerForGroupQuestion(token, response, questionID))
    except:
        pass
