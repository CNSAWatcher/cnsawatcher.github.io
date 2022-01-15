from git import Repo
from pathlib import Path
from time import sleep
import os
# print(Path(path).parent.name)

PATH_OF_GIT_REPO = Path(os.getcwd()).parent.parent  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'auto update'
def git_push():
#     try:
    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add(all=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()
#     except Exception as e:
#         print(str(e))    


while True:
    git_push()
    print(123)
    sleep(1800)