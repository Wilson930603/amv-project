# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class NetaportaItem(scrapy.Item):
    ProductURL = Field()
    MainCategory = Field()
    Brand = Field()
    BrandTotalProducts = Field()
    ProductCategory = Field()
    ProductSubCategory = Field()
    ProductSubsubCategory = Field()
    ProductName = Field()
    ProductPrice = Field()
    

class FartechItem(scrapy.Item):
    ProductURL = Field()
    MainCategory = Field()
    Brand = Field()
    BrandTotalProducts = Field()
    ProductCategory = Field()
    ProductSubcategory = Field()
    ProductSubsubcategory = Field()
    ProductName = Field()
    Price = Field()
    DiscountPrice = Field()