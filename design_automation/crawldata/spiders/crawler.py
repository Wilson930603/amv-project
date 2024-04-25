import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'design_automation'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0','Accept': 'application/json','Accept-Language': 'en-GB,en;q=0.5','appcode': 'VFP','clientappcategory': '30','clientapptype': '2','content-type': 'application/json','showactionid': 'false','Origin': 'https://hallerickson.ungerboeck.com','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin'}
    def start_requests(self):
        data = '["",0,"",120,"",0]'
        url='https://hallerickson.ungerboeck.com/prod/api/VFPServer/GetInitialData'
        yield scrapy.Request(url,callback=self.parse,method="POST",body=data,headers=self.headers,dont_filter=True)
    def parse(self, response):
        Data=json.loads(json.loads(response.text)[0])['ReturnObj']
        for row in Data['ExhibitorList']:
            data = '["17",5007,"DAC23SM",'+str(row['Id'])+',"*"]'
            url='https://hallerickson.ungerboeck.com/prod/api/VFPServer/GetExhibitorDetails'
            yield scrapy.Request(url,callback=self.parse_data,method="POST",body=data,headers=self.headers,dont_filter=True)
    def parse_data(self, response):
        Data=json.loads(json.loads(response.text)[0])['ReturnObj']
        item={}
        item['Company Name']=Data['Name']
        try:
            item['About Description']=Data['CatDesc']
        except:
            item['About Description']=''
        Products=[]
        for row in Data['Products']:
            Products.append(row['Desc'])
        item['Product Tags']=', '.join(Products)
        if len(str(Data['WebsiteURL']))>3:
            item['Website']=Data['WebsiteURL']
        else:
            item['Website']=''
        yield(item)