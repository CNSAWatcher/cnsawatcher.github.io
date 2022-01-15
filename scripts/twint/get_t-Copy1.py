from git import Repo
from pathlib import Path
from time import sleep
import os
# print(Path(path).parent.name)

PATH_OF_GIT_REPO = Path(os.getcwd()).parent.parent  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'auto update'

# repo = git.Repo(os.getcwd())
# files = repo.git.diff(None, name_only=True)
# for f in files.split('\n'):
#     show_diff(f)
#     repo.git.add(f)

# repo.git.commit('test commit', author='sunilt@xxx.com')


def git_push():
#     try:
    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add(all=True)
    repo.git.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()
#     except Exception as e:
#         print(str(e))    


while True:
    git_push()
    print(123)
    sleep(1800)