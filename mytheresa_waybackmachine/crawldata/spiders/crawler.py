import scrapy,json
from crawldata.functions import *
from datetime import datetime
from urllib.parse import quote
class CrawlerSpider(scrapy.Spider):
    name = 'mytheresa_waybackmachine'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    urls=['https://www.mytheresa.com/en-us/designers.html','https://www.mytheresa.com/de-de/designers.html']
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        for URL in self.urls:
            for YEAR in range(2012,datetime.now().year+1):
                url='http://web.archive.org/web/'+datetime.now().strftime('%Y')+'0000000000*/'+URL
                url='http://web.archive.org/__wb/calendarcaptures/2?url='+quote(URL)+'&date='+str(YEAR)+'&groupby=day'
                yield scrapy.Request(url,callback=self.parse,meta={'URL':URL,'YEAR':YEAR})
    def parse(self, response):
        URL=response.meta['URL']
        YEAR=response.meta['YEAR']
        Data=json.loads(response.text)
        for row in Data['items']:
            if row[1]==200:
                MD=str(YEAR) + ("{:04d}".format(row[0]))
                url='http://web.archive.org/__wb/calendarcaptures/2?url='+quote(URL)+'&date='+MD
                yield scrapy.Request(url,callback=self.parse_data_list,meta={'URL':URL,'MD':MD})
    def parse_data_list(self, response):
        URL=response.meta['URL']
        MD=response.meta['MD']
        Data=json.loads(response.text)
        for row in Data['items']:
            if row[1]==200:
                MDS=MD + ("{:06d}".format(row[0]))
                url='http://web.archive.org/web/'+MDS+'/'+URL
                yield scrapy.Request(url,callback=self.parse_data,meta={'URL':URL,'MD':MDS,'Level':0},dont_filter=True)
    def parse_data(self,response):
        URL=response.meta['URL']
        MD=response.meta['MD']
        Level=response.meta['Level']
        YEAR=MD[:4]
        MONTH=MD[4]+MD[5]
        DAY=MD[6]+MD[7]
        HOUR=MD[8]+MD[9]
        MINUTE=MD[10]+MD[11]
        SECOND=MD[12]+MD[13]
        item={}
        item['Website']=URL
        item['Record URL']=response.url
        item['Date Time']=YEAR+'-'+MONTH+'-'+DAY+'T'+HOUR+':'+MINUTE+':'+SECOND
        BRAND=response.xpath('//div[@id="designer-list"]//li/a//text()').getall()
        BRANDS=[]
        for i in range(len(BRAND)):
            brand=str(BRAND[i]).strip()
            if brand!='':
                BRANDS.append(brand)
        item['List of Brands']='; '.join(BRANDS)
        yield item
        
