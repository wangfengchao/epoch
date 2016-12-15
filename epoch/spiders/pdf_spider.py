# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

from epoch.items.pdf_items import PDFItem

class PdfdownloadSpider(scrapy.Spider):
    name = "pdfdownload"
    allowed_domains = []

    def start_requests(self):
        yield scrapy.Request('http://ve.mofcom.gov.cn/article/slfw/', self.parse)

    def parse(self, response):
        selector = Selector(response)
        item = PDFItem()
        menus = selector.xpath('//div[@class="navi"]/ul/li')
        urls = menus.xpath(".//a/@href").extract()
        for i in range(len(urls)):
            if ".pdf" in urls[i]:
                print urls[i].encode('utf-8')
                item['file_urls'] = [urls[i]]
                yield item