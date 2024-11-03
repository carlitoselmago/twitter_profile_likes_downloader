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

final_filename = None

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

def yt_dlp_monitor(self, d):
    global final_filename
    final_filename  = d.get('info_dict').get('_filename')
    print("final_filename",final_filename)
    # You could also just assign `d` here to access it and see all the data or even `print(d)` as it updates frequently
    
def download_video(browser,tweet_url,user):
    global final_filename
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

    sleep(5)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "video")))

    # Click on the video element
    video_component = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="videoComponent"]')))
    video_component.click()
    poster=browser.find_element(By.CSS_SELECTOR,'video[poster]').get_attribute("poster")
    print("poster::::::::::::",poster)
    parts = urlparse(poster).path.split('/')
    is_video=True
    #for p in parts:
    #    print (p)
    try:
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

                # Extract the video ID from the tweet URL
                parts = tweet_url.split('/')
                videoid = parts[-1]  # last element of url
                videoid = videoid.replace("/pu", "")
                print("Video ID:", videoid)
                print("::::::::::::::::::::::::::::::::::::::::::::::")
                # Define yt-dlp options including cookies from Firefox
                ydl_opts = {
                    'outtmpl': destfolder + f'/{videoid}.%(ext)s',
                    'cookiesfrombrowser': ('firefox',),
                }

                # Create an instance of yt_dlp with the specified options
                with YoutubeDL(ydl_opts) as ydl:
                    # Extract video information
                    info = ydl.extract_info(tweet_url)
                    video_ext = info.get('ext', None)
                    video_fname = destfolder + f"/{videoid}.{video_ext}"
                    video_fname_tmp = destfolder + f"/{videoid}_tmp.{video_ext}"
                    
                    # Download the video
                    ydl.download([tweet_url])
                    sleep(1)
                    
                    # Remux the video to avoid data moshing effect
                    os.system(f"ffmpeg -i {video_fname} -c:v copy -c:a copy {video_fname_tmp}")
                    sleep(1)
                    # Remove the original file and rename the temporary file
                    os.remove(video_fname)
                    os.rename(video_fname_tmp, video_fname)
                    print("Video downloaded and processed successfully!")
                  
                
                            
        #except:
        #    print("could not find amplify_video_thumb")
    except:
        pass
    
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