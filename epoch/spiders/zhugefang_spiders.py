# -*- coding: utf-8 -*-
# @Time    : 2017/9/26 17:24
# @Author  : fc.w

from urlparse import urljoin

import scrapy
import os
import urllib
from scrapy import Selector
from selenium import webdriver
from epoch.items.zhugefang_item import ZhugefangItem
from scrapy.loader import ItemLoader

from epoch.config import PHANTOMJS, IMG_INFO


class ZhugefangSpidersSpider(scrapy.Spider):
    """
    爬取诸葛找房  二手房详情页信息
    """
    name = 'zhugefang_spiders'
    allowed_domains = ['zhugefang.com']

    def start_requests(self):
        yield scrapy.Request('http://sh.zhugefang.com/list/', self.house_parse)

    def house_parse(self, response):
        """
        解析二手房列表页
        :param response:
        :return:
        """
        for li in response.selector.xpath('//ul/li'):
            house_detail_url = 'http://sh.zhugefang.com' + li.xpath('.//a/@href')[0].extract()
            try:
                request = scrapy.Request(house_detail_url, callback=self.house_detail_parse)
                yield request
            except Exception, e:
                print 'ERROR: ', e
                continue

        # 是否还有下一页，如果有的话，则继续
        selector = Selector(response)
        next_pages = selector.xpath('//div[@class="laypage-main"]/a[@class="laypage-next"]/@href')
        if next_pages:
            next_page = urljoin('http://sh.zhugefang.com/list/', next_pages[0].extract())
            print next_pages
            # 将 「下一页」的链接传递给自身，并重新分析
            yield scrapy.Request(next_page, callback=self.house_parse)

    def house_detail_parse(self, response):
        """
        解析二手房详情页信息
        :param response:
        :return:
        """

        try:
            item = ItemLoader(item=ZhugefangItem(), response=response)
            selector = Selector(response)
            pageUrl = response.url
            item.add_value("pageUrl", pageUrl)
            item.add_value("houseTitle", selector.xpath('//div[@class="detail-header"]/h2/strong[@title]/text()').extract())
            item.add_value("sellPrice", selector.xpath('//div[@class="price-box"]/h2/text()').extract())
            item.add_value("houseType", selector.xpath('//div[@class="house-type"]/div/h2/text()').extract())
            # 房屋详情
            item.add_value("unitPrice", selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[0].extract())
            item.add_value("downPaymentPrice", selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[1].extract())
            item.add_value("floor", selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[2].extract())
            item.add_value("floorType",  selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[5].extract())
            item.add_value("buildingAge", selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[6].extract())
            item.add_value("propertyRight", selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[7].extract())
            # 房屋朝向
            # 户型朝向：1.东 2.南，3.西 4.北 5.西南 6.东南 7.东北 8.西北 9.南北
            house_orientation = {'东': 1, '南': 2, '西': 3, '北': 4, '西南': 5, '东南': 6, '东北': 7, '西北': 8, '南北': 9}
            house_orientation_str = selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[3].extract()
            ori_num = 0
            if house_orientation.get(str(house_orientation_str).strip()):
                ori_num = house_orientation.get(str(house_orientation_str).strip())
            item.add_value("orientation", ori_num)

            # 装修 1 空房，2 简装，3 中装，4 精装，5 豪装
            renovation_type = {'空房': 1, '简装修': 2, '中装修': 3, '精装修': 4, '豪装修': 5}
            renovation_str = selector.xpath('//ul[@class="ul-houseDetail"]/li/text()')[4].extract()
            renovation_num = 0
            if renovation_type.get(str(renovation_str).strip()):
                renovation_num = renovation_type.get(str(renovation_str).strip())
            item.add_value("renovation", renovation_num)

            # 地铁特色
            metroInfo = selector.xpath('//ul[@class="ul-houseDetail"]/li[@class="col-12"]/text()').extract()
            metroList = []
            print len(metroInfo)
            for i in range(len(metroInfo)):
                if metroInfo[i].strip() != '':
                    metroList.append(metroInfo[i].replace('\n', '').replace(' ', '').strip())
            item.add_value("metroInfo", metroList[0])

            # 房屋特色(标签)
            house_label = selector.xpath('//ul[@class="ul-houseDetail"]/li[@class="col-12"]/label[@class="feature-label"]/text()').extract()
            label_list = []
            for i in range(len(house_label)):
                label_list.append(house_label[i])
            house_label_str = ""
            if len(label_list) > 0:
                house_label_str = (",".join(label_list[i].strip() for i in range(len(label_list))))
            item.add_value("houseBabel", house_label_str)

            # 小区信息
            item.add_value("externalEstateName", selector.xpath('//ul[@class="ul-houseDetail"]/li[@class="col-12"]/a/text()').extract())
            item.add_value("externalHouseId", selector.xpath('//ul[@class="ul-houseDetail"]/li[@class="col-12"]/a/@href').extract()[0].split("?house_id=")[1])

            # 经纪人列表
            driver = webdriver.PhantomJS(PHANTOMJS['phantomjs.home'])
            driver.get(pageUrl)
            driver.find_element_by_id('viewBroker').click()
            body = driver.page_source
            agent_list = ''
            for agent in Selector(text=body).xpath('//div[@id="brokerList"]/div[@class="broker-main"]/ul[@class="broker-list m-auto"]/li/div/h3/text()').extract():
                agent_list += agent + ','
            item.add_value("agentList", agent_list)

            # 房源图片下载
            src_items = selector.xpath('//div[@class="carousel-detail"]/img//@src')
            img_urls = []
            for i in range(len(src_items)):
                src = src_items[i].extract()  # 提取图片链接
                if src:
                    house_id = selector.xpath('//ul[@class="ul-houseDetail"]/li[@class="col-12"]/a/@href').extract()[0].split("?house_id=")[1]
                    file_name = "%s_%s.jpg" % (house_id, i)          # 拼接文件名，houseID_序号
                    img_urls.append(file_name)
                    file_path = os.path.join(IMG_INFO['img_save_dir'], file_name)  # 拼接这个图片的路径
                    urllib.urlretrieve(src, file_path)               # 接收文件路径和需要保存的路径，会自动去文件路径下载并保存到指定的本地路径
            item.add_value("picNum", len(img_urls))

            image_path = ""
            if len(img_urls) > 0:
                image_path = (",".join(img_urls[i] for i in range(len(img_urls))))
            item.add_value("image_urls", image_path)
            item.add_value("spiderSource", 1)
            item.add_value("elevator", 0)

            yield item.load_item()

        except Exception, e:
            print 'ERROR: ', e