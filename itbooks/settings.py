# -*- coding: utf-8 -*-
BOT_NAME = 'itbooks'
SPIDER_MODULES = ['itbooks.spiders']
NEWSPIDER_MODULE = 'itbooks.spiders'
# define our database through a dictionary
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'liaobaocheng',
    'password': 'liaobaocheng',
    'database': 'cssbookss'
}
# add item_pipeline
ITEM_PIPELINES = {'itbooks.pipelines.ItbooksPipeline': 400}
ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline':1}
FILES_STORE = '/home/liaobaocheng/Downloads/CSS_Download'