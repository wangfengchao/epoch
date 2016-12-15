#-*- coding:utf-8 -*-

import scrapy

class DaomubijiItem(scrapy.Item):
    bookName = scrapy.Field()
    bookTitle = scrapy.Field()
    chapterNum = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    chapterContent = scrapy.Field()