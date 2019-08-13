# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaocheRedisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pic = scrapy.Field()  # 图片
    title = scrapy.Field()  # 标题
    price = scrapy.Field()  # 价格
    detail_url = scrapy.Field()  # 详情页url
    source_id = scrapy.Field()  # 车源号
    pic_list = scrapy.Field()  # 详情页图片列表
    regist_date = scrapy.Field()  # 注册日期
    ckg = scrapy.Field()  # 长宽高
