import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'crowneplaza'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    CRAWLED=[]
    IDS=[]
    def start_requests(self):
        url='https://www.ihg.com/crowneplaza/destinations/us/en/explore'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        Data=response.xpath('//section[contains(@class,"countryListing")]//li[contains(@class,"listingItem")]')
        for row in Data:
            url=row.xpath('.//a/@href').get()
            KEY=key_MD5(url)
            if not KEY in self.CRAWLED:
                self.CRAWLED.append(KEY)
                yield scrapy.Request(url,callback=self.parse,dont_filter=True)
        if len(Data)==0:
            Data=response.xpath('//section[@class="hotel-list-container"]//div[contains(@id,"hotelID-")]')
            for row in Data:
                ID=row.xpath('./@id').get()
                if not ID in self.IDS:
                    self.IDS.append(ID)
                    item={}
                    item['Hotel Name']=row.xpath('.//a[contains(@id,"hotelDetailNameLink-")]/text()').get()
                    Address=row.xpath('.//div[contains(@id,"address-Section-")]//span/text()').getall()
                    ADD=[]
                    for rs in Address:
                        rs=str(rs).strip()
                        if rs!='':
                            ADD.append(rs)
                    item['Address']=' '.join(ADD)
                    yield(item)

        

        
