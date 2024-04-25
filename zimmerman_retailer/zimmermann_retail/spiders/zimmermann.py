import scrapy


class ZimmermannSpider(scrapy.Spider):
    name = "zimmermann"
    start_urls = ["https://www.zimmermann.com/us/swim",
                  "https://www.zimmermann.com/us/ready-to-wear"]

    def parse(self, response):
        Page_Count = int(response.xpath("//div[@id='am-page-count']/text()").get())
        #print(Page_Count)
        collection_url = response.request.url + "?p="
        for i in range(1,Page_Count + 1):
            url = collection_url + str(i)
            yield scrapy.Request(url, callback=self.parse_item, meta=response.meta)
    
    def parse_item(self, response):
        Data = response.xpath("//ul[@class='catalog-grid-item__wrapper']//section")
        for row in Data:
            Item = {}
            Item['Collection'] = "Swim & Resort" if response.request.url.find('swim') > 0 else "Ready To Wear"
            Item['Item Name']  = row.xpath(".//a/text()").get()
            Item['Item Price'] = row.xpath(".//span[@class='price']/text()").get()
            if not Item['Item Name'] is None:
                Item['Item Name']  = Item['Item Name'].strip()
                yield(Item)
        pass