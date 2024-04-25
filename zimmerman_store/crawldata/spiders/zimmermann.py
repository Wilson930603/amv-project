import scrapy,json
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'zimmermann'
    start_urls=['https://www.zimmermann.com/hk/store/locate-store/']
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def parse(self, response):
        Data=response.xpath('//div[@class="column main"]//div[@class="container"]')
        for row in Data:
            Country=row.xpath('./div[@role="heading"]/text()').get()
            if Country:
                data=row.xpath('.//div[@class="current_store_details store"]')
                for rs in data:
                    item={}
                    item['Region']=str(Country).strip()
                    item['Title']=str(rs.xpath('.//a[@class="store__name"]/text()').get()).strip()
                    item['Address']=str(rs.xpath('.//span[@class="store__address"]/text()').get()).strip()
                    yield(item)
        
