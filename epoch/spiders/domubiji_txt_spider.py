# -*- coding: utf-8 -*-
import scrapy as scrapy
from scrapy import Selector

from epoch.items.domubiji_txt_items import DaomubijiItem


class DomubijiSpider(scrapy.Spider):
    name = "daomubiji_txt"
    allowed_domains = ["seputu.com"]

    def start_requests(self):
        yield scrapy.Request('http://seputu.com//', self.parse)

    """
    解析小说章节和url
    """
    def parse(self, response):
        selector = Selector(response)
        mulus = selector.xpath("//div[@class=\"mulu\"]/div[@class=\"mulu-title\"]/center/h2/text()").extract()
        boxs = selector.xpath("//div[@class=\"mulu\"]/div[@class=\"box\"]")
        for i in range(len(mulus)):
            mulu = mulus[i]
            box = boxs[i]
            texts = box.xpath(".//ul/li/a/text()").extract()
            urls = box.xpath(".//ul/li/a/@href").extract()
            for j in range(len(urls)):
                item = DaomubijiItem()
                item["bookName"] = mulu
                try:
                    item["bookTitle"] = texts[j].split(' ')[0]
                    item['chapterNum'] = texts[j].split(' ')[1]
                    item['chapterName'] = texts[j].split(' ')[2]
                    item['chapterUrl'] = urls[j]
                    request = scrapy.Request(urls[j], callback=self.parseBody)
                    request.meta['item'] = item
                    yield request

                except Exception, e:
                    print 'exception', e
                    continue

    '''
     解析小说章节中的内容
    '''
    def parseBody(self, response):
        item = response.meta['item']
        selector = Selector(response)
        item['chapterContent'] = '\r\n'.join(selector.xpath('//div[@class="content-body"]/p/text()').extract())
        yield item

