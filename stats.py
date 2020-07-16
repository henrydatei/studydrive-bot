from studydriveapi import *
from datetime import datetime

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

stats = json.loads(makeReadyForJSON(getMyStats(token)))

credits = stats['credit_points']
karma = stats['karma_points']
karmaRank = stats['karma_rank']
totalUploads = stats['total_uploads']
totalDownloads = stats['total_downloads_generated']
totalUpvotes = stats['total_upvotes']
totalPosts = stats['total_posts']
totalAnswers = stats['total_answers']
totalBestAnswers = stats['total_best_answers']
totalFlashcards = stats['total_flashcard_sets']
followedPosts = stats['followed_posts']
followedFiles = stats['followed_files']
followedFlashcards = stats['followed_flashcard_sets']
followedUsers = stats['followed_users']

currentDate = datetime.now().strftime('%Y-%m-%d')

print currentDate + "," + str(credits) + "," + str(karma) + "," + str(karmaRank) + "," + str(totalUploads) + "," + str(totalDownloads) + "," + str(totalUpvotes) + "," + str(totalPosts) + "," + str(totalAnswers) + "," + str(totalBestAnswers) + "," + str(totalFlashcards) + "," + str(followedPosts) + "," + str(followedFiles) + "," + str(followedFlashcards) + "," + str(followedUsers)
