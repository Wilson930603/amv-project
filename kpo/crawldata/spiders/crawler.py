import scrapy,json,os
from crawldata.functions import *

class CrawlerSpider(scrapy.Spider):
    name = 'reclameaqui'
    start_urls=[]
    start_urls.append('https://www.reclameaqui.com.br/empresa/cacau-show/lista-reclamacoes/')
    start_urls.append('https://www.reclameaqui.com.br/empresa/cacau-show-loja-online/lista-reclamacoes/')
    start_urls.append('https://www.reclameaqui.com.br/empresa/kopenhagen/lista-reclamacoes/')
    start_urls.append('https://www.reclameaqui.com.br/empresa/kopenhagen-loja-online/lista-reclamacoes/')
    start_urls.append('https://www.reclameaqui.com.br/empresa/lindt-chocolate-brasil/lista-reclamacoes/')
    domain='https://www.reclameaqui.com.br'
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self,response):
        if 'Ops, algo deu errado' in response.text:
            print("RE-CRAWL")
            yield scrapy.Request(response.url,callback=self.parse,dont_filter=True)
        else:
            k=str(response.url).split('/')[4]
            Data=response.xpath('//div[contains(@class,"bJdtis")]/a/@href').getall()
            for row in Data:
                url=self.domain + row
                yield scrapy.Request(url,callback=self.parse_detail,dont_filter=True)
            if len(Data)>1:
                if not '?pagina=' in response.url:
                    url=response.url+'?pagina=2'
                else:
                    url=str(response.url).split('?pagina=')[0]+'?pagina='+str(int(str(response.url).split('?pagina=')[1])+1)
                yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse_detail(self,response):
        ITEM={}
        URLS=str(response.url).split('/')
        ITEM['Category']=URLS[3]
        ITEM['url']=response.url
        ITEM['title']=response.xpath('//h1[@data-testid="complaint-title"]/text()').get()
        ITEM['subtitle']=response.xpath('//a[@data-testid="company-page-link"]/text()').get()
        ITEM['location']=response.xpath('//span[@data-testid="complaint-location"]/text()').get()
        ITEM['date']=response.xpath('//span[@data-testid="complaint-creation-date"]/text()').get()
        ITEM['id']=str(response.xpath('//span[@data-testid="complaint-id"]/text()').get()).strip()
        ITEM['tag_listitem-categoria']=response.xpath('//li[@data-testid="listitem-categoria"]//a/text()').get()
        ITEM['tag_listitem-produto']=response.xpath('//li[@data-testid="listitem-produto"]//a/text()').get()
        ITEM['tag_listitem-problema']=response.xpath('//li[@data-testid="listitem-problema"]//a/text()').get()
        ITEM['review_text']=str(response.xpath('//p[@data-testid="complaint-description"]/text()').get()).strip()
        ITEM['response_date']=''
        ITEM['response_text']=''
        ITEM['review_solved']=response.xpath('//div[@data-testid="complaint-evaluation-interaction"]//div[@data-testid="complaint-status"]/span/text()').get()
        ITEM['review_comeback']=response.xpath('//div[@data-testid="complaint-evaluation-interaction"]//div[@data-testid="complaint-deal-again"]/text()').get()
        ITEM['review_score']=response.xpath('//div[@data-testid="complaint-evaluation-interaction"]/div[not(@data-testid)]/div[3]/div/div/text()').get()
        ITEM['KEY_']=ITEM['id']
        RES=response.xpath('//div[@data-testid="complaint-interaction"]')
        if len(RES)>0:
            i=0
            for row in RES:
                item={}
                item.update(ITEM)
                item['response_date']=row.xpath('./div/span/text()').get()
                item['response_text']=cleanhtml(row.xpath('./p').get())
                item['KEY_']+='_'+str(i)
                i+=1
                yield(item)
        else:
            yield(ITEM)
            


        