from selenium import webdriver
from selenium.webdriver.common.by import By

from utilities import Utilities 
import credentials

# example of urls from lists.txt
# given a list of books, crawl that page
class GRBookCrawler:
    def __init__(self, url, username, password, urlFilename, booksJsonFilename):
        self.driver = webdriver.Chrome()
        self.utilities = Utilities(self.driver, username, password)

        self.listUrl = url
        self.books = {} # used in bookUrlsToData(bookUrls)
        self.bookUrls = []
        self.urlFilename = urlFilename
        self.booksFilename = booksJsonFilename

    def testCrawlBooks(self, maxBooks):
        self.crawlBooks(maxBooks)

    def crawlBooks(self, maxBooks = -1):
        try: 
            # blach
            self.utilities.login() # to-do, move this to crawler func
            self.listToBookUrls(maxBooks)
            self.bookUrlsToData()
        except Exception as e:
            self.saveData()
            print(e)
        self.saveData()
        return 1

    def close(self):
        self.driver.close()

    def saveData(self):
        self.utilities.writeToText(self.bookUrls, self.urlFilename)
        self.utilities.writeToJSON(self.books, self.booksFilename)
        self.driver.close()

    def listToBookUrls(self, maxBooks):
        currBookIndex = 0
        current_url = self.driver.current_url

        try: 
            # go to list of books url 
            self.driver.get(self.listUrl)
            self.utilities.waitNewUrl(current_url, 10)

            # at the list of books now, and we want the url for each book 
            books = self.utilities.find_elements(self.driver, By.CLASS_NAME, 'bookTitle')
            for book in books: 
                if maxBooks is -1 or currBookIndex < maxBooks:
                    # append all book urls
                    bookUrl = book.get_attribute('href')
                    if bookUrl not in self.bookUrls:
                        self.bookUrls.append(bookUrl)   
                    currBookIndex += 1
                else:
                    return 

            # apparently 10 seconds is the "standard delay," also to help avoid us from getting blocked
            self.utilities.wait(10)
        except Exception as e:
            print(e)
            self.close()
    
    def bookUrlsToData(self):
        current_url = self.driver.current_url
        try: 
            for bookUrl in self.bookUrls: 
                self.driver.get(bookUrl)
                self.utilities.waitNewUrl(current_url, 10)

                isbn = self.getIsbn()

                if isbn is not '':
                    self.books[isbn] = self.getBookDetails(isbn)
        except Exception as e:
            self.close()
            print(e)
            pass
            # maybe one list will throw an error, so write at end of eery list loop for safety
        

    # parsers
    def getId(self):
        title = ''
        try:
            title = self.utilities.find_element(self.driver, By.ID, 'bookTitle').get_attribute('innerHTML')
        except:
            pass
        return title.strip()

    def getAuthor(self): 
        author = ''
        try:
            author = self.utilities.find_element(self.driver, By.XPATH, '//*[@id="bookAuthors"]/span[2]/div/a/span').get_attribute('innerHTML')
        except:
            pass
        return author

    def getDescription(self): 
        description = ''
        try:
            description = self.utilities.find_element(self.driver, By.XPATH, '//*[@id="description"]/span[2]').get_attribute('innerHTML')
        except:
            pass
        return description

    def getIsbn(self): 
        isbn = ''
        try: 
            isbn = self.utilities.find_element(self.driver, By.CSS_SELECTOR, '[itemprop="isbn"]').get_attribute('innerHTML')
        except:
            pass
        return isbn

    def getGenres(self):
        listOfGenres = self.utilities.find_elements(self.driver, By.CSS_SELECTOR, 'div.left a.bookPageGenreLink')
        genres = []
        for genre in listOfGenres:
            genres.append(genre.get_attribute('innerHTML'))
        return genres

    def getBookDetails(self, isbn):
        return {
                "title": self.getId(),
                "authors": self.getAuthor() ,
                "description": self.getDescription(),
                "genres": self.getGenres(),
                "imgUrl": self.getImgUrl(),
                "ratingValue": self.getRatingValue(),
                "isbn": isbn,
            }

    def getImgUrl(self):
        imgUrl = ''
        try: 
            imgUrl = self.utilities.find_element(self.driver, By.ID, 'coverImage').get_attribute('src')
        except:
            pass
        return imgUrl
    
    def getRatingValue(self):
        ratingValue = ''
        try:
            ratingValue = self.utilities.find_element(self.driver, By.CSS_SELECTOR, 'span[itemprop="ratingValue"]').get_attribute('innerHTML')
        except:
            pass
        return ratingValue.strip()

# booksUrl = 'https://www.goodreads.com/list/show/442.Best_Jodi_Picoult_Books'

# bookCrawler = GRBookCrawler(booksUrl, credentials.username, credentials.password, 'test.txt', 'books.json')

# # bookCrawler.crawlBooks()
# bookCrawler.testCrawlBooks(3)