import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'k18'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    def start_requests(self):
        yield scrapy.Request('https://stockist.co/api/v1/u5301/locations/all',callback=self.parse,dont_filter=True)
    def parse(self, response):
        Data=json.loads(response.text)
        for row in Data:
            item={}
            if len(row['custom_fields'])>0:
                item['Person Name']=row['custom_fields'][0]['value']
            else:
                item['Person Name']=''
            item['Salon Name']=row['name']
            ADDS=['address_line_1','address_line_2','city','state','postal_code']
            ADD=[]
            for rs in ADDS:
                if rs in row and row[rs]:
                    ADD.append(row[rs])
            item['Address']=', '.join(ADD)
            item['Country']=row['country']
            item['Phone Number']=row['phone']
            item['Email']=row['email']
            item['Website']=row['website']
            yield(item)

        
