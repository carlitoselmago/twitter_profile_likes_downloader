#from helpers import getselleniumdriver #this has to be first
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from helpers.functions import *
from seleniumwire import webdriver
from helpers.db import db
import sys

user,pwd=get_config()

DB=db()

browser = webdriver.Firefox()
browser.maximize_window()
wait = WebDriverWait(browser, 30)
browser.get('https://twitter.com/login')

sleep(3)

username_input = wait.until(EC.visibility_of_element_located((By.NAME, "text")))
username_input.send_keys(user)


nextbtn=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Next')]")))
nextbtn.click()

sleep(3)

#password
username_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
username_input.send_keys(pwd)
username_input.send_keys(Keys.ENTER)

sleep(3)

#now get to the liked posts page
browser.get('https://twitter.com/'+user+'/likes')
wait = WebDriverWait(browser, 30)

sleep(3)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article")))
posts=browser.find_elements(By.CSS_SELECTOR,'div[data-testid="cellInnerDiv"]')

for p in posts:
    #get posturl as id
    timeelem=p.find_element(By.CSS_SELECTOR,'time[datetime]')
    parent=timeelem.find_element(By.XPATH, '..')
    posturl=parent.get_attribute("href")

    print("PROCESS:::",posturl)

    if not DB.postexists(posturl):

        #get userid
        avatar=p.find_element(By.CSS_SELECTOR,'div[data-testid="Tweet-User-Avatar"]')
        if avatar:
            link=avatar.find_element(By.TAG_NAME, "a")
            if link:
                userid=link.get_attribute("href").rsplit('/', 1)[-1]
                print(userid)

                #process media

                #   images
                img_elements = p.find_elements(By.TAG_NAME, "img")
                if img_elements:

                    
                    for img in img_elements:
                        imgsrc=img.get_attribute("src")
                        if "/media/" in imgsrc:
                            print(imgsrc)
                            
                            downloadmedia(imgsrc,userid)
                            print("")

                #   video
                video_elements= p.find_elements(By.TAG_NAME, "video")
                if video_elements:
                    print("video element!")
                    #get post url
                    
                    print("posturl",posturl)
                    
                    download_video(browser,posturl,userid)
                    sleep(2)
                    print("")
                   
        
        DB.insertpost(posturl)
    else:
        print("already saved, skipping....")

print("END:::::::::::::::::::::::::::::::::::::::::::::")
DB.close()