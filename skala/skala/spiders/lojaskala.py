import scrapy,re
from skala.functions import *

class LojaskalaSpider(scrapy.Spider):
    name = "lojaskala"
    #allowed_domains = ["lojaskala.com.br"]
    start_urls = ["https://www.lojaskala.com.br/fabricante/skala"]
    
    def start_requests(self):
        f=open('lojaskala_urls.txt','r',encoding='utf-8')
        URLS=re.split('\r\n|\n', f.read())
        f.close()
        for URL in URLS:
            ID=(str(URL).split('/')[4])
            page=1
            url='https://www.lojaskala.com.br/fabricante/' + ID
            yield scrapy.Request(url,callback=self.parse, meta = {'ID':ID,'page':page})


    def parse(self, response):
        page = response.meta['page']
        Data = response.xpath('//span[contains(@id,"fbits-grupo-pagina")]//div[contains(@id,"produto-spot-item")]/a')
        for row in Data:
            url = 'https://www.lojaskala.com.br' + row.xpath('./@href').get()
            yield scrapy.Request(url,callback=self.parse_item, meta=response.meta)
        if(len(Data) > 1):
            ID = response.meta['ID']
            page += 1
            next_url = 'https://www.lojaskala.com.br/fabricante/' + ID + '?pagina=' + str(page)
            yield scrapy.Request(next_url, callback=self.parse, meta={'ID':ID, 'page':page})

    def parse_item(self, response):
        Item = {}
        Item['Product Line'] = response.xpath('//div[@id="fbits-fabricante-logo"]//img/@title').get().encode().decode('utf-8')
        Item['Product URL'] = response.request.url
        Item['Product Name'] = response.xpath('//h1[contains(@id,"produto-nome")]/text()').get().replace('\r\n','').encode().decode('utf-8')
        Item['Price'] = response.xpath('//div[@id="divFormaPagamento"]/div/text()').get()
        Item['Description'] = cleanhtml(response.xpath('//div[@id="conteudo-0"]//div[@class="paddingbox"]').get()).replace('\n','').encode().decode('utf-8')

        yield(Item)

        





