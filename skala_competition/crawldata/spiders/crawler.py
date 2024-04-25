import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'skala_competition'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        urls=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
        for ls in urls:
            ls=str(ls).split('~')
            Brand=ls[0]
            Brand_key=str(ls[1]).split('/')[-1]
            for i in range(0,160,5):
                url='https://lista.mercadolivre.com.br/beleza-cuidado-pessoal/novo/_PriceRange_'+str(i)+'-'+str(i+5)+Brand_key
                yield scrapy.Request(url,callback=self.parse,meta={'Brand':Brand},dont_filter=True)
            url='https://lista.mercadolivre.com.br/beleza-cuidado-pessoal/novo/_PriceRange_'+str(i+5)+'-'+str(0)+Brand_key
            yield scrapy.Request(url,callback=self.parse,meta={'Brand':Brand},dont_filter=True)
    def parse(self, response):
        Brand=response.meta['Brand']
        Data=response.xpath('//li[@class="ui-search-layout__item"]')
        for row in Data:
            item={}
            item['Brand Name']=Brand
            item['Product URL']=row.xpath('.//a/@href').get()
            item['KEY_']=''
            yield scrapy.Request(item['Product URL'],callback=self.parse_content,meta={'item':item},dont_filter=True)
        #next page
        next_page=response.xpath('//li[contains(@class,"andes-pagination__button--next")]/a/@href').get()
        if next_page:
            yield scrapy.Request(next_page,callback=self.parse,meta={'Brand':Brand},dont_filter=True)
    def parse_content(self,response):
        item=response.meta['item']
        Data=json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
        item['Product URL']=Data['offers']['url']
        item['KEY_']=str(item['Brand Name']).replace(' ', '-')+'_'+key_MD5(item['Product URL'])
        item['Product Name']=Data['name']
        item['Price']='BRL ' + str(Data['offers']['price'])
        item['Price Vol Equivalent']=''
        PVOL=response.xpath('//div[contains(@class,"ui-pdp-price--size-large")]//p[contains(@class,"ui-pdp-size--XSMALL")]/text()').get()
        if PVOL:
            item['Price Vol Equivalent']=str(PVOL).strip()
            Pvol=response.xpath('//div[contains(@class,"ui-pdp-price--size-large")]//p[contains(@class,"ui-pdp-size--XSMALL")]//span/text()').getall()
            PV=[]
            for rs in Pvol:
                if not 'reales' in rs or not 'centavos' in rs:
                    PV.append(str(rs).strip())
            item['Price Vol Equivalent']+=(' '+(''.join(PV)))
        try:
            item['Average Rating']=Data['aggregateRating']['ratingValue']
        except:
            item['Average Rating']=0
        try:
            item['Number of Ratings']=Data['aggregateRating']['reviewCount']
        except:
            item['Number of Ratings']=0
        DATA=response.xpath('//div[@class="ui-vpp-striped-specs__table"]') or response.xpath('//div[@id="technical_specifications"]//table') or response.xpath('//div[contains(@class,"ui-pdp-specs__table")]//table')
        if len(DATA)>0:
            Data=DATA[0].xpath('.//tr')
            if Data:
                item['Main Features Dictionary']={}
                for row in Data:
                    TITLE=row.xpath('./th/text()').get()
                    VAL=row.xpath('./td/span/text()').get()
                    item['Main Features Dictionary'][TITLE]=VAL
        else:
            item['Main Features Dictionary']=''
        yield(item)