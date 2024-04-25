import scrapy,json,os
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    #https://www.olx.pl/oferty/uzytkownik/1zUMu2/
    name = 'olx_api'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    START=25000000
    END=1144935731
    END=START+5000000
    LIMIT=5
    if os.path.exists('CRAWLED.txt'):
        START=int(open('CRAWLED.txt','r').read())-LIMIT
    #START+=1
    headers = {'Accept': '*/*','Accept-Language': 'pl','Referer': 'https://www.olx.pl/oferty/uzytkownik/1zUMu2/','X-Client': 'DESKTOP','X-Platform-Type': 'mobile-html5','Version': 'v1.19','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','Authorization': '','Connection': 'keep-alive',}
    headers['Authorization']='Bearer c338a21fb45ff82da057c6e60caa73057e36d887'
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        for i in range(self.LIMIT):
            self.START+=1
            url='https://www.olx.pl/api/v1/users/'+str(self.START)+'/'
            yield scrapy.Request(url,callback=self.parse,meta={'id':self.START},headers=self.headers,dont_filter=True)
    def parse(self, response):
        if response.status==401:
            yield scrapy.Request('http://222.255.38.4/Bearer.txt',callback=self.update_bearer,meta={'id':response.meta['id']},dont_filter=True)
        else:
            id=response.meta['id']+self.LIMIT
            if response.status==200:
                item=json.loads(response.text)
                ITEM={}
                ITEM['KEY_']=item['data']['id']
                ITEM.update(item['data'])
                yield ITEM
                f=open('CRAWLED.txt','w',encoding='utf-8')
                f.write(str(response.meta['id']))
                f.close()
            if id<=self.END:
                url='https://www.olx.pl/api/v1/users/'+str(id)+'/'
                yield scrapy.Request(url,callback=self.parse,meta={'id':id},headers=self.headers,dont_filter=True)
    def update_bearer(self,response):
        id=response.meta['id']
        self.headers['Authorization']=response.text
        url='https://www.olx.pl/api/v1/users/'+str(id)+'/'
        yield scrapy.Request(url,callback=self.parse,meta={'id':id},headers=self.headers,dont_filter=True)