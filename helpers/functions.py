import os
from furl import furl
from bs4 import BeautifulSoup
import requests
from pathlib import Path    
import urllib.request
import configparser
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.parse import urlparse
#from seleniumwire import webdriver
from yt_dlp import YoutubeDL


downloadfolder="downloaded/"


def userfolder(user):
    isExist = os.path.exists(downloadfolder+user)
    if not isExist:

        # Create a new directory because it does not exist
        os.makedirs(downloadfolder+user)

    return downloadfolder+user

def downloadmedia(url,user):
    destfolder=userfolder(user)
    f=furl(url)
    file_name=str(f.path.segments[-1])+"."+f.args["format"]
    f.set({"format":"jpg","name":"large"})
    url=f.url
    full_path = destfolder+'/' + file_name# + '.jpg'
    urllib.request.urlretrieve(url, full_path)
    
def download_video(browser,tweet_url,user):
    #open new tab
    #browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't') 
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    # Open a new window
    browser.execute_script("window.open('');")
    # Switch to the new window
    browser.switch_to.window(browser.window_handles[1])

    destfolder=userfolder(user)

    #browser = webdriver.Firefox()
    wait = WebDriverWait(browser, 30)

    browser.get(tweet_url)

    sleep(1)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "video")))
    poster=browser.find_element(By.CSS_SELECTOR,'video[poster]').get_attribute("poster")
    print("poster::::::::::::",poster)
    parts = urlparse(poster).path.split('/')
    is_video=True
    #for p in parts:
    #    print (p)

    if "tweet_video_thumb" in poster:
        #it's an animated gif  
        is_video=False
        filename=parts[-1].split(".")[0]+".mp4"
        url="https://video.twimg.com/tweet_video/"+filename
        print("gif url",url)
        full_path=userfolder(user)+'/' +filename
        urllib.request.urlretrieve(url, full_path)
    else:
        try:
            i1, i2 = parts.index('amplify_video_thumb')+1, parts.index('img')
        except:
            i1, i2 = parts.index('ext_tw_video_thumb')+1, parts.index('img')
              
        if is_video:
            videoid = '/'.join(parts[i1:i2])
            print("video ID",videoid)
            # Access requests via the `requests` attribute
            for request in browser.requests:
                if request.response:
                    if "fmp4" in request.url:
                        if videoid in request.url:
                            URLS = [request.url]
                            ydl_opts = {
                                    'outtmpl': destfolder+'/%(title)s-%(id)s.%(ext)s'
                                }
                            with YoutubeDL(ydl_opts) as ydl:
                                ydl.download(URLS)
                            break
                        
    #except:
    #    print("could not find amplify_video_thumb")
    
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    
def create_config(config_file_path, user, pwd):
    config = configparser.ConfigParser()
    config.add_section('Credentials')
    config.set('Credentials', 'user', user)
    config.set('Credentials', 'pwd', pwd)
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

def get_config():
    config_file_path = 'settings.ini'
    config = configparser.ConfigParser()
    if os.path.isfile(config_file_path):
        config.read(config_file_path)
        user = config.get('Credentials', 'user')
        pwd = config.get('Credentials', 'pwd')
        print('Settings loaded: User - {}'.format(user))
    else:
        print("settings.ini doesn't exist, introduce your Twitter user and password and the data will be stored for next time")
        user = input('Enter user: ')
        pwd = input('Enter password: ')
        create_config(config_file_path, user, pwd)
        print('Settings saved in settings.ini file.')
    
    return user,pwd