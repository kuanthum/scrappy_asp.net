import scrapy
import time

from scrapy.http import FormRequest
from scrapy.exceptions import CloseSpider
from apto_scrap.payloads import submit_1, change_page, change_page_2, change_page_3, change_page_4

from apto_scrap.items import AptoScrapItem

HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}

URL = 'https://sidano.org.ar:1100/'

class SidanoSpider(scrapy.Spider):
    name = "sidano_spider"
    item_count = 0
    page = 1

    allowed_domains = ["www.sidano.org.ar"]
    
    def start_requests(self):
        urls = [
            'https://sidano.org.ar:1100/',
        ]
        for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data = submit_1
        return FormRequest(url=URL,
                        method='POST',
                        callback=self.parse_page,
                        formdata= data,
                        meta={'page': 1},
                        dont_filter = True,
                        headers=HEADERS
                        )

    def parse_page(self, response):
        current_page = response.meta['page'] + 1

        print(current_page)

        self.item_count += 1
        a_item = AptoScrapItem()
        
        cantidad = len(response.xpath("//tr").getall())
        #print(f'cantidad={cantidad}')

        #parse
        for i in range(2, cantidad-1):
            a_item['registro']     = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][1]/text()").extract()
            a_item['cargo']        = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][2]/text()").extract()
            a_item['dni']          = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][3]/text()").extract()
            a_item['calle']        = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][4]/text()").extract()
            a_item['barrio']       = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][5]/text()").extract()
            a_item['localidad']    = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][6]/text()").extract()
            a_item['departamento'] = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][7]/text()").extract()
            a_item['delegacion']   = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][8]/text()").extract()
            a_item['tel']          = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][9]/text()").extract()
            a_item['tel_2']        = response.xpath(f"//tr[{i}]/td[@class='item-col-style'][10]/text()").extract()
            yield a_item



        if current_page < 12:
            data = change_page(current_page)
        elif current_page < 22:
            data = change_page_2(current_page)
        elif current_page < 32:
            data = change_page_3(current_page)
        else:
            data = change_page_4(current_page)

        if current_page %3 == 0:
            time.sleep(2)

        if self.item_count == 37:
            raise CloseSpider('item_exceeded')

        yield FormRequest(url=URL,
                        method='POST',
                        formdata=data,
                        callback=self.parse_page,
                        meta={'page': current_page},
                        dont_filter = True,
                        headers=HEADERS
                        )