import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime
from urllib.parse import urlparse, urlencode,parse_qsl

class CrawlerSpider(scrapy.Spider):
    name = 'walmart'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    domain='https://www.walmart.com'
    def start_requests(self):
        yield scrapy.Request('https://www.walmart.com/all-departments',callback=self.parse,dont_filter=True)
    def parse(self, response):
        DATA=response.xpath('//main//ul[contains(@class,"list")]')
        for ROW in DATA:
            CATE=ROW.xpath('../h2/a/text()').get()
            Data=ROW.xpath('.//li/a[not(contains(@link-identifier,"Shop All"))]')
            for row in Data:
                Cate=row.xpath('./text()').get()
                url=row.xpath('./@href').get()
                if not str(url).startswith('http'):
                    url=self.domain+url
                if self.domain in url:
                    yield scrapy.Request(url,callback=self.parse_list,dont_filter=True,meta={'CATE':CATE,'Cate':Cate,'Page':1})
    def parse_list(self,response):
        CATE=response.meta['CATE']
        Cate=response.meta['Cate']
        Page=response.meta['Page']
        HTML=response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if HTML is None:
            yield scrapy.Request(response.meta['redirect_urls'][0],callback=self.parse_list,dont_filter=True,meta={'CATE':CATE,'Cate':Cate,'Page':Page})
        else:
            DATA=json.loads(HTML)
            try:
                Data=DATA['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']
                MAX_PAGE=DATA['props']['pageProps']['initialData']['searchResult']['paginationV2']['maxPage']
            except:
                Data=[]
                MAX_PAGE=0
            for row in Data:
                if 'canonicalUrl' in row:
                    yield scrapy.Request(self.domain+row['canonicalUrl'],callback=self.parse_data,dont_filter=True,meta={'CATE':CATE,'Cate':Cate})
            if Page<MAX_PAGE:
                Page+=1
                parsed_url = urlparse(response.url)
                URL=dict(parse_qsl(parsed_url.query))
                URL['page']=str(Page)
                url=parsed_url.scheme+'://'+parsed_url.netloc+parsed_url.path
                if not '?' in url:
                    url+='?'
                url+=urlencode(URL)
                yield scrapy.Request(url,callback=self.parse_list,dont_filter=True,meta={'CATE':CATE,'Cate':Cate,'Page':Page})
    def parse_data(self,response):
        CATE=response.meta['CATE']
        Cate=response.meta['Cate']
        HTML=response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if HTML is None:
            yield scrapy.Request(response.meta['redirect_urls'][0],callback=self.v,dont_filter=True)
        else:
            DATA=json.loads(HTML)
            row=DATA['props']['pageProps']['initialData']['data']['product']
            item={}
            item['KEY_']=key_MD5(CATE+Cate+response.url)
            item['Store Name']='Walmart'
            item['Product Category']=CATE
            item['Product Subcategory']=Cate
            item['Product URL']=response.url
            item['Product title']=row['name']
            item['Product Brand']=row['brand']
            try:
                item['Product Price']=row['priceInfo']['currentPrice']['price']
            except:
                item['Product Price']=''
            yield(item)
        

        
