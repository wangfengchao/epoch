# -*- coding: utf-8 -*-
import BeautifulSoup as BeautifulSoup
import scrapy

from epoch.items.mofcom_items import MofcomItem, FileItem


class MofcomSpider(scrapy.Spider):
    name = "mofcom"
    allowed_domains = ["mofcom.gov.cn"]
    start_urls = ['http://www.mofcom.gov.cn/mofcom/guobiebaogao.shtml']

    def parse(self, response):
        for countryInfo in response.xpath('//tr/td'):
            countrys = countryInfo.xpath('a/text()').extract()
            links = countryInfo.xpath('a/@href').extract()
            if len(countrys) and len(links):
                if "mofcom.gov.cn" in links[0]:
                    item = MofcomItem()
                    item["country"] = countrys[0]
                    item["countryLink"] = links[0]
                    request = scrapy.Request(links[0], callback=self.parse_country)
                    request.meta['item'] = item
                    yield request


    def parse_country(self, response):
        item = response.meta['item']
        for menu in response.xpath("//div[@class=\"navi\"]/ul/li"):
            titles = menu.xpath("a/text()").extract()
            links = menu.xpath("a/@href").extract()
            if len(titles) and len(links) and links[0].find("/article/"):
                item["title"] = titles[0]
                item["titleLink"] = links[0]
                if ".pdf" in links[0]:
                #     request = scrapy.Request(countryLink+"/"+links[0], callback=self.parse_article)
                #     request.meta['item'] = item
                #     yield request
                # else:
                    fileItem = FileItem()
                    countryLink = item["countryLink"]
                    if ".pdf" in links[0] and "/includes/" in links[0]:
                        print "pdf  includes link: "+ (countryLink+"/"+ +links[0])
                        fileItem["file_urls"] = countryLink+"/"+links[0]
                        yield fileItem
                    if ".pdf" in links[0] :
                        print "pdf link: " +links[0]
                        fileItem["file_urls"] = links[0]
                        yield fileItem

    # def parse_article(self, response):
    #     item = response.meta['item']
    #     for alist in response.xpath("//div[@class=\"alist\"]/ul/li"):
    #         titles = alist.xpath("a/text()").extract()
    #         links = alist.xpath("a/@href").extract()
    #         if len(titles) and len(links):
    #             item["articleTitle"] = titles[0]
    #             item["articleLink"] = links[0]
    #             yield item