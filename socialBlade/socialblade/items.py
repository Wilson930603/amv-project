# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class SocialbladeItem_facebook(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Brand = Field()
    Website = Field()
    Page_likes = Field()
    Talking_about = Field()
    TotalLikes_monthly = Field()
    TotalTalking_monthly = Field()

class SocialbladeItem_youtube(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Brand = Field()
    Website = Field()
    Uploads = Field()
    Subcribers = Field()
    VideoViews = Field()
    country = Field()
    ChannelType = Field()
    UserCreated = Field()
    subscriberOverTime = Field()
    videoOverTime = Field()
    #url = Field()
