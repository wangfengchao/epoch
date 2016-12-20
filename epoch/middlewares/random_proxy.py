# -*- coding: utf-8 -*-
import random

import pymongo
from epoch.config import DB_CONFIG

'''
这个类主要用于产生随机代理
'''


class RandomProxy(object):

    def __init__(self):
        client = pymongo.MongoClient(host=DB_CONFIG["HOST"], port=DB_CONFIG["PORT"])
        db = client[DB_CONFIG["DB"]]
        self.collection = db[DB_CONFIG["INFO"]]
        self.count = self.collection.count()

    def process_request(self, request, spider):
        idList = range(1, self.count + 1)
        id = random.choice(idList)
        results = self.collection.find({'proxyId': id})
        if results:
            for result in results:
                HTTP_PROXY = 'http://' + result['ip'] + ':' + result['port']
                request.meta['proxy'] = HTTP_PROXY