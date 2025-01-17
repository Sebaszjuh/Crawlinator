# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class crawlinatorItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    status = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    h1 = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    datetime = scrapy.Field()
    threat = scrapy.Field()
