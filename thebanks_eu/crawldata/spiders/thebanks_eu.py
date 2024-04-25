import scrapy,json,re,cloudscraper,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'thebanks_eu'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','mobile': False})
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    def start_requests(self):
        urls=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for URL in urls:
            URL=str(URL).split('~')
            item={}
            item['Country']=URL[0]
            item['URL']=URL[1]
            yield scrapy.Request(self.URL,callback=self.parse,meta={'item':item},dont_filter=True)
    def parse(self, response):
        ITEM=response.meta['item']
        HTML=self.scraper.get(ITEM['URL'])
        response=scrapy.Selector(text=HTML.text)
        Data=response.xpath('//div[@class="products"]/div[@class="product"]')
        for row in Data:
            RATE=row.xpath('.//div[contains(@class,"thebanks_score")]')
            if RATE:
                item={}
                item.update(ITEM)
                item['Name']=row.xpath('.//div[contains(@class,"name_text")]/a/text()').get()
                item['Company URL']=row.xpath('.//div[contains(@class,"name_text")]/a/@href').get()
                item['Business Focus']=row.xpath('.//div[contains(@class,"business_focus")]/text()').get()
                item['Rating']=str(RATE.xpath('.//text()').get()).replace('(', '').replace(')', '').replace('\xa0', '')
                yield(item)
        

        
