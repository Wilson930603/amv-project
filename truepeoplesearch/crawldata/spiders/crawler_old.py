import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'truepeoplesearch_old'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    def start_requests(self):
        phones=open('phone.txt').read().splitlines()
        for phone in phones:
            url='https://www.truepeoplesearch.com/results?name='+phone
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'phone':phone})
    def parse(self, response):
        phone=response.meta['phone']
        if response.status<400:
            Data=response.xpath('//div[@data-detail-link]')
            if len(Data)>0:
                for row in Data:
                    item={}
                    item['phone']=phone
                    item['Name']=str(row.xpath('.//div[@class="h4"]/text()').get()).strip()
                    LABELS=row.xpath('.//*[@class="content-label"]/text()').getall()
                    VALUES=row.xpath('.//*[@class="content-value"]/text()').getall()
                    for i in range(len(LABELS)):
                        item[str(LABELS[i]).strip()]=str(VALUES[i]).strip()
                    item['url']='https://www.truepeoplesearch.com'+row.xpath('./@data-detail-link').get()
                    yield scrapy.Request(item['url'],callback=self.parse_detail,meta={'item':item},dont_filter=True)
            else:
                item={}
                item['Phone Number']=phone
                item['Digits']=len(item['Phone Number'])
                item['Name']=''
                item['Age']=''
                item['Birthday']=''
                item['Current Address']=''
                item['Address Info (Tenure)']=''
                item['Primary Phone']=''
                item['Email Addresses']=''
                item['Current Property Details (Est. Value)']=''
                item['Est. Equity']=''
                yield(item)
        else:
            yield scrapy.Request(response.url,callback=self.parse,meta={'phone':phone},dont_filter=True)
    def parse_detail(self, response):
        ITEM=response.meta['item']
        if response.status<400:
            Birthday=str(response.xpath('//div[@id="personDetails"]//span[contains(text(),"Age")]/text()').get()).strip()
            if '(' in Birthday:
                Birthday=str(Birthday).split('(')[1].split(')')[0]
            else:
                Birthday=''
            item={}
            item['Phone Number']=ITEM['phone']
            item['Digits']=len(item['Phone Number'])
            item['Name']=ITEM['Name']
            item['Age']=ITEM['Age']
            item['Birthday']=Birthday
            item['Current Address']=''
            item['Address Info (Tenure)']=''
            item['Primary Phone']=''
            item['Email Addresses']=''
            item['Current Property Details (Est. Value)']=''
            item['Est. Equity']=''
            ADDRESS=response.xpath('//div[@id="personDetails"]//div[@itemprop="address"]')
            if len(ADDRESS)>0:
                ADD=ADDRESS[0]
                ADDS=ADD.xpath('.//span[@itemprop]/text()').getall()
                item['Current Address']=', '.join(ADDS)
                Tenures=ADD.xpath('.//span[@class="dt-sb"]/text()').getall()
                for i in range(len(Tenures)):
                    Tenures[i]=str(Tenures[i]).strip()
                item['Address Info (Tenure)']='\n'.join(Tenures)
            item['Primary Phone']=response.xpath('//div[@id="personDetails"]//span[@itemprop="telephone"]/text()').get().strip()
            EMAILS=response.xpath('//div[@id="personDetails"]//div[contains(text(),"@")]/text()').getall()
            for i in range(len(EMAILS)):
                EMAILS[i]=str(EMAILS[i]).strip()
            item['Email Addresses']='\n'.join(EMAILS)
            ESV=response.xpath('//div[@id="personDetails"]//div[contains(text(),"Estimated Value")]')
            if ESV:
                item['Current Property Details (Est. Value)']=ESV.xpath('./b/text()').get()
            ESE=response.xpath('//div[@id="personDetails"]//div[contains(text(),"Estimated Equity")]')
            if ESE:
                item['Est. Equity']=ESE.xpath('./b/text()').get()
            yield(item)

        else:
            yield scrapy.Request(response.url,callback=self.parse_detail,meta={'item':ITEM},dont_filter=True)
        

        
