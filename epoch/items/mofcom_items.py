# -*- coding: utf-8 -*-

import scrapy

class MofcomItem(scrapy.Item):
    country = scrapy.Field()
    countryLink = scrapy.Field()
    title = scrapy.Field()
    titleLink = scrapy.Field()
    articleTitle = scrapy.Field()
    articleLink = scrapy.Field()

class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    file = scrapy.Field()