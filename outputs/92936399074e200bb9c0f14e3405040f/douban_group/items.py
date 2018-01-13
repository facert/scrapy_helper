
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopicItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    create_time = scrapy.Field()
    image_urls = scrapy.Field()
