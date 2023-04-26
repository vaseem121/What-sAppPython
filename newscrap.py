from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
from selenium.common.exceptions import NoSuchElementException
import lxml.html as lh
from bs4 import BeautifulSoup as bs
import time
import qrcode  
import cv2  
import dbconfig as db
import fr_db as fr
import re
def userList(driver,i,userId):
	data = []
	finalMobile = ''
	userId = userId
	contactNameData = driver.find_element_by_class_name("_8nE1Y").get_attribute('innerHTML')
	soup = bs(contactNameData,"html.parser")
	contactName = soup.find("span",{"class":"_11JPr"}).get_text()
	print(">>>> contactName",contactName)
	time.sleep(20)
	profilePhotoData = driver.find_element_by_class_name("_1AHcd").get_attribute('innerHTML')
	soupProfile = bs(profilePhotoData,"html.parser")
	try:
		profilePic = soupProfile.findAll("img")
		if len(profilePic) != 0:
			profilePhoto = profilePic[0]['src']
			contact_photo = profilePhoto
			print(">>>> profilePhoto",profilePhoto)
		else:
			contact_photo = ''
		try:
			user = driver.find_element_by_xpath("//span[@title='{}']".format(contactName))
			user.click()
			time.sleep(5)
			contactChat = driver.find_element_by_class_name("_24-Ff")
			driver.execute_script("arguments[0].click();", menu)
			profileContactData = driver.find_element_by_class_name("_1xFRo").get_attribute('innerHTML')
			soupProfileContact = bs(profileContactData,"html.parser")
			print(">>>> Contact Profile Data >>>>",profileContactData)
			try:
				statusData = driver.find_element_by_xpath("//span[@title='{}']".format('online')).get_attribute('title')
				if statusData == 'online':
					online_status = statusData
				else:
					online_status = 'offline'
			except NoSuchElementException:
				online_status = 'offline'
			try:
				mobileData = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[5]/div").get_attribute('innerHTML')
				soupsss = bs(mobileData,"html.parser")
				mobile = soupsss.find("div",{"class":"hY_ET"})['data-id']
				splitOne = re.split('_',mobile)
				splitTwo = re.split('@',splitOne[1])
				finalMobile = splitTwo[0]
			except NoSuchElementException:
				print(">>>> No Element Found")
		except NoSuchElementException:
			online_status = 'offline'
	except NoSuchElementException:
		contact_photo = ''
	data.append({'contact_name': contactName,'contact_photo' : contact_photo,'user_id': userId,'online_status': online_status,'contact_phone' : finalMobile })
	fr.saveContactList(data,i) 
	print(">>>> After Login",data)

def userProfileData(driver):
	userData = []
	try:
		menu = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div')
		driver.execute_script("arguments[0].click();", menu)
	except NoSuchElementException:
		print(">>>>>>>> No Element Found!!!!!!")
	time.sleep(20)
	try:
		profile = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[5]/div')
		driver.execute_script("arguments[0].click();", profile)
	except NoSuchElementException: 
		print(">>>>>>>> No Element Found!!!!!!")
	time.sleep(20)
	profile_name = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div/div/div[2]/div[2]/div[1]/div/span').get_attribute('title')
	try:
		profile_photo = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/div/div/div/div[2]/div[1]/div/div/img').get_attribute('src')
		userData.append({'user_name': profile_name,'user_photo' : profile_photo }) 
	except NoSuchElementException:
		userData.append({'user_name': profile_name,'user_photo' : '' })
	user_id = fr.saveUserProfileInfo(userData) 
	print(">>>>> Profile Data",userData)
	return user_id

def returnBack(driver):
	back = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/div/header/div/div[1]/div')
	driver.execute_script("arguments[0].click();", back)

def main():
	keyboard = Controller()
	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")
	CHROMEDRIVER_PATH = 'utils/chromedriver.exe'
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
	driver.get('https://web.whatsapp.com/')
	while(True):
		try:
			time.sleep(20)
			checkLogin = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div').get_attribute("data-ref");
			keyboard.press(Key.enter)
			print(">>>> Home",checkLogin)
			db.deleteWhatsAppToken()
			db.storeWhatsAppToken(checkLogin)
		except NoSuchElementException:
			time.sleep(50)
			user_id = userProfileData(driver)
			returnBack(driver)
			afterLogin = driver.find_elements_by_class_name('rx9719la')
			countRows = (len(afterLogin))
			print(">>>> Count",countRows)
			i=0
			while i < countRows:
				userList(afterLogin[i],i,user_id)

				i += 1	

if __name__ == '__main__':
	main()