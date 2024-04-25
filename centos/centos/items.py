# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CentosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    URL = scrapy.Field()
    Title = scrapy.Field()
    User = scrapy.Field()
    UserUrl = scrapy.Field()
    Date = scrapy.Field()
    Posts = scrapy.Field()
    Joined = scrapy.Field()
    # name = scrapy.Field()

    pass
