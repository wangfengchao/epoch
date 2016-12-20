# -*- coding: utf-8 -*-
import pymongo

from epoch.config import DB_CONFIG
from epoch.db.mongo_helper import MongoHelper


def test_mongo():
    client = pymongo.MongoClient(host=DB_CONFIG["HOST"], port=DB_CONFIG["PORT"])
    db = client[DB_CONFIG["DB"]]
    collection = db[DB_CONFIG["INFO"]]
    print collection.count()
    # client = MongoHelper()
    #
    #
    # try:
    #     new_proxy = {
    #         "ip": '192.168.8.100',
    #         # "port": '27017',
    #         # "protocol": 'aaaa',
    #     }
    #     # client.insert(value=new_proxy)
    #     # client.delete(conditions=new_proxy)
    #     results = client.find(conditions=new_proxy)
    #     print results
    # except Exception, e:
    #     print Exception, ':', e
    # finally:
    #     client.close()


if __name__ == "__main__":
    test_mongo()


