import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from scrapy import Request
from scrapy.http import request
from scrapy.selector import Selector
from scrapy import Spider
from time import sleep

from books_selenium_project.items import BooksSeleniumProjectItem
class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        chrome_options=Options()
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.driver.get('https://books.toscrape.com/')
        sleep(2)
        sel = Selector(text = self.driver.page_source)
        books  = sel.css('.col-xs-6.col-sm-4.col-md-3.col-lg-3')
        for book in books:
            link = book.css('article.product_pod > h3:nth-child(3) a::attr(href)').get()
            url = 'https://books.toscrape.com/'+link
            # print(url)
            self.logger.info('Link is get for each page')
            yield Request(url, callback=self.parse_a)
        while True:
            try:
                # add pagination concept
                self.find_element_by_xpath("//a[contains(text(),'next')]").click()
                sleep(3)
                self.logger.info('Click on next page..')


                sel = Selector(text = self.driver.page_source)
                books  = sel.css('.col-xs-6.col-sm-4.col-md-3.col-lg-3')
                for book in books:
                    link = book.css('article.product_pod > h3:nth-child(3) a::attr(href)').get()
                    url = 'https://books.toscrape.com/'+link
                    print(link)
                    self.logger.info('Link is get for each page')
                    yield Request(url, callback=self.parse_a)

            except NoSuchElementException:
                self.logger.info('No more page found')
                self.driver.quit()
                break

    def parse_a(self, response):
        
        # import pdb; pdb.set_trace()
        print('Call detail function ')
        
        # title = response.css('div.col-sm-6.product_main:nth-child(2) > h1:nth-child(1)::text').get()
        # warning  =  response.css('div.alert.alert-warning:nth-child(6)::text').get()
        # price  =   response.css('.price_color::text').get()
        # url =response.request.url 
        # print('_________________')
        # print('Title ', title)
        # print('Waring ', warning)
        # print('price ', price)
       
        # print('url ', url)
        # print('_________________')
      
        book_item = BooksSeleniumProjectItem()

        book_item['title'] = response.css('div.col-sm-6.product_main:nth-child(2) > h1:nth-child(1)::text').get()
        book_item['warning']  =  response.css('div.alert.alert-warning:nth-child(6)::text').get()
        book_item['price']  =   response.css('.price_color::text').get()
        book_item['url'] =response.request.url 
      
        yield book_item
