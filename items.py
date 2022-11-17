# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AptoScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    registro = scrapy.Field()
    cargo = scrapy.Field()
    dni = scrapy.Field()
    calle = scrapy.Field()
    barrio = scrapy.Field()
    localidad = scrapy.Field()
    departamento = scrapy.Field()
    delegacion = scrapy.Field()
    tel = scrapy.Field()
    tel_2 = scrapy.Field()

    pass
