import scrapy
from crawldata.functions import *

class CrawlerSpider(scrapy.Spider):
    name = 'stackoverflow_data'
    start_urls=['https://stackoverflow.com/tags']
    domain='https://stackoverflow.com'
    conn=None
    def parse(self, response):
        Data=response.xpath('//div[@id="tags-browser"]/div')
        for row in Data:
            url=self.domain+row.xpath('.//a/@href').get()
            txt=row.xpath('.//a/text()').get()
            item={}
            item['SHEET']='urls'
            item['KEY_']=key_MD5(url)
            item['name']=txt
            item['url']=url
            item['questions']=str(row.xpath('.//div[@class="flex--item" and contains(text(),"question")]/text()').get()).split()[0]
            yield item
        next_page=response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            url=self.domain+next_page
            yield scrapy.Request(url,callback=self.parse)