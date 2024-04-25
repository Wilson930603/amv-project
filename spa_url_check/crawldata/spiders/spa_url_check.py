import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime
from urllib.parse import urlparse

class CrawlerSpider(scrapy.Spider):
    name = 'spa_url_check'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    social=['facebook','google','yahoo','youtube','twitter','instagram']
    URLS=re.split('\r\n|\n',open('urls.txt').read())
    def start_requests(self):
        for URL in self.URLS:
            row=str(URL).split('~')
            if not str(row[1]).startswith('http'):
                row[1]='http://'+row[1]
            yield scrapy.Request(row[1],callback=self.parse,dont_filter=True,meta={'row':row,'proxy':None,'Level':0},errback=self.parse_error)
    def parse_error(self,failure):
        print(failure)
        row=failure.request.meta['row']
        Level=failure.request.meta['Level']
        if Level==0:
            yield scrapy.Request(row[1],callback=self.parse,dont_filter=True,meta={'row':row,'Level':0})
    def parse(self, response):
        print('\n ----------------------')
        print(response.url)
        row=response.meta['row']
        Level=response.meta['Level']
        domain = (str(urlparse(row[1]).netloc).lower()).replace('www.','')
        item={'ID':row[0],'URL':row[1]}
        print(response.meta)
        if response.status<400:
            TRUE_DOMAIN=is_domain(row[1],response.url)
            NAV=len(response.xpath('//nav').getall())
            H1=len(response.xpath('//h1').getall())
            H2=len(response.xpath('//h2').getall())
            H3=len(response.xpath('//h3').getall())
            H4=len(response.xpath('//h4').getall())
            H5=len(response.xpath('//h5').getall())
            H6=len(response.xpath('//h6').getall())
            HEADER=H1+H2+H3+H4+H5+H6
            LINKS=response.xpath('//a/@href').getall()
            LINK_IN=0
            LINK_OUT=0
            EMAIL=0
            SOCIAL=0
            RESPONSIVE=False
            RES=response.xpath('//meta[@name="viewport"]')
            if RES:
                RESPONSIVE=True

            for LINK in LINKS:
                LINK=str(LINK).lower()
                domain_name=(str(urlparse(row[1]).netloc).lower()).replace('www.','')
                if domain==domain_name or domain_name=='':
                    LINK_IN+=1
                if domain_name!='' and domain!=domain_name:
                    LINK_OUT+=1
                if 'mailto' in LINK:
                    EMAIL+=1
                for k in self.social:
                    if k in LINK:
                        SOCIAL+=1 
            item_dt={'TRUE_DOMAIN':TRUE_DOMAIN,'RESPONSIVE':RESPONSIVE,'HEADER':HEADER,'NAV':NAV,'LINK_IN':LINK_IN,'LINK_OUT':LINK_OUT,'EMAIL':EMAIL,'SOCIAL':SOCIAL,'H1':H1,'H2':H2,'H3':H3,'H4':H4,'H5':H5,'H6':H1}
            item.update(item_dt)
            item['Status']=''
            if item['RESPONSIVE']==False:
                item['Status']='None-Responsive'
            elif item['RESPONSIVE']=='':
                item['Status']='DEAD'
            else:
                if item['TRUE_DOMAIN']==False:
                    item['Status']='Filler Page'
                if item['Status']=='':
                    if item['LINK_IN']<=1 or item['LINK_IN']<item['LINK_OUT']:
                        item['Status']='Filler Page'
            if item['Status']=='':
                item['Status']='Real'
            
        elif Level==0:
            Level+=1
            yield scrapy.Request(row[1],callback=self.parse,dont_filter=True,meta={'row':row,'Level':Level})
        yield(item)

        
