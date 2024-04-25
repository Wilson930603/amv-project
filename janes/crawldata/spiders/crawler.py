import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'janes'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        urls=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for url in urls:
            page=1
            yield scrapy.Request(url,callback=self.parse,meta={'url':url,'page':page},dont_filter=True)
    def parse(self, response):
        page=response.meta['page']
        url=response.meta['url']
        Data=response.xpath('//div[contains(@class,"list-item")]')
        for row in Data:
            item={}
            item['url_scraper']=url
            item['URL']=row.xpath('.//a/@href').get()
            item['Title']=row.xpath('.//h3/text()').get()
            SPAN=row.xpath('.//span/text()').getall()
            item['Author']=''
            item['Date']=''
            if len(SPAN)>=2:
                item['Author']=SPAN[0]
                item['Date']=SPAN[1]
            elif len(SPAN)>=1:
                strtxt=(str(SPAN[0]).strip()).split()
                if len(strtxt[-1])==4 and Get_Number(strtxt[-1])==strtxt[-1]:
                    item['Date']=SPAN[0]
                else:
                    item['Author']=SPAN[0]
            yield(item)
        if len(Data)>=20:
            page+=1
            yield scrapy.Request(url+'/'+str(page),callback=self.parse,meta={'url':url,'page':page},dont_filter=True)