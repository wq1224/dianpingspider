# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shopname = Field()
    shoplevel = Field()
    shopurl = Field()
    commentnum = Field()
    avgcost = Field()
    taste = Field()
    envi = Field()
    service = Field()
    foodtype = Field()
    loc = Field()
