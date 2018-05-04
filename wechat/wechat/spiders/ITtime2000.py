#coding:utf-8
#@author:hya
#time:2018-04-26

import scrapy
from scrapy import Request
from ..items import WechatItem
from scrapy.selector import Selector

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import chardet

class QQchuangye(scrapy.Spider):
    name = "itime"
    allowed_domains = ['weixin.sogou.com']
    start_urls = ['http://weixin.sogou.com/weixin?type=1&s_from=input&query=ITtime2000',
                  'http://weixin.sogou.com/weixin?type=1&s_from=input&query=qqchuangye',
                  'http://weixin.sogou.com/weixin?type=1&s_from=input&query=python6359'
                 ]

    def parse(self, response):
        print "url:"+response.url
        print "response:"+response.__str__()

        list_url = response.xpath('//div[@class="news-box"]/ul[@class="news-list2"]/li[1]/div[@class="gzh-box2"]/div[@class="img-box"]/a/@href').extract()
        print "list_url:***"+list_url.__str__()
        if list_url:
            yield Request(list_url[0], callback=self.parse_list, dont_filter=True)
        else:
            print "***********"
    def parse_list(self, response):
        item = WechatItem()
        selector = Selector(response)
        print "response:"+response.__str__()
        article_srcs = response.xpath("//div[@class='profile_info']/strong[@class='profile_nickname']/text()").extract()
        print article_srcs[0].strip()

        titles = selector.xpath('//*[@id="history"]/div/div[@class="weui_msg_card_bd"]/div[@class="weui_media_box appmsg"]/div[@class="weui_media_bd"]')
        i = 1
        for each_title in titles:
            print i
            i = i+1
            name = each_title.xpath('h4/text()').extract()[0]
            time = each_title.xpath('p[@class="weui_media_extra_info"]/text()').extract()[0]
            #summary = each_title.xpath('p[@class="weui_media_desc"]/text()').extract()[0]
            print "[[[[[[[[["
            print name.strip().encode('utf-8')
            print time.strip().encode('utf-8')
            #print summary.strip().encode('utf-8')
            print "]]]]]]]]]"
            item['name'] = name
            item['time'] = time
            #item['summary'] = summary 
            yield item
