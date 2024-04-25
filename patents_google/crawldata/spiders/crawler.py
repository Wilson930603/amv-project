import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'patents_google_1'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    URLS=re.split('\r\n|\n', open('urls1.txt').read())
   #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        for url in self.URLS:
            yield scrapy.Request(url,callback=self.parse)
    def parse(self, response):
        item={}
        item['Patent Number']=response.xpath('//dd[@itemprop="publicationNumber"]/text()').get()
        item['Abstract']=response.xpath('//abstract/div/text()').get()
        item['Location']=response.xpath('//dd[@itemprop="countryName"]/text()').get()
        item['Inventor']=response.xpath('//dd[@itemprop="inventor"]/text()').getall()
        item['Current Assignee']=response.xpath('//dd[@itemprop="assigneeCurrent"]/text()').get()
        item['Worldwide applications']=[]
        Data=response.xpath('//li[@itemprop="applicationsByYear"]')
        for row in Data:
            it={}
            data=row.xpath('.//span[@itemprop]')
            for rs in data:
                it[rs.xpath('./@itemprop').get()]=rs.xpath('./text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Worldwide applications'].append(it)
        item['Events']=[]
        Data=response.xpath('//dd[@itemprop="events"]')
        for row in Data:
            it={}
            data=row.xpath('.//*[@itemprop]')
            for rs in data:
                it[rs.xpath('./@itemprop').get()]=rs.xpath('./text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Events'].append(it)
        item['Classifications']=[]
        Data=response.xpath('//li[@itemprop="cpcs"]')
        for row in Data:
            it={}
            data=row.xpath('.//*[@itemprop]')
            for rs in data:
                it[rs.xpath('./@itemprop').get()]=rs.xpath('./text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Classifications'].append(it)
        item['Description']=cleanhtml(response.xpath('//section[@itemprop="description"]/div[@itemprop="content"]').get())
        item['Patent Citations']=[]
        LABEL={'Publication number':'publicationNumber','Language':'primaryLanguage','Priority date':'priorityDate','Publication date':'publicationDate','Assignee':'assigneeOriginal','Title':'title'}
        Data=response.xpath('//tr[@itemprop="backwardReferences"]')
        for row in Data:
            it={}
            for k,v in LABEL.items():
                it[k]=row.xpath('.//*[@itemprop="'+v+'"]/text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Patent Citations'].append(it)
        for k,v in item.items():
            if not v is None and not isinstance(v, list) and not isinstance(v, dict) and not isinstance(v, tuple):
                item[k]=str(v).strip()
        Data=response.xpath('//tr[@itemprop="backwardReferencesFamily"]')
        for row in Data:
            it={}
            for k,v in LABEL.items():
                it[k]=row.xpath('.//*[@itemprop="'+v+'"]/text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Patent Citations'].append(it)
        item['Cited By']=[]
        Data=response.xpath('//tr[@itemprop="forwardReferencesOrig"]')
        for row in Data:
            it={}
            for k,v in LABEL.items():
                it[k]=row.xpath('.//*[@itemprop="'+v+'"]/text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Cited By'].append(it)
        for k,v in item.items():
            if not v is None and not isinstance(v, list) and not isinstance(v, dict) and not isinstance(v, tuple):
                item[k]=str(v).strip()
        Data=response.xpath('//tr[@itemprop="forwardReferencesFamily"]')
        for row in Data:
            it={}
            for k,v in LABEL.items():
                it[k]=row.xpath('.//*[@itemprop="'+v+'"]/text()').get()
            for k,v in it.items():
                it[k]=str(v).strip()
            item['Cited By'].append(it)
        yield(item)

        #f=open(item['Patent Number']+'.html','w',encoding='utf-8')
        #f.write(response.text)
        #f.close()
        
