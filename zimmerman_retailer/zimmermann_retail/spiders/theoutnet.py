import scrapy


class TheoutnetSpider(scrapy.Spider):
    name = "theoutnet"
    allowed_domains = ["www.theoutnet.com"]
    start_urls = ["http://www.theoutnet.com/"]

    def parse(self, response):
        for i in range(1,10):
            url = 'https://www.theoutnet.com/en-us/shop/designers/zimmermann?pageNumber=' + str(i)
            yield scrapy.Request(url, callback=self.parse_theoutnet, meta={'url':url})
        
    def parse_theoutnet(self, response):
        Data = response.xpath("//div[contains(@class,'ProductItem24__content')]")
        for row in Data:
            Item = {}
            #Item['URL'] = response.meta['url'] 
            Item['Item Name'] = row.xpath(".//span[@class='ProductItem24__name']/text()").get()
            Item['Item Price'] = row.xpath(".//span[@itemprop='price']/text()").get()
            yield(Item)
