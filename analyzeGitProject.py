
import os
import sys
import git
urls = [
    "https://github.com/scp-WFZ/Tic-tac-toe",
"https://github.com/ZhangT-tech/Java2Assignment2",
"https://github.com/haodi19/Java2Assign2"
]

users = [
"scp-WFZ",
"ZhangT-tech",
"haodi19"
]

# dir = "/Volumes/v/conffix-subjects/benchmark/pixez-flutter"
for i, user in enumerate(users):
    user = user.strip()
    outputPath = "./"+user+".txt"

    if os.path.exists(user):
        succ = True

    else:
        succ = git.cloneProject(urls[i], user)

    if succ:
        print("clone successful, starting to analyze repo...")
        git.findLogsAndDiffs(user, outputPath)
    else:
        print("clone failed, exit...")
        exit(0)

exit()
