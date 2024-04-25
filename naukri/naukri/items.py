# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaukriItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name= scrapy.Field()
    Experience= scrapy.Field()
    Salary= scrapy.Field()
    City= scrapy.Field()
    Title= scrapy.Field()
    Views= scrapy.Field()
    Downloads= scrapy.Field()
    ModifiedOn= scrapy.Field()
    Active= scrapy.Field()
    pass
