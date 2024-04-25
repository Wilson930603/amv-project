import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'globalblue'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        url='https://public.globalblue-prod.magnolia-platform.com/.rest/delivery/countries/v1/?orderBy=title'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        Data=json.loads(response.text)
        for Country in Data['results']:
            url='https://public.globalblue-prod.magnolia-platform.com/.rest/delivery/listStores/v1?country='+Country['countryKey']+'&salesforcePubliciationStatus=true'
            yield scrapy.Request(url,callback=self.parse_stores,dont_filter=True)
    def parse_stores(self,response):
        Data=json.loads(response.text)
        if 'results' in Data:
            for row in Data['results']:
                url='https://public.globalblue-prod.magnolia-platform.com/.rest/delivery/storeLocator/v1?saleforceId='+row['saleforceId']+'&salesforcePubliciationStatus=true'
                yield scrapy.Request(url,callback=self.parse_store,dont_filter=True)
    def parse_store(self,response):
        Data=json.loads(response.text)
        for row in Data['results']:
            item={}
            item['Country']=row['country']
            item['Store Name']=row['title']
            item['Address']=row['street']+', '+row['zip']+' '+row['city']+', '+row['country']
            item['Store Category']=row['products']
            yield(item)