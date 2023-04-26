from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import qrcode  
import cv2  
import dbconfig as db

def user_chat():
	pass

if __name__ == '__main__':

	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")
	CHROMEDRIVER_PATH = 'utils/chromedriver.exe'
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
	driver.get('https://web.whatsapp.com/')

	time.sleep(20)