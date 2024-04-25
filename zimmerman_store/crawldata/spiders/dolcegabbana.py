import scrapy,re


class DolcegabbanaSpider(scrapy.Spider):
    name = "dolcegabbana"
    #allowed_domains = ["boutique.dolcegabbana.com"]
    start_urls = ["https://boutique.dolcegabbana.com/directory"]

    def parse(self, response):
        Data = response.xpath("//ul[@class='Directory-listLinks']//a")
        for row in Data:
            url =  "https://boutique.dolcegabbana.com/" + row.xpath("./@href").get()
            region = row.xpath(".//span/text()").get()
            yield scrapy.Request(url, callback=self.parse_region, meta={'region':region})

    def parse_region(self, response):
        Countries = response.xpath("//ul[@class='Directory-listLinks']//a")
        for row in Countries:
            url =  "https://boutique.dolcegabbana.com/" + row.xpath("./@href").get()
            region = response.meta['region']
            country = row.xpath(".//span/text()").get()
            count = int(re.findall(r'\d+',row.xpath("./@data-count").get())[0])
            # Region -> Country with single store
            if count < 2:
                city = ""
                yield scrapy.Request(url, callback=self.parse_details_single, meta={'region':region, 'country':country, 'city':city})
            # Region -> Country with multiple stores
            else:
                yield scrapy.Request(url, callback=self.parse_country, meta={'region':region, 'country':country})

    def parse_country(self, response):
        Cities = response.xpath("//ul[@class='Directory-listLinks']//a")
        region = response.meta['region']
        country = response.meta['country']
        # Country -> Cities
        if len(Cities) > 0:
            for row in Cities:
                url =  "https://boutique.dolcegabbana.com/" + row.xpath("./@href").get()
                city = row.xpath(".//span/text()").get()
                count = int(re.findall(r'\d+',row.xpath("./@data-count").get())[0])
                # City -> Single store
                if count < 2:
                    yield scrapy.Request(url, callback=self.parse_details_single, meta={'region':region, 'country':country, 'city':city})
                # City -> Multiple stores
                else:
                    yield scrapy.Request(url, callback=self.parse_city, meta={'region':region, 'country':country,'city': city})
        # Country -> Multiple stores
        else:
            Stores = response.xpath("//h2[@class='Teaser-title']//a")
            for row in Stores:
                url = "https://boutique.dolcegabbana.com/" + row.xpath("./@href").get().strip('../')
                region = response.meta['region']
                country = response.meta['country']
                city = ''
                yield scrapy.Request(url, callback=self.parse_details_single, meta={'region':region, 'country':country, 'city':city})

    def parse_city(self, response):
        Stores = response.xpath("//h2[@class='Teaser-title']//a")
        for row in Stores:
            url = "https://boutique.dolcegabbana.com/" + row.xpath("./@href").get().strip('../')
            region = response.meta['region']
            country = response.meta['country']
            city = response.meta['city']
            yield scrapy.Request(url, callback=self.parse_details_single, meta={'region':region, 'country':country, 'city':city})

    def parse_details_single(self, response):
        Item = {}
        Item['Region'] = response.meta['region']
        Item['Country'] = response.meta['country']
        Item['City'] = response.meta['city']
        Item['Title'] = response.xpath('//div[@class="Core-titleWrapper"]//span[@class="Core-geo"]/text()').get()
        Address1=response.xpath('//address/div[@class="c-AddressRow"]//span[@class="c-address-street-1"]/text()').get().strip('c/o ')
        Address2=response.xpath('//address/div[@class="c-AddressRow"]//span[@class="c-address-street-2"]/text()').get()
        Item['Address'] = str(Address1) + ', ' + str(Address2)
        Item['Address'] = Item['Address'].strip('c/o')
        yield(Item)

    pass

