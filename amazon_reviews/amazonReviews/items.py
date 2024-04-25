# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class AmazonreviewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Retailer_Name = Field()
    Title = Field()
    Review_Star = Field()
    Is_Verified = Field()
    Has_Response = Field()
    Review_Title = Field()
    Review_Text = Field()
    Review_Date = Field()
    Review_URL = Field()
    Category = Field()
    Is_Discontinued_By_Manufacturer = Field()
    Product_Dimensions = Field()
    Item_model_number = Field()
    UPC = Field()
    Manufacturer = Field()
    ASIN = Field()
    Brand = Field()
    URL = Field()

class AmazonUrls(scrapy.Item):
    brand = Field()
    url = Field()