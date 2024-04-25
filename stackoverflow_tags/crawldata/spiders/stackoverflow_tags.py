import scrapy,re,json
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'stackoverflow_tags'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    domain='https://stackoverflow.com'
    def start_requests(self):
        TAGS=re.split('\r\n|\n',open('tags.txt').read())
        for tags in TAGS:
            data = {'filter': tags,'tab': 'Popular','namesOnly': 'false'}
            yield scrapy.FormRequest('https://stackoverflow.com/filter/tags-for-index',formdata=data,callback=self.parse_tags,meta={'tags':tags})
    def parse_tags(self,response):
        tags=response.meta['tags']
        Data=response.xpath('//div[@id="tags-browser"]/div')
        for row in Data:
            url=self.domain+row.xpath('.//a/@href').get()
            yield scrapy.Request(url,callback=self.parse_data,meta={'tags':tags})
        next_page=response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            url=self.domain+next_page
            yield scrapy.Request(url,callback=self.parse_tags,meta={'tags':tags})
    def parse_data(self,response):
        tags=response.meta['tags']
        Data=response.xpath('//div[@id="questions"]/div[@data-post-id]')
        for row in Data:
            item={}
            item['KEY_']=row.xpath('./@data-post-id').get()
            item['Search_tags']=tags
            item['Title']=str(row.xpath('.//h3/a/text()').get()).strip()
            TAGS=row.xpath('.//a[@rel="tag"]/text()').getall()
            item['Tags']=', '.join(TAGS)
            item['Time']=row.xpath('.//span[@class="relativetime"]/@title').get()
            item['Author']=row.xpath('.//div[@class="s-user-card--info"]//a/text()').get()
            DT=row.xpath('./div/div[contains(@class,"s-post-summary--stats-item")]')
            item['Votes']=''
            item['Answers']=''
            item['Views']=''
            IT={}
            for rs in DT:
                TITIE=rs.xpath('./span[@class="s-post-summary--stats-item-unit"]/text()').get()
                if TITIE:
                    TITIE=(str(TITIE).strip()).title()
                    Val=rs.xpath('./span[@class="s-post-summary--stats-item-number"]/text()').get()
                    IT[TITIE]=Val
            for k,v in IT.items():
                if 'Vote' in k:
                    item['Votes']=v
                if 'Answer' in k:
                    item['Answers']=v
                if 'View' in k:
                    item['Views']=v
            item['Text']=str(row.xpath('.//div[@class="s-post-summary--content-excerpt"]/text()').get()).strip()
            item['Link']=self.domain+row.xpath('.//h3/a/@href').get()
            yield(item)
        next_page=response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            url=self.domain+next_page
            yield scrapy.Request(url,callback=self.parse_data,meta={'tags':tags})