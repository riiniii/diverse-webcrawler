from selenium import webdriver
from selenium.webdriver.common.by import By

from utilities import Utilities 
import credentials

# crawl through all of the lists available
class ListopiaCrawler:
    def __init__(self, url, username, password, listFilename):
        self.listUrls = []
        self.startingUrl = url
        self.listFilename = listFilename

        self.driver = webdriver.Chrome()
        self.utilities = Utilities(self.driver, username, password)

    # only crawl x amount of lists before stopping
    def testCrawlLists(self, maxList):
        self.crawlLists(maxList)

    def crawlLists(self, maxList = -1): 
        try: 
            self.utilities.login()

            self.driver.get(self.startingUrl)
            # assert we are at the right place
            assert "Female Authors Book List" in self.driver.title
            
            self.getPagesOfListUrls(maxList)

            self.utilities.writeToText(self.listUrls, self.listFilename)
        except:
            self.driver.close()


    def getListUrls(self, maxList):
        currListIndex = 0
        listsOfFemaleBooks = self.utilities.find_elements(self.driver, By.CLASS_NAME, "listTitle")
        
        for bookList in listsOfFemaleBooks:
            if maxList is -1 or currListIndex < maxList:
                currListIndex += 1
                self.listUrls.append(bookList.get_attribute('href'))
            else: 
                break
    
    def getPagesOfListUrls(self, maxList): 
        driver = self.driver
        current_url = driver.current_url
        
        self.getListUrls(maxList)
        nextLink = self.utilities.find_element(driver, By.CSS_SELECTOR, "a.next_page[rel='next']")
    
        if nextLink:
            nextLink.click()
            self.utilities.waitNewUrl(current_url, 10)
            self.getPagesOfListUrls(maxList)
        
        return 



# get my lists and send it to 'lists.txt'
# startingPage = 'https://www.goodreads.com/list/tag/female-authors?page=1' 

# goodreadsCrawler = ListopiaCrawler(startingPage, credentials.username, credentials.password)

# goodreadsCrawler.crawlLists()