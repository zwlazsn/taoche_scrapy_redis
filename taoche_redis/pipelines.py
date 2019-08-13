# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class TaocheRedisPipeline(object):
    def process_item(self, item, spider):
        return item


class PymongoPipeline(object):

    #链接mongodb
    # def __init__(self):
    #     self.MONGODB_HOST = settings['MONGODB_HOST']
    #     self.MONGODB_PORT = settings['MONGODB_PORT']
    #     self.MONGODB_DB = settings['MONGODB_DB']
    #     # 创建连接
    #     conn = pymongo.MongoClient(host=self.MONGODB_HOST, port=self.MONGODB_PORT)
    #     # 连接数据库
    #     db = conn[self.MONGODB_DB]
    #     # 创建表
    #     self.colltection = db[RenrenspiderslaveItem.collection]
    #
    # def process_item(self, item, spider):
    #     # 使用id去定位数据库中是否有此数据,如果没有就添加数据.如果已经存在就更新数据
    #     self.colltection.update({'id': item['id']}, {'$set': item}, True)
    #     return item
    def __init__(self):
        self.count = 1
        self.db= self.conn_mongo()

    def conn_mongo(self):
        client = pymongo.MongoClient(host="localhost",port=27017)
        print(client)
        return client.taoche

    def process_item(self, item, spider):
        # print(self.count,item)
        self.db.taoche.insert(dict(item))
        self.count+=1
        return item
