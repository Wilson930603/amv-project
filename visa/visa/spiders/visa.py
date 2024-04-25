import scrapy
from random import randint
import pandas as pd
class Visa_spider(scrapy.Spider):
    name = "visa"


    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48',
            'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppwleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        ]

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'user-agent': user_agents[randint(0,len(user_agents)-1)],
        }
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        df = pd.read_csv('./links.csv')
        self.start_urls = df["URL"].to_list()
        print(len(self.start_urls))
    def start_requests(self):
        for url in self.start_urls:
            print(url)
            # break
            yield scrapy.Request(url, callback=self.information, headers=self.headers)

    
    def information(self,response):

        title = response.xpath('//h1/text()').get(default='NA')
        description = response.xpath('//div[contains(@class,"vds-text--body")]//p/text()').get(default='NA')
        website = response.xpath('//a[@class="vds-btn-text--secondary "]/@href').get(default='NA')
        capabilities = response.xpath('//h3[text()="Capability"]/..//p/text()').get(default='NA')
        countries_list = response.xpath('//div[@class="tabcontent"]')
        country= []
        for countries in countries_list:
            data = countries.xpath('.//p/text()').get(default = 'NA')
            if data !="NA":
                country.append(data)

        country = ', '.join(country)
        if country == "":
            country = "NA"
        yield {
            "URL": response.url,
            "Name":title,
            "Description":description,  
            "Website":website,
            "Capability":capabilities,
            "Countries":country

        }

        