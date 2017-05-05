import pika, sys
from pymongo import MongoClient

class Mongo(object):

    def __init__(self, ip, port, db):
        client = MongoClient(ip, int(port))
        self.db = client[db]

    def insert(self, collection_name, item):
        try:
            collection = self.db[collection_name]
            collection.insert(item)
            return True
        except Exception as exception:
            print exception
            return False

    def find(self, collection_name, condition):
        try:
            collection = self.db[collection_name]
            items = collection.find(condition)
            return items
        except Exception as exception:
            print exception
            return False

    # def create_index(self, collection_name, index_name, unique):
        