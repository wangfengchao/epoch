# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from w3lib.html import remove_tags


def filter_price(value):
    if value.isdigit():
        return value


class Product(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )

    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_price,float),
        output_processor=TakeFirst(),
    )

    # Housekeeping fields，这些字段用来在调试时显示相关信息
    url = scrapy.Field()
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    date = scrapy.Field()
    links = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join()
    )