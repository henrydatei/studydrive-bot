# studydrive-bot
A bot for boosting your studydrive account

### General information
Studydrive is a platform where students can share lecture notes and ask questions. For interacting with this website you get credits and karma. The idea of this bot is to boost both values by making other accounts like or download your stuff. Therefore you need a main/master account (that account will be boosted) and a few other accounts ("alt-accounts" = "alternative accounts" or short "alts") that will like your stuff. When you create the alts you should use the main-account's reflink to get some extra credits.

**This is just a fun project to play a bit with the api of studydrive. I have no idea if they can detect alts boosting your account. Maybe they will ban you!**

### Features
- download documents
- upvote documents
- upvote answers
- upvote questions
- upvote flashcards
- play flashcards
- joining/leaving the same courses as the main account
- sort courses alphabetically
- boost single document with all alts
- get stats for main account

### Planned Features
- boost random documents/questions/... to make the alts more "legit"
- maybe multi-main-account-support?
- cleanup -> maybe moving API into a PyPi-Package?
- use a database instead of files to save information

### How to use this bot

Currently this repo is just a bunch of scripts (and I want to tidy this up some day) so here is a short tutorial on how this bot is working. If you are purely interested in the API calls have a look at [studydriveapi.py](https://github.com/henrydatei/studydrive-bot/blob/master/studydriveapi.py). Every function there needs a token because for all API requests you have to be authenticated. To get such a token simply run
```python
from studydriveapi import *

token = login("my email", "password")
```
The return of most functions is text although it should be JSON (When I startet this repo the API sometimes retuned malformed JSON so I wrote my own function called `makeReadyForJSON()` that corrects mistakes. Now the API should be returning correct JSON). It should be safe to change the return of every API call from `return req.text` to `req.json()`.
At this point I haven't implemented all API calls but I have extracted a whole list of possible API calls from the Studydrive App. It's called [api-list.md](https://github.com/henrydatei/studydrive-bot/blob/master/api-list.md).

Some more advanced methods I put in the file [functions.py](https://github.com/henrydatei/studydrive-bot/blob/master/functions.py).

Before using this bot you need some alts. You can register new accounts via API too:
```python
from studydriveapi import *

token = register("email", "password")
setNickname(token, "my Nickname")
setProgram(token, universityID = 800, programID = 619, semesterID = 45) # 800 = RWTH Aachen, 619 = Wirtschaftswissenschaften, # 45 = WS 2021/22 [not 100% sure]
```
The IDs for university, program and semester can be retrieved from the API but I haven't implemented that yet.
For the bot to work with the alts there is a certain structure nessesary. For every alt a folder will be created where all information about downloaded documents, liked questions etc. will go. I plan to put all this data into a single database but for now you will have to stay with this. To create all the important files and folders I highly recommend using [add-alt.py](https://github.com/henrydatei/studydrive-bot/blob/master/add-alt.py). It asks for the email and passwords and handles the rest in the background.

You can make your alts look a bit more legit by let them join the same courses as you main account. For that reason I wrote [alts-join-mains-courses.py](https://github.com/henrydatei/studydrive-bot/blob/master/alts-join-mains-courses.py) that will do that and also sort the course list alphabetically. If you just want to sort the courses of your main account use [sort-courses.py](https://github.com/henrydatei/studydrive-bot/blob/master/sort-courses.py).

If you want a script that generates answers for a given question then have a look at [answergenerator.py](https://github.com/henrydatei/studydrive-bot/blob/master/answergenerator.py). It is an AI from microsoft that I liked with studydrive. It answers questions in groups like "Prokratination". More a fun project that anything useful.

To boost just a single document you can use [boost-document.py](https://github.com/henrydatei/studydrive-bot/blob/master/boost-document.py). It's made for command line usage so simply run
```bash
python3 boost-document.py 123456
```
where 123456 is the document ID. You can find this ID in the link to the document: If this is your document https://www.studydrive.net/de/doc/kreise/1203303 then the document ID is 1203303.

It took me quite a while to figure out how the upload process is working. For testing purposes I wrote [upload-document.py](https://github.com/henrydatei/studydrive-bot/blob/master/upload-document.py) where you can see how to upload a document. This code is really awful and I plan to write an easy upload function. But this is currently WIP. Pull requests are highly appreciated.

The bot this repo is all about is in [bot.py](https://github.com/henrydatei/studydrive-bot/blob/master/bot.py). First of all it crawls your main account for documents, posts, answers, flashcards etc. and calculates the difference between what an alt has liked, downloaded etc. From that set a fow documents, questions, answers, flashcards etc will be selected and they will be liked, downloaded etc. Every time you run this bot not all alts will go through this process, only a few to make this legit.

If you want to monitor how the stats from your account are chaning then have a look at [stats](https://github.com/henrydatei/studydrive-bot/blob/master/stats.py) (stats for your main account), [stats2.py](https://github.com/henrydatei/studydrive-bot/blob/master/stats2.py) (stats for your alts) and [statsFromOthers.py](https://github.com/henrydatei/studydrive-bot/blob/master/statsFromOthers.py) (stats for any studydrive profile, here you need the ID of the profile; for this profile https://www.studydrive.net/de/profile/hauser/1835660#documents the ID is 1835660). All these scripts return csv data so simply make a cronjob
```bash
python3 stats.py >> stats.csv
```
and process this data with literally any tool.

Recently I discovered that I can get even more information about a profile via the API so I wrote a script that should crawl all studydrive profiles and download the information. As this is WIP you can have a look at [crawlAllProfiles.py](https://github.com/henrydatei/studydrive-bot/blob/master/crawlAllProfiles.py).

#### Special thanks
Special thanks to [RomanKarwacik](https://github.com/RomanKarwacik) for releasing a [Studydrive Downloader in Python](https://gist.github.com/RomanKarwacik/225ceeca7a7825c0d2be7554c03b2bea) and helping me out with some problems.
