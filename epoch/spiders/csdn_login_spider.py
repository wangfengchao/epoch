# -*- coding: utf-8 -*-
import socket

import datetime
import scrapy as scrapy
from scrapy import Selector
from scrapy.http import request
from scrapy.loader import ItemLoader
from epoch.items.csdn_iterms import Product


class CSDNSpider(scrapy.Spider):
    """
    登陆后爬数据
    """
    name = "csdn_login"
    allowed_domains = ["csdn.net"]

    def start_requests(self):
        yield scrapy.Request("https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn", self.parse)

    def parse(self, response):
        return [scrapy.FormRequest.from_response(
            response,
            formdata={'username':'wang915900175', 'password':'wang920311'},
            callback=self.login,
            dont_filter=True,
            method="POST"
        )]

    def login(self, response):
        yield request.Request(response.url.split("?from=")[1], callback=self.page_parse)

    def page_parse(self, response):
        selector = Selector(response)
        il = ItemLoader(item=Product(), selector=selector, response=response)
        il.add_xpath('links', ["//div[@class=\"nav_content\"]/li/a/@href"])
        il.add_value('url', response.url)
        il.add_value('project', self.settings.get('BOT_NAME'))
        il.add_value('spider', self.name)
        il.add_value('server', socket.gethostname())
        il.add_value('date', datetime.datetime.now())
        return il.load_item()


