import twint
import nest_asyncio
import os
from time import sleep
from datetime import datetime
import pandas as pd
import re
import json

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


while True:
    """
    git pull
    """


    save_to_file("-"*50)
    save_to_file((datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    os.system("git pull")
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

    df_new = pd.concat([df,df_tmp]).drop_duplicates().sort_values(by = ['date', 'time'], ascending = False)
    df_new.to_csv('tweets.csv', sep = sep, header = False, index = False)
    df_new = df_new[~df_new['tweet'].str.startswith('@')]
    
    
    
    df = pd.read_csv('tweets.csv', sep = sep, names=['id','date','time','link','thumbnail','tweet'])#names=['id','date','time','tweet']
    df = df.fillna('')

    searchforMars = ['mars','zhurong','tianwen','martian']
    df_mars = df[df['tweet'].str.contains('|'.join(searchforMars),flags=re.IGNORECASE)]

    searchforMoon = ["chang’e", "chang'e", "change","moon","yutu","lunar"]
    df_moon = df[df['tweet'].str.contains('|'.join(searchforMoon),flags=re.IGNORECASE)]

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
    git add --all
    """
    os.system("git add --all")
    save_to_file(("files added to git"))
    sleep(30)
    """
    git commit
    """
    os.system('git commit -m "auto updates"')
    save_to_file("files committed")
    sleep(30)
    """
    git push
    """
    os.system("git push")
    save_to_file("files pushed")
    save_to_file("")
    sleep(1800)