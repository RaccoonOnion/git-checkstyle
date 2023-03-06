import subprocess
import os
import time

ddl = "\"2023-03-30\""


def find_java_files(str):
    if os.path.isdir(str):
        os.chdir(str)
        for i in os.listdir("."):
            find_java_files(i)
        os.chdir("..")

    elif (str.endswith(".java")):
        javaFiles.append(os.path.abspath(os.path.dirname(str)) + '/'+str)
        # print(os.path.abspath(os.path.dirname(str)) + '/'+str)


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
    # os.chdir(dir)
    os.chdir(user)
    print(os.getcwd())
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
    return [commidIds[0], commidIds[-2]]


def findLogsAndDiffs(user, outputPath):
    global javaFiles
    javaFiles = []
    prevWarnCnt = 0
    curWarnCnt = 0
    try:
        outputFile = open(outputPath, 'w')
        os.chdir(user)
        find_java_files(".")
        print(f'all_java_files: {javaFiles}')
        commitIds = getCommitId(user)
        print(commitIds)
        numOfCommitIds = len(commitIds)

        for i in range(numOfCommitIds):
            cmd = "git checkout " + commitIds[i]
            print("executing command " + cmd)
            logMessage = subprocess.check_output(cmd, shell=True).decode("utf-8")

            for file in javaFiles:
                # "java -jar /Users/sqlab/Downloads/checkstyle-10.3-all.jar -c /google_checks.xml "
                cmd = "java -jar D:\Java\checkstyle-10.7.0-all.jar -c /google_checks.xml "+ file
                logMessage = subprocess.check_output(cmd, shell=True).decode("utf-8")
                print(file)
                if logMessage is not None:
                    arrs = logMessage.split("\n")
                    for item in arrs:
                        if "[WARN]" in item:
                            if i != 0:
                                prevWarnCnt += 1
                            else:
                                curWarnCnt += 1
            print(f'{commitIds[i]} prev:{str(prevWarnCnt)} + " ;" + cur:{str(curWarnCnt)}')
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
    except Exception as ee:
        print(ee)
