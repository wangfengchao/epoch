# -*- coding: utf-8 -*-

import pymysql
from sqlalchemy.dialects.mysql import DOUBLE

from epoch.db.ISqlHelper import ISqlHelper
from sqlalchemy import Column, Integer, create_engine, VARCHAR
from sqlalchemy.orm import sessionmaker
from epoch.config import DB_CONFIG
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'fc.w'

pymysql.install_as_MySQLdb()
BaseModel = declarative_base()


class ZhugeModel(BaseModel):
    """
    数据结构化
    """
    __tablename__ = 'zhuge_spider'
    id = Column(Integer, primary_key=True,  nullable=False)
    houseTitle = Column(VARCHAR(50), nullable=True)   # 房源标题
    sellPrice = Column(DOUBLE, nullable=True)   # 售价
    unitPrice = Column(DOUBLE, nullable=True)        # 每平米价格
    downPaymentPrice = Column(DOUBLE, nullable=True)  # 首付价
    houseType = Column(VARCHAR(20), nullable=True)        # 户型
    floor = Column(VARCHAR(20), nullable=True)            # 楼层
    floorType = Column(VARCHAR(20), nullable=True)        # 楼型
    orientation = Column(Integer, nullable=True)      # 朝向 1.东 2.南，3.西 4.北 5.西南 6.东南 7.东北 8.西北 9.南北
    renovation = Column(Integer, nullable=True)       # 1 空房，2 简装，3 中装，4 精装，5 豪装
    buildingAge = Column(VARCHAR(20), nullable=True)       # 建造年代
    propertyRight = Column(VARCHAR(20), nullable=True)     # 产权年限
    externalEstateName = Column(VARCHAR(50), nullable=True)  # 外部小区名称
    externalHouseId = Column(VARCHAR(20), nullable=True)   # 外部房源houseId
    pageUrl = Column(VARCHAR(100), nullable=True)           # 外部房源网页url
    picNum = Column(Integer, nullable=True)            # 有效图片数
    image_urls = Column(VARCHAR(50), nullable=True)        # 图片地址
    elevator = Column(Integer, nullable=True)          # 是否有电梯 0 没有  1 有
    metroInfo = Column(VARCHAR(255), nullable=True)         # 地铁描述
    houseBabel = Column(VARCHAR(255), nullable=True)      # 房屋标签
    spiderSource = Column(Integer, nullable=True)  # 爬取来源：1. 诸葛找房
    agentList = Column(VARCHAR(255), nullable=True)  # 经纪人列表


class MySqlHelper(ISqlHelper):
    """
    sql操作的基类
    """

    def __init__(self):
        self.engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'], echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

    def insert(self, value=None):
        if value:
            record = ZhugeModel(houseTitle=value['houseTitle'], sellPrice=value['sellPrice'], unitPrice=value['unitPrice'], downPaymentPrice=value['downPaymentPrice'],
                                houseType=value['houseType'], floor=value['floor'], floorType=value['floorType'], orientation=value['orientation'], renovation=value['renovation'],
                                buildingAge=value['buildingAge'], propertyRight=value['propertyRight'], externalEstateName=value['externalEstateName'], externalHouseId=value['externalHouseId'],
                                pageUrl=value['pageUrl'], picNum=value['picNum'],image_urls=value['image_urls'], elevator=value['elevator'], metroInfo=value['metroInfo'],
                                houseBabel=value['houseBabel'], spiderSource=value['spiderSource'], agentList=value['agentList'])
            self.session.add(record)
            self.session.commit()
            return True
        else:
            return False



# if __name__ == '__main__':
#     sqlhelper = MySqlHelper()
#     sqlhelper.init_db()
#     proxy = {'ip': '192.168.1.1', 'port': 80}
#     sqlhelper.insert(proxy)


