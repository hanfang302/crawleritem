# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import pymongo
class YouyisiPipeline(object):                          #12到38行这是保存到本地文件夹,需要更改下路径
    def process_item(self, item, spider):
        qudiao = str(item['title'][0]).strip()      #保存到本地需要设定文件夹名字为标题
                                                    #但是我发现获取到的标题有空格,一保存就报错,需要把两端的空格去掉
        pathh = "/home/bc/桌面/有意思/" + qudiao      #设定路径
        if not os.path.exists(pathh):               #判断有没有这个路径,如果有就不创建,没有就创建
            os.mkdir(pathh, 0o755)
        else:
            print('存在了就不创建了')
        a = open(pathh+'/'+item['title'][0]+'.txt','a')  #创建文件名字为标题的文件,因为item['title']是一个列表,所以要取索引
        zz = '作者:'+item['name'][0]+'\n'+'\n'+item['text']+'\n'  #把内容加到一起,保存到文件里
        a.write(zz)

        # for i in item['img']:    #然后是保存图片
        #     print(i)
        #     zf = i[-3:]         #取图片链接的后三位
        #     print(zf)
        #     if zf == 'jpg':     #如果等于jpg，就保存到
        #         houzhui = '.jpeg'
        #     else:
        #         continue        #否则就跳过这次循环
        #     pathh2 = pathh+'/'+str(item['img'].index(i))+houzhui   #这是拼接路径加文件名字
        #
        #     a = requests.get(i)   #请求这个网页，获取相应
        #
        #     c = open(pathh2,'wb')   #以二进制响应保存到本地
        #     c.write(a.content)
        # a.close()3

        client = pymongo.MongoClient('localhost', 27017)   #这是保存到mongodb数据库
        db = client.youyisi
        biao = db.yisi
        biao.insert(dict(item))

