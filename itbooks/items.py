# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ItbooksItem(Item):
    # 一级信息
    title = Field()  # 书名
    author = Field()  # 作者
    image = Field()  # 封面
    url = Field()  # 跳转链接
    # 二级信息， 请求url后再次提取信息
    isbn = Field()  # isbn号
    year = Field()  # 出版日期
    pages = Field()  # 页码数
    file_size = Field()  # 文件大小
    category = Field()  # 所属分类
    category_url = Field()  # 分类链接
    description = Field()  # 简述
    download = Field()  # 下载链接
    files = Field() #为了pipeline
    file_urls = Field()
