from helpers.functions import *
from seleniumwire import webdriver

browser = webdriver.Firefox()
download_video(browser,"https://twitter.com/dantheboxingman/status/1694717116778430842","dantheboxingman")