# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import scrapy
from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request
from itbooks.items import ItbooksItem


class EasySpider(CrawlSpider):
    # name = 'itbook'
    # allowed_domains = ['allitebooks.com']
    #
    # start_urls = (
    #     'http://www.allitebooks.com/page/506',
    # )
    # current_page = 0
    # # 规则
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//span[@class="current"]'), callback="next_page"),  # 翻页规则
    #     Rule(LinkExtractor(restrict_xpaths='//*[@rel="bookmark"]'), callback='parse_item')  # 本页规则
    # )
    #
    # def start_requests(self):
    #     reqs = []
    #     for i in range(1, 603):
    #         req = scrapy.Request("http://www.allitebooks.com/page/%s" % i)
    #         reqs.append(req)
    #     return reqs
    #
    # def next_page(self, page):
    #     next_url = int(page) + 1
    #     url = "http://www.allitebooks.com/page/%s" % next_url
    #     return url

    ################################### 以上是爬取全站的代码 ##############################################################


    #################################### 接下来是爬取css特定页面的代码 #####################################################
    name = 'itbook'
    allowed_domains = ['allitebooks.com']

    start_urls = (
        'http://www.allitebooks.com/page/1/?s=css',
    )
    current_page = 0
    # 规则
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//span[@class="current"]'), callback="next_page"),  # 翻页规则
        Rule(LinkExtractor(restrict_xpaths='//*[@rel="bookmark"]'), callback='parse_item')  # 本页规则
    )

    def start_requests(self):
        reqs = []
        for i in range(1, 10):
            req = scrapy.Request("http://www.allitebooks.com/page/%s/?s=css" % i)
            reqs.append(req)
        return reqs

    def next_page(self, page):
        next_url = int(page) + 1
        url = "http://www.allitebooks.com/page/%s/?s=css" % next_url
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
        l.add_xpath('title', '//h1[@class="single-title"]/text()',
                    MapCompose(unicode.strip, unicode.title))  # //h1[@class="single-title"]
        l.add_xpath('author', '//dl/dd/a[@rel="tag"]/text()')  # //dl/dd/a[@rel="tag"]
        l.add_xpath('image',
                    '(//img[contains(@src,"http")]/@src)[1]')  # //div[@class="entry-body-thumbnail hover-thumb"]/a/img["src"]
        l.add_value('url', response.url)  # response.url
        l.add_xpath("isbn", '//dl/dd[2]/text()', MapCompose(unicode.strip))  # //dl/dd[2]
        l.add_xpath('year', '//dl/dd[3]/text()', MapCompose(lambda i: i.replace(' ', '')))  # //dl/dd[3]
        l.add_xpath('pages', '//dl/dd[4]/text()', MapCompose(unicode.strip))  # //dl/dd[4]
        l.add_xpath('file_size', '//dl/dd[6]/text()', MapCompose(unicode.strip))  # //dl/dd[6]
        l.add_xpath('category', '//dl/dd[8]/a/text()')  # //dl/dd[8]
        l.add_xpath('category_url', '//dl/dd[8]/a/@href')  # //dl/dd[8]
        l.add_xpath('description', '//div[@class="entry-content"]/p/text()', MapCompose(unicode.strip),
                    Join())  # //div[@class="entry-content"]/p
        l.add_xpath('download',
                    '//span[@class="download-links"]/a[contains(@href,"http://file.allitebooks.com")]/@href')  # //span[@class="download-links"]/a[contains(@href,"http://file.allitebooks.com")]
        l.add_xpath('file_urls','//span[@class="download-links"]/a[contains(@href,"http://file.allitebooks.com")]/@href')
        return l.load_item()
