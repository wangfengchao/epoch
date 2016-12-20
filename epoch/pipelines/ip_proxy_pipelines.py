# -*- coding: utf-8 -*-
from epoch.db.mongo_helper import MongoHelper


class IPProxyPipelines(object):

    proxyId = 1  # 设置一个ID号，方便多线程验证

    def process_item(self, item, spider):
        connection = MongoHelper()
        new_proxy = {
            "ip": item['ip'][0],
            "port": item['port'][0],
            "proxyId": self.proxyId,
            "alive": item["alive"][0],
            "addr": item["addr"][0]
        }

        if connection.insert(new_proxy):
            self.proxyId += 1
        return item