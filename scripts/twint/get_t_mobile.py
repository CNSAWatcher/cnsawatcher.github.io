import twint
import nest_asyncio
import os
from time import sleep
from datetime import datetime
import pandas as pd
import re
import json
import subprocess
from googleapiclient.discovery import build
import urllib.request 


# from git import Repo
# from pathlib import Path
# print(Path(path).parent.name)

# PATH_OF_GIT_REPO = Path(os.getcwd()).parent.parent  # make sure .git folder is properly configured
# COMMIT_MESSAGE = 'auto update'

def dfToList(df):
    return list(df.T.to_dict().values())

def saveJSON(data, jsonFilename):
    data.sort(key = lambda x: (x['date'], x['time']), reverse = True)
    with open(jsonFilename, 'w', encoding="utf-8") as f:
        json.dump(data , f, ensure_ascii=False)


# assert os.path.isfile(r'..\\..\\..\\log.txt')
def save_to_file(str):
    print(str)
    with open(r'../../../log.txt', 'a') as f:
        f.write(str + '\n')
def command(cmds):
    subprocess.call(cmds)

# def git_pull():
#     try:
#         repo = Repo(PATH_OF_GIT_REPO)
#         repo.git.pull
#     except Exception as e:
#         save_to_file(str(e))  
        
# def git_push():
#     try:
#         repo = Repo(PATH_OF_GIT_REPO)
#         repo.git.add(all=True)
#         repo.index.commit(COMMIT_MESSAGE)
#         origin = repo.remote(name='origin')
#         origin.push()
#     except Exception as e:
#         save_to_file(str(e))    

# suppress = " >/dev/null 2>&1"

count = 0

while True:
    """
    git pull
    """

    save_to_file("-"*50)
    save_to_file((datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    print("Turn: " + str(count))
#     os.system("git pull"+suppress)
#     git_pull()


#init gitt
    command(["git", "pull"])
    save_to_file(("Git Pulled"))
    sleep(30)


    """
    get tweets
    """
    tmpFilename = 'tweetsTmp.csv'
    file = open(tmpFilename,"w+")
    file.truncate(0)
    file.close()

    sep = "\t"
    nest_asyncio.apply()
    config = twint.Config()
    # print(config.Proxy_host)
    # config.Proxy_host = "proxy.server^&%$"
    # print(config.Proxy_host)
    # config.Proxy_port = "3128"
    # config.Proxy_type = "http"
    config.Username = "cnsawatcher"
    # config.Search = ""
    config.Limit=10000
    config.Since = '2021-04-01'
    config.Store_object = True
    config.Output = tmpFilename
    config.Format = "{id}"+sep+"{date}"+sep+"{time}"+sep+"{link}"+sep+"{thumbnail}"+sep+"{tweet}"
    config.Hide_output = True

    save_to_file(("Feed Starts"))
    try:
        twint.run.Search(config)
    except Exception as e:
        save_to_file(e)
    else:
        save_to_file("Feed Got")
#     sleep(5)
    
    """
    Saving JSON
    """
    df_tmp = pd.read_csv(tmpFilename, sep = sep, names=['id','date','time','link','thumbnail','tweet'])
    df_tmp = df_tmp.fillna('')
    df_tmp = df_tmp[~df_tmp['tweet'].str.startswith('@')]

    df = pd.read_csv('tweets.csv', sep = sep, names=['id','date','time','link','thumbnail','tweet'])#names=['id','date','time','tweet']
    df = df.fillna('')
    df = df[~df['tweet'].str.startswith('@')]

    df_new = pd.concat([df,df_tmp]).drop_duplicates(subset=['tweet']).sort_values(by = ['date', 'time'], ascending = False)
    df_new.to_csv('tweets.csv', sep = sep, header = False, index = False)
    df_new = df_new[~df_new['tweet'].str.startswith('@')]
    
    
    
    df = pd.read_csv('tweets.csv', sep = sep, names=['id','date','time','link','thumbnail','tweet'])#names=['id','date','time','tweet']
    df = df.fillna('')

    searchforMars = ['mars','zhurong','tianwen','martian']
    df_mars = df[df['tweet'].str.contains('|'.join(searchforMars),flags=re.IGNORECASE)]

    searchforMoon = ["chang’e", "chang'e", "change","moon","yutu","lunar"]
    df_moon = df[df['tweet'].str.contains('|'.join(searchforMoon),flags=re.IGNORECASE)]
    df_moon = df_moon[df_moon['tweet'].str.contains('lunar new year', flags=re.IGNORECASE) == False]


    searchforCSS = ['Tiangong','Shenzhou','Space Station','Tianhe', "CSS","Astronaut","spacewalk","EVA","Nie Haisheng","Liu Boming","Tang Hongbo"]
    df_CSS = df[df['tweet'].str.contains('|'.join(searchforCSS),flags=re.IGNORECASE)]

    searchforLaunch = ["launch"]
    df_Launch = df[df['tweet'].str.contains('|'.join(searchforLaunch),flags=re.IGNORECASE)]

    searchforCommercial = ["private", "commercial","spaceglory","originspace","landspace", "galacticenergy"]
    df_Commercial = df[df['tweet'].str.contains('|'.join(searchforCommercial),flags=re.IGNORECASE)]
    
    

    directory = "../../json/"
    saveJSON(dfToList(df), directory + 'all_updates.json')
    saveJSON(dfToList(df_mars), directory + 'mars_updates.json')
    saveJSON(dfToList(df_moon), directory + 'moon_updates.json')
    saveJSON(dfToList(df_CSS), directory + 'css_updates.json')
    saveJSON(dfToList(df_Launch), directory + 'launch_updates.json')
    saveJSON(dfToList(df_Commercial), directory + 'commercial_updates.json')
    
    save_to_file("JSON saved")


    """
    Retrieve remote jsons
    """
    def retrieve_remote_jsons(developerKey = '0MxW8in0Z6F3LnvaGCroiHCMw6Ggn-cWCySazIA'[::-1]):
        print("Retrieving jsons starts...")
        # Create YouTube Object
        youtube = build('youtube', 'v3',
                        developerKey=developerKey)

        def get_list_videos(channelId):
            nextPageToken = None
            return_list = []
            while True:
                sleep(1)
                pl_request = youtube.search().list(
                    part='snippet',
                    q='',
                    channelId=channelId,
                    maxResults=50,
                    pageToken=nextPageToken
                    )
                pl_response = pl_request.execute()

                # Iterate through all response and get video description
                for item in pl_response['items']:
                    # description = item['snippet']['description']
                    return_list.append(item)
                print(nextPageToken)
                nextPageToken = pl_response.get('nextPageToken')
                if not nextPageToken:
                    break
            return return_list

        def get_videos_raw():
            video_raw_list = []
            video_raw_list += get_list_videos('UCmPk2F0Ze-HzDWZ8lEdTRaw')
            video_raw_list += get_list_videos('UCvt59mvaxcTCEb7a0MLJutA')
            return video_raw_list

        def get_videos_list(videos_raw):
            video_list = []
            for item in videos_raw:
                # print(item)
                if item['id']['kind'] == 'youtube#video':
                    video_list.append({'date': item['snippet']['publishTime'][:10].replace('-',''), 'title': item['snippet']['title'].replace('&#39;', "'"), 'description': item['snippet']['description'].replace('&#39;', "'"), 'videoID': item['id']['videoId']})
            video_list.sort(key=lambda item: item['date'], reverse=True)
            return video_list

        def filter_keywords(video_list, keywords):
            ret_list = []
            for item in video_list:
                for word in keywords:
                    if word.lower() in item['description'].lower() or word.lower() in item['title'].lower():
                        ret_list.append(item)
                        break
            return ret_list
        videos_raw = get_videos_raw()
        video_list = get_videos_list(videos_raw)
        css_list = filter_keywords(video_list, ['Tiangong','Shenzhou','Space Station','Tianhe', "CSS","Astronaut","spacewalk","EVA"])
        mars_list = filter_keywords(video_list, ['mars','zhurong','tianwen','martian'])
        moon_list = filter_keywords(video_list, ["chang’e", "chang'e", "change","moon","yutu","lunar"])

        directory = "../../json/"
        with open(directory + 'space_tiangong_gallery_videos.json', 'w') as outfile:
            json.dump(css_list, outfile, ensure_ascii=False)
        with open(directory + 'zhurong_gallery_videos.json', 'w') as outfile:
            json.dump(mars_list, outfile, ensure_ascii=False)
        with open(directory + 'yutu_gallery_videos.json', 'w') as outfile:
            json.dump(moon_list, outfile, ensure_ascii=False)


        with urllib.request.urlopen("https://watcher-3eeb5-default-rtdb.firebaseio.com/launchlog.json") as url:
            data = json.loads(url.read().decode())
            if type(data) == dict:
                data = list(data.values())
                data.sort(key=lambda item: (item['date'], item['time']), reverse=True)
            with open(directory + 'launch_log.json', 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=False)

        with urllib.request.urlopen("https://watcher-3eeb5-default-rtdb.firebaseio.com/upcoming.json") as url:

            data = json.loads(url.read().decode())
            if type(data) == dict:
                data = list(data.values())
                data.sort(key=lambda item: (item['date'], item['time']), reverse=True)
            with open(directory + 'upcoming_activities.json', 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=False)

        print("Retrieving jsons finished")
    
    if count % 4 == 0:
        try:
            retrieve_remote_jsons(developerKey = '0MxW8in0Z6F3LnvaGCroiHCMw6Ggn-cWCySazIA'[::-1])
        except:
            retrieve_remote_jsons(developerKey = 'UnGppUon6l4qt13I_hl8siJT3VLBF32XDySazIA'[::-1])

    """
    git add --all
    """
#     os.system("git add --all"+suppress)
    command(["git", "add", "--all"])
    save_to_file(("files added to git"))
    sleep(30)
    """
    git commit
    """
#     os.system('git commit -m "auto updates"'+suppress)
    command(["git", "commit", "-m", '"auto updates"'])
    save_to_file("files committed")
    sleep(30)
    """
    git push
    """
#     os.system("git push"+suppress)
    command(["git", "push"])
    save_to_file("files pushed")
    save_to_file("")
    
#     git_push()
#     save_to_file("git pushed")

    sleep(1800)
    count += 1

