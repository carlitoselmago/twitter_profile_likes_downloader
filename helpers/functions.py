import os
from furl import furl
from bs4 import BeautifulSoup
import requests
from pathlib import Path    
import urllib.request
import configparser
import os
#from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver as uc
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

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

    full_path = destfolder+'/' + file_name# + '.jpg'
    urllib.request.urlretrieve(url, full_path)
    
def download_video():
    video_url = driver.find_element_by_xpath('//video[@id="video_id"]/source').get_attribute('src')

    # download the video
    r = requests.get(video_url, stream = True)

    # check if the request is successful.
    if r.status_code == 200:
        # set video file paths
        path = os.getcwd()
        path += '/your_video.mp4'
        
        # start download
        with open(path, 'wb') as f:
            f.write(r.content)
            
    driver.close()

def download_video_sellenium(tweet_url,user):
    #browser = webdriver.Firefox()
  
    browser = uc.Chrome(headless=False,use_subprocess=True)
    wait = WebDriverWait(browser, 30)
    browser.get('https://twittervideodownloader.com/')

    cookies=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[mode="primary"]'))).click()
    
    sleep(1)

    tweet_input = wait.until(EC.visibility_of_element_located((By.NAME, "tweet")))
    for character in tweet_url:
        tweet_input.send_keys(character)
        sleep(0.3) # pause for 0.3 seconds
       
    sleep(2)
    tweet_input.send_keys(Keys.ENTER)



def download_video_old(tweet_url,user):
    destfolder=userfolder(user)
    tweet_url = tweet_url.split('?', 1)[0]
    session = requests.Session()
    response = session.get('http://twittervideodownloader.com')
    print('Cookies: ', response.cookies.get_dict()) # print all cookies from the server
    csrf = session.get('http://twittervideodownloader.com').cookies['csrftoken']
    result = session.post('http://twittervideodownloader.com/download', data={'tweet': tweet_url, 'csrfmiddlewaretoken': csrf})
    
    if result.status_code == 200:
    
        bs = BeautifulSoup(result.text, 'html.parser')
        video_element = bs.find('a', string='Download Video')
        
        if video_element is None:
            print('video not found !')
        else:
            video_url = video_element['href']
            tweet_id = tweet_url.split('/')[-1]
            fname = tweet_id + '.mp4'
            
            download_result = session.get(video_url, stream = True) 
            with open(Path(destfolder) / Path(fname), 'wb') as video_file:
                for chunk in download_result.iter_content(chunk_size=1024*1024):
                    # writing one chunk at a time to video file 
                    if chunk:
                        video_file.write(chunk)
                video_file.close()
    else:
        print('an error in downloading video! status code: ' + result.status_code)



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


