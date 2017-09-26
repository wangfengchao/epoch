# -*- coding: utf-8 -*-

import scrapy


class ZhugefangItem(scrapy.Item):
    """
    诸葛找房二手房房源爬取信息定义
    """
    houseTitle = scrapy.Field()        # 房源标题
    sellPrice = scrapy.Field()         # 售价
    unitPrice = scrapy.Field()         # 每平米价格
    downPaymentPrice = scrapy.Field()  # 首付价
    houseType = scrapy.Field()         # 户型
    floor = scrapy.Field()             # 楼层
    floorType = scrapy.Field()         # 楼型
    orientation = scrapy.Field()       # 朝向 1.东 2.南，3.西 4.北 5.西南 6.东南 7.东北 8.西北 9.南北
    renovation = scrapy.Field()        # 1 空房，2 简装，3 中装，4 精装，5 豪装
    buildingAge = scrapy.Field()       # 建造年代
    propertyRight = scrapy.Field()     # 产权年限
    externalEstateName = scrapy.Field()  # 外部小区名称
    externalHouseId = scrapy.Field()   # 外部房源houseId
    pageUrl = scrapy.Field()           # 外部房源网页url
    picNum = scrapy.Field()            # 有效图片数
    image_urls = scrapy.Field()        # 图片地址
    elevator = scrapy.Field()          # 是否有电梯 0 没有  1 有
    metroInfo = scrapy.Field()         # 地铁描述
    houseBabel = scrapy.Field()        # 房屋标签
    spiderSource = scrapy.Field()      # 爬取来源：1. 诸葛找房
    agentList = scrapy.Field()         # 经纪人列表