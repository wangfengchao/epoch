# -*- coding: utf-8 -*-
import scrapy


class IPProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    alive = scrapy.Field()
    addr = scrapy.Field()