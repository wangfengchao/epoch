# -*- coding: utf-8 -*-
import scrapy

from epoch.items.jiandan_img_items import JiandanItem


class JiandanImgSpider(scrapy.Spider):
    """
    下载图片
    """
    name = 'jiandan_img'
    start_urls = ["http://jandan.net/ooxx"]

    def parse(self, response):
        item = JiandanItem()

        item['image_urls'] = response.xpath('//img//@src').extract()  # 提取图片链接
        yield item
        new_url = response.xpath('//a[@class="previous-comment-page"]//@href').extract_first()  # 翻页
        if new_url:
            yield scrapy.Request(new_url, callback=self.parse)


