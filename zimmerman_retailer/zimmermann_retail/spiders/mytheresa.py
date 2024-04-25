import scrapy


class MytheresaSpider(scrapy.Spider):
    name = "mytheresa"
    allowed_domains = ["www.mytheresa.com"]
    start_urls = ["http://www.mytheresa.com/"]

    def parse(self, response):
        for i in range(1,5):
            url = 'https://www.mytheresa.com/en-us/designers/zimmermann.html?p=1' + str(i)
            yield scrapy.Request(url, callback=self.parse_item_mytheresa, meta={'url':url})

    def parse_item_mytheresa(self, response):
        Data = response.xpath("//ul[contains(@class,'products-grid ')]//li[contains(@class,'item')]")
        for row in Data:
            Item = {}
            #Item['URL'] = response.meta['url'] 
            Item['Item Name'] = row.xpath(".//h2[@class='product-name']//a/text()").get()
            Item['Item Price'] = row.xpath(".//div[@class='price-box']//span[@class='price']/text()").get()
            yield(Item)