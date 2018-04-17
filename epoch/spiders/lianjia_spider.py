# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 
# @Author  : fc.w
# @File    : lianjia_spider.py
import scrapy
from scrapy import Selector


class LianjiaSpider(scrapy.Spider):
    """
    链家
    爬取地图找房板块中的区域信息
    """
    name = 'lianjia_spiders'
    allowed_domains = ['cs.lianjia.com']

    def start_requests(self, response):
        yield scrapy.Request("https://cs.lianjia.com/", self.lianjia_home_page)

    def lianjia_home_page(self, response):
        """
        链家首页
        :param response:
        :return:
        """
        selector = Selector(response)
        selector.xpath('//div[@class="fc-main clear"]/div/ul/li[@class="clear"]/div/a/@href').extract()
        selector.xpath('//div[@class="fc-main clear"]/div/ul/li[@class="clear"]/div/a/text()').extract()

