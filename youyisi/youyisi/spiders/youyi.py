# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import re
from youyisi.items import *

class YouyiSpider(CrawlSpider):
    name = 'youyi'
    allowed_domains = ['www.u148.net']
    start_urls = ['http://www.u148.net/']

    rules = (

        Rule(LinkExtractor(allow=('/.*?/'),restrict_xpaths=('//div[@class="menu"]/a')), callback='parse_item', follow=True),
        #设定匹配规则爬全站网页    匹配class为menu的div下面的a的链接,然后一层层的请求,再回调函数
        Rule(LinkExtractor(allow=('/.*?/\d+'),restrict_xpaths=('//div[@class="pageli"]/a')), callback = 'parse_page', follow = True),

        Rule(LinkExtractor(allow=('/article/\d+.html'),),callback='parse_detail',)

    )

    def parse_item(self, response):

        i = {}

         #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
    def parse_page(self, response):        #匹配分页
        print(response.url)
    def parse_detail(self, response):
        item = YouyisiItem()             #创建一个item类的对象
        item['title'] = response.xpath('//div[@class="content"]/h1/a/text()').extract()   #匹配标题
        content = response.xpath('//div[@class="contents"]/p//text()').extract()      #匹配内容
        text = ''         #发现匹配的内容里有一些换行符之类的,要用条件给他去掉
        for i in content:     #遍历获取到的内容
            if i == '\xa0':   #如果内容是换行符,那么就去掉
                pass
            else:              #否则就加到一起
                text = text+i

        item['img'] = response.xpath('//div[@class="contents"]/p/a[@class="img"]/img/@src|//div[@class="contents"]/p/img/@src|//div[@class="contents"]/div/img/@src').extract()
        item['name'] = response.xpath('//div[@class="article-info"]/a[@target="_blank"]/text()|//div[@class="article-info"]/a[5]/text()').extract()
        item['text'] = text
        yield item       #然后在返回给pipelines保存数据
