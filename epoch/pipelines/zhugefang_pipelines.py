# -*- coding: utf-8 -*-
# @Time    : 2017/9/26 17:24
# @Author  : fc.w
# @File    : zhugefang_pipelines.py

from epoch.db.MySqlHelper import MySqlHelper


class ZhugefangPipeline(object):

    proxyId = 1  # 设置一个ID号，方便多线程验证

    def process_item(self, item, spider):
        conn = MySqlHelper()
        zhugeModel = {
            "houseTitle": item['houseTitle'][0],  # 房源标题
            "sellPrice": item['sellPrice'][0],  # 售价
            "unitPrice": item['unitPrice'][0],  # 每平米价格
            "downPaymentPrice": item['downPaymentPrice'][0],  # 首付价
            "houseType": item['houseType'][0],  # 户型
            "floor": item['floor'][0],  # 楼层
            "floorType": item['floorType'][0],  # 楼型
            "orientation": item['orientation'][0],  # 朝向 1.东 2.南，3.西 4.北 5.西南 6.东南 7.东北 8.西北 9.南北
            "renovation": item['renovation'][0],  # 1 空房，2 简装，3 中装，4 精装，5 豪装
            "buildingAge": item['buildingAge'][0],  # 建造年代
            "propertyRight": item['propertyRight'][0],  # 产权年限
            "externalEstateName": item['externalEstateName'][0],  # 外部小区名称
            "externalHouseId": item['externalHouseId'][0],  # 外部房源houseId
            "pageUrl": item['pageUrl'][0],  # 外部房源网页url
            "picNum": item['picNum'][0],  # 有效图片数
            "image_urls": item['image_urls'][0],  # 图片地址
            "elevator": item['elevator'][0],  # 是否有电梯 0 没有  1 有
            "metroInfo": item['metroInfo'][0],  # 地铁描述
            "houseBabel": item['houseBabel'][0],  # 房屋标签
            "spiderSource": item['spiderSource'][0],  # 爬取来源：1. 诸葛找房
            "agentList": item['agentList'][0]  # 经纪人列表
        }

        if (conn.insert(zhugeModel)):
            self.proxyId += 1
        return item
