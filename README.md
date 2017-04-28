# 项目说明
- 使用scrapy1.0
- 使用postgres作为数据库
- 使用pycharm为开发工具
- ubuntu系统

# 代码部分
```
$ scrapy startproject itbooks
$ cd itbooks
$ scrapy genspider -t crawl easy itbook
$ scrapy crawl itbook -o filename.extension
#######################
├── itbooks
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── items.py
│   ├── items.pyc
│   ├── models.py
│   ├── models.pyc
│   ├── pipelines.py
│   ├── pipelines.pyc
│   ├── settings.py
│   ├── settings.pyc
│   └── spiders
│       ├── easy.py
│       ├── easy.pyc
│       ├── __init__.py
│       ├── __init__.pyc
│       ├── mybook.py
│       └── mybook.pyc
├── scrapy.cfg

###################################
##########
itbooks/items.py
##########
# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class ItbooksItem(Item):
    # 一级信息
    title = Field() # 书名
    author = Field() # 作者
    image = Field() # 封面
    url = Field() # 跳转链接

    # 二级信息， 请求url后再次提取信息
    isbn = Field() # isbn号
    year = Field() # 出版日期
    pages = Field() # 页码数
    file_size = Field() # 文件大小
    category = Field() # 所属分类
    category_url = Field() # 分类链接
    description = Field() # 简述
    download = Field() # 下载链接

##########
itbooks/spider/easy.py
##########
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request
from itbooks.items import ItbooksItem


class EasySpider(CrawlSpider):
    name = 'itbook'
    allowed_domains = ['allitebooks.com']
    start_urls = (
        'http://www.allitebooks.com/page/506',
    )
    current_page = 0
    # 规则
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//span[@class="current"]'),callback="next_page"), # 翻页规则
        Rule(LinkExtractor(restrict_xpaths='//*[@rel="bookmark"]'),callback='parse_item')  #本页规则
    )

    def start_requests(self):
        reqs = []
        for i in range(1,603):
            req = scrapy.Request("http://www.allitebooks.com/page/%s"%i)
            reqs.append(req)
        return reqs

    def next_page(self,page):
        next_url = int(page) + 1
        url = "http://www.allitebooks.com/page/%s" % next_url
        return url

    def parse_item(self, response):
        """
        检测该页面是否可以爬取。。。
        @url http://www.allitebooks.com
        @returns items 1
        @scrapes title author image url
        """

        l = ItemLoader(item=ItbooksItem(), response=response)

        # 使用xpath寻找信息
        l.add_xpath('title','//h1[@class="single-title"]/text()',MapCompose(unicode.strip, unicode.title)) #//h1[@class="single-title"]
        l.add_xpath('author','//dl/dd/a[@rel="tag"]/text()') # //dl/dd/a[@rel="tag"]
        l.add_xpath('image','(//img[contains(@src,"http")]/@src)[1]') # //div[@class="entry-body-thumbnail hover-thumb"]/a/img["src"]
        l.add_value('url',response.url)  # response.url

        l.add_xpath("isbn",'//dl/dd[2]/text()',MapCompose(unicode.strip)) # //dl/dd[2]
        l.add_xpath('year','//dl/dd[3]/text()',MapCompose(lambda i:i.replace(' ',''))) # //dl/dd[3]
        l.add_xpath('pages','//dl/dd[4]/text()',MapCompose(unicode.strip)) # //dl/dd[4]
        l.add_xpath('file_size','//dl/dd[6]/text()',MapCompose(unicode.strip))  # //dl/dd[6]
        l.add_xpath('category','//dl/dd[8]/a/text()') # //dl/dd[8]
        l.add_xpath('category_url','//dl/dd[8]/a/@href')  # //dl/dd[8]

        l.add_xpath('description','//div[@class="entry-content"]/p/text()',MapCompose(unicode.strip),Join())  #   //div[@class="entry-content"]/p
        l.add_xpath('download','//span[@class="download-links"]/a[contains(@href,"http://file.allitebooks.com")]/@href')   # //span[@class="download-links"]/a[contains(@href,"http://file.allitebooks.com")]

        return l.load_item()


####################
itbooks/models.py
####################
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "allitbooks"

    id = Column(Integer, primary_key = True)
    title = Column('title',String) # 书名
    author = Column('author',String) # 作者
    image = Column('image',String) # 封面
    url = Column('url',String) # 跳转链接

    isbn = Column('isbn',String) # isbn号
    year = Column('year',String) # 出版日期
    pages = Column('pages',String) # 页码数
    file_size = Column('file_size',String) # 文件大小
    category = Column('category',String) # 所属分类
    category_url = Column('category_url',String) # 分类链接
    description = Column('description',String) # 简述
    download = Column('download',String) # 下载链接


#################
itbooks/pipelines.py
#################
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table


class ItbooksPipeline(object):
    """
    pipline for storing scraped items in the database
    """
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item



############################
itbooks/pipelines.py
############################
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table


class ItbooksPipeline(object):
    """
    pipline for storing scraped items in the database
    """
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item



#################
itbooks/settings.py
#################


# -*- coding: utf-8 -*-

BOT_NAME = 'itbooks'

SPIDER_MODULES = ['itbooks.spiders']
NEWSPIDER_MODULE = 'itbooks.spiders'


# define our database through a dictionary
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'balsam',
    'password': 'balsam',
    'database': 'itbooks'
}

# add item_pipeline
ITEM_PIPELINES = {'itbooks.pipelines.ItbooksPipeline': 400}
```

# 2.代码解析
- 1.定义item，声明接下来要从页面中提取的信息（items.py)
- 2.定义spider，网络请求，使用xpath从请求中提取信息(easy.py)
- 3.定义数据库model，使用sqlalchemy为ORM映射工具(models.py)
- 4.定义pipelines，将item，spider，model连接起来(pipelines.py)
- 5.设置settings，将pipeline添加到项目执行过程中，配置数据库（setttings.py)
- 6.运行程序 scrapy crawl itbook

# 运行结果
![最终结果](https://github.com/liaobaocheng/itbooks/blob/master/scrapy_result.png)
总共爬取了5179条数据

# 优化空间
- 1.定时任务
- 2.分布式爬取
- 3.去重爬取
- 4.其他
