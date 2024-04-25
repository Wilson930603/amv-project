import scrapy


class GanniCrawlSpider(scrapy.Spider):
    name = "ganni_crawl"
    allowed_domains = ["www.ganni.com"]
    start_urls = ["http://www.ganni.com/en/stores-find"]

    def parse(self, response):
        Data = response.xpath('//div[@class="b-store-tiles-section__content"]')
        for row in Data:
            Country = row.xpath('./div[@class="b-store-tiles-section__title"]/text()').get()
            if Country:
                data = row.xpath('.//div[@class="b-store-tile js-store-tile "]')
                # print(data)
                # print(str(Country).split(maxsplit=1)[0].strip())
                for rs in data:
                    item = {}
                    item['Country'] = str(Country).rsplit(' ', 1)[0].strip()
                    item['Title'] = str(rs.xpath('.//h6[@class="b-store-tile__content-title"]/text()').get()).strip().title()
                    item['Address'] = str(rs.xpath('.//div[@class="b-store-tile__content"]//address/text()').get()).strip().replace("\n", " ")
                    yield(item)
