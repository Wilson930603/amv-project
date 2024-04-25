import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'shopbop'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        url='https://www.shopbop.com/reviews/brand?folderID=5090&baseIndex=0'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'Index':0})
    def parse(self, response):
        Index=response.meta['Index']
        Data=response.xpath('//div[contains(@class,"brand-product-review")]')
        for row in Data:
            ITEM={}
            ITEM['URL']=response.url
            ITEM['Product Name']=row.xpath('.//span[@class="description"]/text()').get()
            if not ITEM['Product Name'] is None:
                PRICES=row.xpath('.//span[@class="salePrice"]/text()').getall() or row.xpath('.//div[contains(@class,"product-info")]/text()').getall()
                PRICE=''
                for rs in PRICES:
                    rs=str(rs).strip()
                    if '$' in rs and PRICE=='':
                        PRICE=rs
                ITEM['Price']=PRICE
                Review=str(row.xpath('.//div[contains(@class,"product-info")]//img[contains(@src,"rebrand_stars_")]/@src').get()).split('rebrand_stars_')[1].split('_')[0]
                ITEM['Overall Rating']=Review
                ITEM['Overall # of Reviews']=Get_Number(row.xpath('.//a[@class="brandReviewCount"]/text()').get())
                data=row.xpath('.//div[@class="review"]')
                for rs in data:
                    item={}
                    item.update(ITEM)
                    item['User']=rs.xpath('.//div[contains(@class,"profile-name")]/text()').get()
                    item['Location']=rs.xpath('.//div[contains(@class,"location")]/text()').get()
                    try:
                        item['# of User Reviews']=str(rs.xpath('.//div[contains(@class,"see-users-reviews")]/a/text()').get()).split('(')[-1].split(')')[0]
                    except:
                        item['# of User Reviews']=''
                    Review=str(rs.xpath('.//span[@class="review-rating"]/img/@src').get()).split('rebrand_stars_')[1].split('_')[0]
                    item['User Rating']=Review
                    item['Rating Title']=rs.xpath('.//span[contains(@class,"review-title")]/text()').get()
                    item['Rating Description']=rs.xpath('.//div[@class="review-text"]/text()').get()
                    Sizes=rs.xpath('.//div[@class="size"]/text()').getall()
                    Size=''
                    for r in Sizes:
                        r=str(r).strip()
                        if r!='' and not 'Sizing:' in r and Size=='':
                            Size=r
                    item['Sizing']=Size
                    yield(item)
        if len(Data)>0:
            Index+=15
            url='https://www.shopbop.com/reviews/brand?folderID=5090&baseIndex='+str(Index)
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'Index':Index})