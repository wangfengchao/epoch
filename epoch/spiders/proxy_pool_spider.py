# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy import Selector
from scrapy.loader import ItemLoader

from epoch.items.ip_proxy_items import IPProxyItem
from epoch.thread.detect_manager import Detect_Manager


class ProxyPoolSpider(scrapy.Spider):
    name = "proxyPool"
    allowed_domains = ["youdaili.net"]
    # detecter = Detect_Manager(5)
    # detecter.start()

    def start_requests(self):
        yield scrapy.Request("http://www.youdaili.net/Daili/guonei/24535.html", self.parse)

    def parse(self, response):
        selector = Selector(response)
        lines = selector.xpath("//div[@class=\"content\"]/p/span/text()").extract()
        for line in lines:
            line_record = line.split("@")
            if len(line_record) == 2:
                ip_info = line_record[0].split(":")
                addr_info = line_record[1].split("#")[1]
                ip = ip_info[0]
                port = ip_info[1]
                if detect(ip, port):
                    item = ItemLoader(item=IPProxyItem(), response=response)
                    item.add_value("ip", ip)
                    item.add_value("port", port)
                    item.add_value("alive", True)
                    item.add_value("addr", [addr_info])
                    yield item.load_item()
            else:
                print 'line_record size != 2'


def detect(*args):
    '''
    验证ip是否可用
     http://ip.chinaz.com/getip.aspx  作为检测目标
    :param args:
    :return:
    '''
    try:
        verify_url = "http://ip.chinaz.com/getip.aspx"
        proxy_host = "http://" + args[0] + ":" + args[1]
        response = urllib.urlopen(verify_url, proxies={"http": proxy_host})
        if response.getcode() == 200:
            return True
        else:
            return False
    except Exception, e:
        print proxy_host, 'bad proxy'
        return False
