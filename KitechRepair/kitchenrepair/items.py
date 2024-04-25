# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class KitchenrepairItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    URL = Field()
    City = Field()
    State = Field()
    ZIPCode = Field()
    TollFreeNumber = Field()
    BusinessFax = Field()
    BusinessWebsiteAddress = Field()
    PrimaryContact = Field()
    PrimaryContactJobTitle = Field()
    PrimaryContactEmail = Field()
    InstallationLevel = Field()
    Servicesoffered = Field()
    YearEstablished = Field()
    CFESAMembersince = Field()
    MemberGroup = Field()
    CFESAGeographicalRegion = Field()
    pass
