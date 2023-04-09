import subprocess
import os
import time

ddl = "\"2023-04-01\""


def find_java_files(str):
    if os.path.isdir(str):
        os.chdir(str)
        for i in os.listdir("."):
            find_java_files(i)
        os.chdir("..")

    elif (str.endswith(".java")):
        javaFiles.append(os.path.abspath(os.path.dirname(str)) + '/'+str)


def cloneProject(url, user):
    "clone the git repo at url to a local folder at dir for analysis"
    cmd = "git clone " + url + " " + user
    print("executing command " + cmd)
    retCode = subprocess.call(cmd, shell=True)
    if retCode == 0:
        print("clone successful")
        return True
    else:
        print("clone failed")
        return False


def getCommitId(user):
    "return a list of revision numbers in a git repo at local path dir"
    os.chdir(user)
    cmd = "git log --format=%H --before=" + ddl
    print("executing command " + cmd)
    log = subprocess.check_output(cmd, shell=True).decode("utf-8")
    commidIds = []
    lines = log.split("\n")
    for line in lines:
        hash = line.strip()
        if len(hash) > 0:
            commidIds.append(hash)
    if commidIds[0] == commidIds[-2]:
        return [commidIds[0], commidIds[-1]]
    return [commidIds[0], commidIds[-2]] #commidIds[0] is the newest one
    # return commidIds


def findLogsAndDiffs(user, outputPath):
    global javaFiles
    javaFiles = []
    prevWarnCnt = 0
    curWarnCnt = 0
    try:
        outputFile = open(outputPath, 'w')
        commitIds = getCommitId(user)
        print("commit ids are",commitIds)
        numOfCommitIds = len(commitIds)
        for i in range(numOfCommitIds):
            javaFiles = []
            cmd = "git checkout " + commitIds[i]
            print("executing command " + cmd)
            logMessage = subprocess.check_output(cmd, shell=True).decode("utf-8")
            find_java_files(".") # "." represents current working directory
            print(f'all_java_files: {javaFiles}, {i}th')
            
            for file in javaFiles:
                # "java -jar /Users/sqlab/Downloads/checkstyle-10.3-all.jar -c /google_checks.xml "
                cmd = "java -jar D:\Java\checkstyle-10.7.0-all.jar -c /google_checks.xml "+ file
                logMessage = subprocess.check_output(cmd, shell=True).decode("utf-8")
                if logMessage is not None:
                    arrs = logMessage.split("\n")
                    for item in arrs:
                        if "[WARN]" in item:
                            if i != 0:
                                prevWarnCnt += 1
                            else:
                                curWarnCnt += 1
            print(f'{commitIds[i]} prev:{str(prevWarnCnt)} + " ;" + cur:{str(curWarnCnt)}')
            os.chdir(user)
        print(str(prevWarnCnt) + " ;" + str(curWarnCnt))
        outputFile.write("prevWarnCnt: " + str(prevWarnCnt))
        outputFile.write("\n")
        outputFile.write("curWarnCnt: " + str(curWarnCnt))
        outputFile.write("\n")
        if prevWarnCnt > curWarnCnt:
            outputFile.write("True")
            outputFile.write("\n")
        else:
            outputFile.write("False")
            outputFile.write("\n")

        cmd = "git checkout " + commitIds[0]
        print("executing command " + cmd)
        subprocess.check_output(cmd, shell=True).decode("utf-8")
        os.chdir("..")
        print(os.getcwd())
        outputFile.close()
    except Exception as ee:
        print(ee)
