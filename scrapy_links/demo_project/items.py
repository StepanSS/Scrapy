# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def remove_whitespace(value):
    return value.strip()

class JokesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    joke_text = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )

class LinkScraperItem(scrapy.Item):
    main_headline = scrapy.Field()
    link = scrapy.Field()
    url = scrapy.Field()
    project = scrapy.Field()
    spider = scrapy.Field()