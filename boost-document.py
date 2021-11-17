from studydriveapi import *
from functions import *

import argparse

# Create the parser
my_parser = argparse.ArgumentParser(description = 'Give me the ID of the document')

# Add the arguments
my_parser.add_argument('id', metavar='id', type=str, help='ID of document')

# Execute the parse_args() method
args = my_parser.parse_args()

docID = args.id

file = open("alts.txt")
alts = file.read().splitlines()
file.close()

for alt in alts:
    try:
        username = alt.split(":")[0]
        password = alt.split(":")[1]
        folderName = username.split("@")[0]
        print "Use alt: " + str(username)
        #download the documents
        tokenAlt = login(username, password)
        print "Downloading documents:"
        f = open(folderName + "/downloadedDocuments.txt", "a+")
        document = getDocument(docID, tokenAlt)
        f.write(str(docID) + "\n")
        f.close()
    except Exception as e:
        pass
