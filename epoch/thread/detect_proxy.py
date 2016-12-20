# -*-coding:utf-8 -*-
#
import socket
import urllib
from threading import Thread
import pymongo
from epoch.config import DB_CONFIG

"""
这个类主要是用来检测代理的可用性
"""


class DetectProxy(Thread):

    url = 'http://ip.chinaz.com/getip.aspx'

    def __init__(self, part, threadNum, threadName):
        Thread.__init__(self)
        self.client = pymongo.MongoClient(host=DB_CONFIG["HOST"], port=DB_CONFIG["PORT"])
        self.db = self.client[DB_CONFIG["DB"]]
        self.collection = self.db[DB_CONFIG["INFO"]]
        self.threadName = threadName
        self.threadNum = threadNum
        self.part = part
        self.counts = self.collection.count()
        socket.setdefaulttimeout(2)
        self.__goodNum = 0
        self.__badNum = 0

    def run(self):
        self.detect()

    def detect(self):
        if self.counts < self.threadNum:
            return

        pre = self.counts / self.threadNum
        start = pre * (self.part - 1)
        end = pre * self.part
        if self.part == self.threadNum:
            end = self.counts

        results = self.collection.find({'proxyId': {'$gt': start, '$lte': end}})
        for result in results:
            ip = result['ip']
            port = result['port']
            try:
                proxy_host = "http://" + ip + ":" + port
                response = urllib.urlopen(self.url, proxies={'http': proxy_host})
                if response.getcode() != 200:
                    self.collection.delete_one({'ip': ip, 'port': port})
                    self.__badNum += 1
                    print self.threadName, ' DetectProxy----', proxy_host, 'bad proxy'
                else:
                    self.__goodNum += 1
                    print self.threadName, ' DetectProxy----', proxy_host, 'good proxy'
            except Exception, e:
                print self.threadName, ' DetectProxy----', proxy_host, 'bad proxy'
                self.collection.delete_one({'ip': ip, 'port': port})
                self.__badNum += 1
                continue

    @property
    def getGoodNum(self):
        return self.__goodNum

    @getGoodNum.setter
    def setGoodNum(self, value):
        self.__goodNum = value

    @property
    def getBadNum(self):
        return self.__badNum

    @getBadNum.setter
    def setBadNum(self, value):
        self.__badNum = value




