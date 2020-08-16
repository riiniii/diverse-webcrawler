from selenium import webdriver


from utilities import Utilities 
from GRListopiaCrawler import ListopiaCrawler
from GRBookCrawler import GRBookCrawler
from selenium.webdriver.support.ui import WebDriverWait

import credentials

# crawl all lists of pages using GRListopicaCrawler and CRBookCrawler

# call BookCrawler when we already have lists of urls to crawl
# can call populate lists.txt too when we want more lists
# takes in starting page


class GRCrawler:
    def __init__(self, startingUrl, username, password, listFilename):
        self.username = username
        self.password = password
        self.startingUrl = startingUrl
        self.listFilename = 'lists.txt' # listFilename

        self.driver = webdriver.Chrome()
        self.utilities = Utilities(self.driver, username, password)
        
    
    # crawl from beginning
    def crawl(self):
        self.utilities.login()
        listCrawler = ListopiaCrawler(self.url, self.username, self.password, self.listFilename)
        listCrawler.crawlLists()
    # we have our lists of list urls, just crawl from cgbookcrawler
    def crawlBooks(self, listToRead = 'lists.txt'):
        # listsOfUrl = self.readListsFromTextfile(self.listFilename)
        listsOfUrl = self.readListsFromTextfile(listToRead)
        for index in range(len(listsOfUrl)):
            print index
            listUrl = listsOfUrl[index]
            outputUrls = 'output/books/urls/' + str(index) + '.txt'
            outputDetails = 'output/books/details/' + str(index) + '.json'
            bookCrawler = GRBookCrawler(listUrl, credentials.username, credentials.password, outputUrls, outputDetails)

            bookCrawler.crawlBooks()
            
            # if index + 1 < len(listsOfUrl):
            #     nextListUrl = listsOfUrl[index+1]
            #     self.waitForNextList(nextListUrl)
    
    def waitForNextList(self, desired_url):
        WebDriverWait(self.driver, 86400).until(
            lambda driver: driver.current_url == desired_url)
    
    def readListsFromTextfile(self, filename):
        text_file = open(filename, "r")
        lines = text_file.read().split('\n')
        
        return lines


# get my lists and send it to 'lists.txt'
startingPage = 'https://www.goodreads.com/list/tag/female-authors?page=1' 

grCrawler = GRCrawler(startingPage, credentials.username, credentials.password, 'urlsOfFemaleAuthors.txt')

grCrawler.crawlBooks()