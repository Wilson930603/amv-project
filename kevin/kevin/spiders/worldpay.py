import scrapy,json,csv,os
from os import path
class CrawlerSpider(scrapy.Spider):
    name = 'worldpay'
    def start_requests(self):
        url='https://workswith.worldpay.com/en/listing'
        if path.exists("worldpay.csv"):
            os.remove("worldpay.csv")
        with open('worldpay.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["URL", "Name", "Description", "Integrated to Worldpay Product(s)", "Vendor"]
            writer.writerow(field)
        yield scrapy.Request(url,callback=self.get_listing,meta={'page':1},dont_filter=True)
    def get_listing(self,response):
        hrefs=response.xpath('//a[@class="id id__logo id__sq_large id__linked"]/@href').getall()
        for href in hrefs:
            link = 'https://workswith.worldpay.com'+href
            yield scrapy.Request(link,callback=self.parse_page,dont_filter=True)
        if len(hrefs)>=12:
            pagenum=response.meta['page']+1
            url='https://workswith.worldpay.com/en/listing?page='+str(pagenum)
            yield scrapy.Request(url,callback=self.get_listing,meta={'page':pagenum},dont_filter=True)
    def parse_page(self, response):
        url=response.url
        name=""
        description=""
        integrated_to_worldpay_product_s=""
        vendor=""
        try:
            name=response.xpath('//h1[@class="title"]/text()').get()
        except:
            name=""
        try:
            description=response.xpath('//div[@class="description"]/text()').get()
        except:
            description=""
        i=0
        j=0
        for row in response.xpath('//h1[@class="integrated-vendor-info"]').getall():
            if response.xpath('//h1[@class="integrated-vendor-info"]//text()').getall()[j].strip()=="Integrated to Worldpay Product(s):":
                integrated_to_worldpay_product_s=response.xpath('//h1[@class="integrated-vendor-info"]//a/text()').getall()[i]
            if response.xpath('//h1[@class="integrated-vendor-info"]//text()').getall()[j].strip()=="Vendor:":
                vendor=response.xpath('//h1[@class="integrated-vendor-info"]//a/text()').getall()[i]
            i+=1
            j+=2
        with open('worldpay.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([url, name, description, integrated_to_worldpay_product_s, vendor])