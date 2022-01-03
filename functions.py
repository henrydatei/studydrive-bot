import difflib
import random
from studydriveapi import *

def getAdditionsFromFiles(file1Location, file2Location):
    # copied from https://stackoverflow.com/questions/19120489/compare-two-files-report-difference-in-python
    file1 = open(file1Location, "r")
    file1List = file1.readlines()
    file1List.sort();
    lines1 = "".join(str(line) for line in file1List)
    file2 = open(file2Location, "r")
    file2List = file2.readlines()
    file2List.sort();
    lines2 = "".join(str(line) for line in file2List)
    diff = difflib.unified_diff(lines1.strip().splitlines(), lines2.strip().splitlines(), fromfile='file1', tofile='file2', lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    file1.close()
    file2.close()
    return added

def sortCourses(token):
    list = []
    ids = []
    courses = json.loads(makeReadyForJSON(getLeftSidebar(token)))
    for courseData in courses['courses']:
        courseID = courseData['course_id']
        courseName = courseData['course_name']
        list.append([courseID,courseName])
    #print str(list)
    ### sort
    sortedList = sorted(list, key=lambda tup: tup[1])
    #print str(sortedList)
    for courseData in sortedList:
        id = courseData[0]
        ids.append(id)
    #print str(ids)
    print(setCourseOrder(ids[::-1],token))

def getCourseDifference(tokenMain,tokenAlt):
    #main
    courses = json.loads(makeReadyForJSON(getMyCourses(tokenMain)))
    mainCourses = []
    for course in courses['courses']:
        courseID = course['id']
        mainCourses.append(courseID)

    #alt
    courses = json.loads(makeReadyForJSON(getMyCourses(tokenAlt)))
    altCourses = []
    for course in courses['courses']:
        courseID = course['id']
        altCourses.append(courseID)

    difference = list(set(mainCourses) - set(altCourses))
    return difference
