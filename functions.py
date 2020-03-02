import difflib
import random

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
