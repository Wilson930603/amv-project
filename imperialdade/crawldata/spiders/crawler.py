import scrapy,json,re,html
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'imperialdade'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    DATASET={'Foodservice':{}}
    def start_requests(self):
        url='https://www.imperialdade.com/catalog/categories/foodservice?cid=WCL1001'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        Data=response.xpath('//div[@class="container"]/div[@class="row"]//div[contains(@class,"card-footer")]')
        for row in Data:
            url='https://www.imperialdade.com'+row.xpath('.//a/@href').get()
            Cate=str(row.xpath('.//a/text()').get()).strip()
            if not Cate in self.DATASET['Foodservice']:
                self.DATASET['Foodservice'][Cate]=[]
            yield scrapy.Request(url,callback=self.parse_list,meta={'Cate':Cate},dont_filter=True)
    def parse_list(self, response):
        Cate=response.meta['Cate']
        Data=response.xpath('//div[@id="products"]/div')
        for row in Data:
            url='https://www.imperialdade.com'+row.xpath('.//a/@href').get()
            yield scrapy.Request(url,callback=self.parse_content,meta={'Cate':Cate},dont_filter=True)
        next_page=response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            url=str(response.url).split('?')[0]+next_page
            yield scrapy.Request(url,callback=self.parse_list,meta={'Cate':Cate},dont_filter=True)
    def parse_content(self,response):
        Cate=response.meta['Cate']
        item={}
        item['url']=response.url
        item['Name']=response.xpath('//h3/text()').get()
        item['Manufacturer']=response.xpath('//div[contains(@class,"product-detail__manufacturer")]//a/text()').get()
        item['Size']=str(response.xpath('//div[contains(@class,"product-detail__pack-size")]/text()').get()).replace('\xa0',' ')
        Data=response.xpath('//div[contains(@id,"product_")]//div[contains(@class,"border-bottom")]')
        for row in Data:
            TITLE=row.xpath('./div[contains(@class,"text-label")]/text()').get()
            VAL=html.unescape(cleanhtml(row.xpath('.//div[not(contains(@class,"text-label"))]').get()).strip())
            item[TITLE]=VAL
        (self.DATASET['Foodservice'][Cate]).append(item)
        yield(item)