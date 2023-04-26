from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import qrcode  
import cv2  
import dbconfig as db

while(True):
	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")
	CHROMEDRIVER_PATH = 'utils/chromedriver.exe'
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
	driver.get('https://web.whatsapp.com/')
	time.sleep(20)
	driver.find_element_by_id('app')
	the_soup = BeautifulSoup(driver.page_source, 'html.parser')
	auth_key = the_soup.find('div', {"class": "_19vUU"})['data-ref']
	db.deleteWhatsAppToken()
	db.storeWhatsAppToken(auth_key)
	print(">>>> Auth Key",auth_key)
	qr_img = qrcode.make(auth_key)
	qr_img.show()
	qr_img.save('qr-img1.png')
	time.sleep(60)	      
	driver.quit()