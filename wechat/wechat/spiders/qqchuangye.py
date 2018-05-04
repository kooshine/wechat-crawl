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
    name = "qqchuangye"
    allowed_domains = ['weixin.sogou.com']
    start_urls = ['http://weixin.sogou.com/weixin?type=1&s_from=input&query=ITtime2000']

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
	times = response.xpath('//div[@id="history"]/div[@class="weui_msg_card"]/div[@class="weui_msg_card_hd"]/text()').extract()
        #name = response.xpath('//*[@id="WXAPPMSG1000000736"]/div/h4/text()').extract()
        names = response.xpath('//*[@id="history"]/div[1]/div[2]/div[2]/div/h4/text()').extract()
        print "********before crawl*********"
        print names[0]
        print "------------"
        #titles = selector.xpath('//*[@id="history"]').extract()
        i = 1
        for each_time in times:
            print i
            tmp = '//*[@id="history"]/div[%d]/div[@class="weui_msg_card_bd"]' %(i)
            i = i+1
            titles = selector.xpath(tmp)
            j = 1
            for each_title in titles:
                print j
                tmp = 'div[%d]/div[@class="weui_media_bd/h4/text()"]' %(j)
                j = j+1
                name = each_title.xpath(tmp).extract()
                print name

            item['time'] = each_time
            #result = chardet.detect(each_time)
            #print result
            print item['time']
            #selector = Selector(response)
            #articles = selector.xpath('//div[@class="weui_media_box appmsg"]/div[@class="weui_media_bd"]/h4/text()').extract()
            
            #titles = response.xpath('//div[@id="history"]/div[@class="weui_msg_card"]/div[@class="weui_msg_card_bd"]/div[@class="weui_media_box appmsg"]').extract()
            #print len(articles)
            #print articles[0].encode('utf-8')
            #print articles[1].encode('gbk')
            #print articles[2].encode('gbk')
            '''j = 0
            for each_title in articles:
                j = j+1
                print each_title
                print j
            '''
