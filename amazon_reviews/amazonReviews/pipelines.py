# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import AmazonreviewsItem, AmazonUrls
import pandas as pd
import os
import csv
import sys
class AmazonreviewsPipeline:
    base_urlUS = "https://www.amazon.com"
    base_urlUK = "https://www.amazon.co.uk"
    fileNames = []
    def __init__(self):
        self.file = {}
        self.writer = {}
    
    def close_spider(self, spider):
        for keys in self.file.keys():
            self.file[keys].close()

    def process_item(self, item, spider):
        UK_url = './datafolder/UK/'
        US_url = './datafolder/US/'
        try:
            adapter = AmazonreviewsItem(item)
            url = adapter['URL']
            if self.base_urlUK in url:
                filename = UK_url+adapter['Brand']+'.csv'
            else:
                filename = US_url+adapter['Brand']+'.csv'
            brand = adapter['Brand']
            if self.file.get(brand) is None:
                self.file[brand] = open(filename, 'a', newline='', encoding='utf-8-sig')
                self.writer[brand] = csv.writer(self.file[brand])
                if self.file[brand].tell() == 0:
                    self.writer[brand].writerow([
                        'Retailer_Name',
                        'Title',
                        'Review_Star',
                        'Is_Verified',
                        'Has_Response',
                        'Review_Title',
                        'Review_Text',
                        'Review_Date',
                        'Review_URL',
                        'Category',
                        'Is_Discontinued_By_Manufacturer',
                        'Product_Dimensions',
                        'Item_model_number',
                        'UPC',
                        'Manufacturer',
                        'ASIN',
                        'Brand',
                        'URL',
                    ])
                    self.file[brand].flush()
                    os.fsync(self.file[brand].fileno())
            self.writer[brand].writerow([
                adapter['Retailer_Name'],
                adapter['Title'],
                adapter['Review_Star'],
                adapter['Is_Verified'],
                adapter['Has_Response'],
                adapter['Review_Title'],
                adapter['Review_Text'],
                adapter['Review_Date'],
                adapter['Review_URL'],
                adapter['Category'],
                adapter['Is_Discontinued_By_Manufacturer'],
                adapter['Product_Dimensions'],
                adapter['Item_model_number'],
                adapter['UPC'],
                adapter['Manufacturer'],
                adapter['ASIN'],
                adapter['Brand'],
                adapter['URL'],
            ])
            self.file[brand].flush()
            os.fsync(self.file[brand].fileno())
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            
            
        return item

