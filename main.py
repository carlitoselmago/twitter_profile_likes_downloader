#from helpers import getselleniumdriver #this has to be first
from helpers import savesettings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

browser = webdriver.Firefox()
browser.maximize_window()
wait = WebDriverWait(browser, 30)
browser.get('https://twitter.com/login')

sleep(0.5)

username_input = wait.until(EC.visibility_of_element_located((By.NAME, "text")))
username_input.send_keys(user)


nextbtn=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Next')]")))
nextbtn.click()

sleep(1)

#password
username_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
username_input.send_keys(pwd)
username_input.send_keys(Keys.ENTER)

sleep(1)

#now get to the liked posts page
browser.get('https://twitter.com/'+user+'/likes')
wait = WebDriverWait(browser, 30)

sleep(1)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article")))
posts=browser.find_elements(By.CSS_SELECTOR,'div[data-testid="cellInnerDiv"]')

for p in posts:
    
    img_elements = p.find_elements(By.TAG_NAME, "img")
    if img_elements:
        for img in img_elements:
            imgsrc=img.get_attribute("src")
            if "/media/" in imgsrc:
                print(imgsrc)


sleep(60)