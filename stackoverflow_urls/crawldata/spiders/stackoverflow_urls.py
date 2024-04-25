import scrapy
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'stackoverflow_urls'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    start_urls=['https://stackoverflow.com/questions/tagged/artifactory','https://stackoverflow.com/questions/tagged/nexus']
    domain='https://stackoverflow.com'
    conn=None
    def start_requests(self):
        for URL in self.start_urls:
            yield scrapy.Request(URL,callback=self.parse_data,meta={'URL':URL})
    def parse_data(self,response):
        URL=response.meta['URL']
        Data=response.xpath('//div[@id="questions"]/div[@data-post-id]')
        for row in Data:
            item={}
            item['URL']=URL
            item['Date']=row.xpath('.//span[@class="relativetime"]/@title').get()
            item['User']=row.xpath('.//div[@class="s-user-card--info"]//a/text()').get()
            item['Title']=str(row.xpath('.//h3/a/text()').get()).strip()
            TAGS=row.xpath('.//a[@rel="tag"]/text()').getall()
            item['Tags']=', '.join(TAGS)
            yield(item)
        next_page=response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            url=self.domain+next_page
            yield scrapy.Request(url,callback=self.parse_data,meta={'URL':URL})