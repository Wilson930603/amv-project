import scrapy


class NetAPorterSpider(scrapy.Spider):
    name = "net-a-porter"
    #allowed_domains = ["net-a-porter.com"]
    start_urls = ["https://www.net-a-porter.com"]
    pages = 4

    def parse(self, response):
        for i in range(1, self.pages + 1):
            url = 'https://www.net-a-porter.com/en-us/shop/designer/zimmermann?pageNumber=' + str(i)
            yield scrapy.Request(url, callback=self.parse_item_netaporter, meta={'url':url})

    def parse_item_netaporter(self, response):
        Data = response.xpath("//div[@itemprop='item']")
        for row in Data:
            Item = {}
            #Item['URL'] = response.meta['url'] 
            Item['Item Name'] = row.xpath(".//span[@itemprop='name']/text()").get()
            Item['Item Price'] = row.xpath(".//span[@itemprop='price']/text()").get()
            yield(Item)