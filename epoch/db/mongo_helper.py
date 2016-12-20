
import pymongo

from epoch.config import DB_CONFIG
from epoch.db.sqlhelper import SqlHelper


class MongoHelper(SqlHelper):

    def __init__(self):
        self.client = pymongo.MongoClient(host=DB_CONFIG["HOST"], port=DB_CONFIG["PORT"])
        self.db = self.client[DB_CONFIG["DB"]]
        self.collection = self.db[DB_CONFIG["INFO"]]

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        if value:
            self.collection.insert(value)
            return True
        else:
            return False

    def delete(self, conditions=None):
        if conditions:
            self.collection.remove(conditions)
            return {'deleteNum': 'ok'}
        else:
            return {'deleteNum': 'None'}

    def update(self, conditions=None, value=None):
        if conditions and value:
            self.collection.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def find(self, conditions=None):
        items = self.collection.find(conditions)
        results = []
        for item in items:
            result = (item['ip'], item['port'], item['protocol'])
            results.append(result)
        return results

    def close(self):
        if self.client:
            self.client.close()
