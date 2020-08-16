from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

loginPage = 'https://www.goodreads.com/user/sign_in'

class Utilities:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password

    def wait(self, seconds): 
        print "waiting", seconds, "seconds..."
        self.driver.implicitly_wait(seconds)
        # element_present = EC.presence_of_element_located((by, byStr))
        # WebDriverWait(self.driver, timeout).until(element_present)
    
    def waitNewUrl(self, current_url, waitTime = 15):
        # wait for URL to change with 15 seconds timeout
        WebDriverWait(self.driver, waitTime).until(EC.url_changes(current_url))

    def find_elements(self, driver, by, byStr):
        try: 
            return driver.find_elements(by, byStr)
        except NoSuchElementException:
            print 'NoSuchElementException:', by, byStr 
            return False

    def find_element(self, driver, by, byStr):
        try:
            return driver.find_element(by, byStr)
        except NoSuchElementException:
            print 'NoSuchElementException:', by, byStr
            return False

    def writeToJSON(self, data, filename):
        print "dumping data to", filename
        with open(filename, 'w') as fp: 
            json.dump(data, fp)
    
    def writeToText(self, dataList, filename):
        with open(filename, 'w') as filehandle:
            for listitem in dataList:
                filehandle.write('%s\n' % listitem)
    
    def login(self): 
        driver = self.driver
        driver.get(loginPage)
        try:
            usernameInput = self.find_element(driver, By.ID, 'user_email')
            passwordInput = self.find_element(driver, By.ID, 'user_password')
            submitButton = self.find_element(driver, By.XPATH, '//*[@id="emailForm"]/form/fieldset/div[5]/input')
        
            usernameInput.send_keys(self.username)
            passwordInput.send_keys(self.password)
            
            self.wait(5)
            submitButton.submit()
        except NoSuchElementException:
            print 'lNoSuchElementException'
            return False
        return True

