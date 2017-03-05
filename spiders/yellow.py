#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,re
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

from .. import items


emptyLink = []
# saveLink = []
# lastLinkPattem = re.compile(ur'\<li class\=\"title\"\>([^\w]+)\<\/li\>.*\"(\/\w+\/\w+\/\d+.\d+\/\d+\/\w+\.mp4)\"', re.S)

class huangwang(scrapy.Spider):
    name = 'huangwang'
    # download_delay = 1
    start_urls = ['https://www.susu57.com/htm/movielist1/index.htm']
    allowed_urls = ['susu57.com']

    def parse(self, response):
        for x in response.xpath("/html/body/div/div/ul/li/a/@href").extract():
            x =  'https://www.susu57.com/' + x
            yield scrapy.Request(x,callback=self.findAndprint)

        pageLink = response.xpath("/html/body/div/div/div/div/a/@href").extract()
        nextLink =  'https://www.susu57.com/' + pageLink[-2]
        # saveLink.append(nextLink)
        if nextLink not in emptyLink:
            yield scrapy.Request(nextLink,callback=self.parse)
        else:
            print 'list is already in list'
            pass

    def findAndprint(self,response):
        item = items.yellow()
        item['Vname'] = response.selector.xpath("//title/text()").extract()[0]
        item['Vurl'] =  re.findall(ur'GvodUrls \= codeUrl\(movieurl_24k_2\+\"(.*?.mp4)\"\)',response.xpath("//div [@class='ndownlist']/script").extract()[1])[0]
        yield item

        with open('urlAll.txt','a') as fileName:

            fileName.write('《'+str(item['Vname'])+'》'+'->http://m.123456xia.com:888'+str(item['Vurl'])+'\n')
        print '####################成功获取\n'


# run = huangwang()
# run.parse()
