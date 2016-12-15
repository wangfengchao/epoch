# -*- coding: utf-8 -*-
import scrapy as scrapy
from scrapy import Selector
from scrapy.http import request

"""
scrapy 登陆后爬数据
"""
class CSDNSpider(scrapy.Spider):
    name = "csdn_login"
    allowed_domains = ["csdn.net"]

    def start_requests(self):
        yield scrapy.Request("https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn", self.parse)

    def parse(self, response):
        return [scrapy.FormRequest.from_response(
            response,
            formdata={'username':'', 'password':''},
            callback=self.login,
            dont_filter=True,
            method = "POST"
        )]

    def login(self, response):
        # print response
        # print response.url
        # print response.status
        # print response.meta
        yield request.Request(response.url.split("?from=")[1], callback=self.after_login_parse)

    def after_login_parse(self, response):
        selector = Selector(response)
        print selector.xpath("//div[@class=\"nav_content\"]/li/a/@href").extract()