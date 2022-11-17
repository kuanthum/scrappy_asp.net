import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from apto_scrap.items import AptoScrapItem

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


#class testSpider(scrapy.Spider):
class testSpider(CrawlSpider):

    name       = 'test_spider'
    item_count = 0
    allowed_domain = ['https://sidano.org.ar:1100/']

    rules = {
        # Cuando encuentre cambio de pagina que cambie
        Rule(LinkExtractor(allow=(), restrict_xpaths=('///*[@id="Grilla"]/tbody/tr[22]/td/table/tbody/tr/td[2]/a')))
    }

    def start_requests(self):
        urls = [
            'https://sidano.org.ar:1100/',
        ]
        for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self, name='test_spider',**kwargs):
        super(testSpider, self).__init__(name, **kwargs)
        
        # Disable Chrome for opening in a window and spend resources
        self.options = Options() 
        self.options.add_argument("--headless"),
        self.options.add_argument("--disable-gpu"),
        self.options.add_argument("--no-sandbox")

        # Instantiate Chrome driver
        self.driver  = webdriver.Chrome(chrome_options=self.options)


    # We need Selenium to do some things before scraping the response response (click for showing table)
    @staticmethod
    def get_sele_response(driver,url='https://sidano.org.ar:1100/'):
        driver.get(url)
        button = driver.find_element('xpath','//*[@id="BtnBuscar"]') # Search for the button to click
        button.click()
        wait = WebDriverWait(driver, 30) # Wait until the browser loads the items needed
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-col-style")))
        resp = driver.page_source.encode('utf-8')
        return resp
    
    def parse(self, response):
        my_item = AptoScrapItem()

        response = scrapy.Selector(text=self.get_sele_response(self.driver, response.url)).xpath('//td/text()').getall()

        # Process response
        response = list(map(lambda x: x.strip(), response))
        response = list(filter(None, response))
        
        my_item['page'] = response

        # Save result
        # filename = 'agu.txt'
        # with open(filename, 'w') as f:
        #     f.write(str(response))
        # self.log('Saved file %s' % filename)

