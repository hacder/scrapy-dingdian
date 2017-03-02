# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # 小说名
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 小说网址
    novelurl = scrapy.Field()
    # 小说状态
    serialstatus = scrapy.Field()
    # 字数
    textnumber = scrapy.Field()
    # 类型
    category = scrapy.Field()
    # 小说编号
    name_id = scrapy.Field()


class DcontentItem(scrapy.Item):

    # 小说编号
    id_name = scrapy.Field()
    # 章节内容
    chaptercontent = scrapy.Field()
    # 用于绑定章节顺序
    num = scrapy.Field()
    # 章节地址
    chapterurl = scrapy.Field()
    # 章节名
    chaptername = scrapy.Field()
