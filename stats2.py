from datetime import datetime

currentDate = datetime.now().strftime('%Y-%m-%d')

# main
documents = open("documents.txt").read().splitlines()
answers = open("answers.txt").read().splitlines()
flashcards = open("flashcards.txt").read().splitlines()
questions = open("questions.txt").read().splitlines()

output = currentDate + "," + str(len(documents)) + "," + str(len(answers)) + "," + str(len(flashcards)) + "," + str(len(questions))

# alts
file = open("alts.txt")
alts = file.read().splitlines()
file.close()

for alt in alts:
    folderName = alt.split(":")[0].split("@")[0]
    downloadedDocuments = open(folderName + "/downloadedDocuments.txt").read().splitlines()
    upvotedAnswers = open(folderName + "/upvotedAnswers.txt").read().splitlines()
    upvotedDocuments = open(folderName + "/upvotedDocuments.txt").read().splitlines()
    upvotedFlashcards = open(folderName + "/upvotedFlashcards.txt").read().splitlines()
    upvotedQuestions = open(folderName + "/upvotedQuestions.txt").read().splitlines()

    output = output + "," + str(len(downloadedDocuments)) + "," + str(len(upvotedAnswers)) + "," + str(len(upvotedAnswers)) + "," + str(len(upvotedDocuments)) + "," + str(len(upvotedFlashcards)) + "," + str(len(upvotedQuestions))

print output
