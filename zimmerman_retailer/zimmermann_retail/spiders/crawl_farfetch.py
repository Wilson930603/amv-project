import scrapy


class CrawlFarfetchSpider(scrapy.Spider):
    name = "crawl_farfetch"
    allowed_domains = ["www.farfetch.com"]
    start_urls = ["http://www.farfetch.com/vn/shopping/women/zimmermann/items.aspx?page=1"]

    def parse(self, response):
        products = response.xpath('//li[@data-testid="productCard"]')

        for product in products:
            items = {
                'Season' : product.xpath('.//div[@data-component="ProductCardInfo"]//p[@class="ltr-8h1fa5-Body e3gfwc50"]/text()').get(),
                'Item Name' : product.xpath('.//div[@data-component="ProductCardInfoClamp"]//p[@class="ltr-4y8w0i-Body"]/text()').get(),
                'Price' : product.xpath('.//div[@class="ltr-l3ndox"]/p/text()').get(),
            }

            yield items
        
        # extract page num from url
        current_page = int(response.url.split('=')[-1])
        
        
        if len(products) > 0:
            next_page = f"http://www.farfetch.com/vn/shopping/women/zimmermann/items.aspx?page={current_page + 1}"
            yield scrapy.Request(next_page, callback=self.parse)

    
