from scrapy import Request, Selector,Spider

import pandas as pd
import json
from datetime import datetime
import os
try:
    from ..items import AmazonreviewsItem, AmazonUrls
except:
    from items import AmazonreviewsItem, AmazonUrls
from random import randint

import re
class Spider_Amazon(Spider):
    name = 'amazon'
    base_urlUS = "https://www.amazon.com"
    base_urlUK = "https://www.amazon.co.uk"
    #download_delay = 1.8
    error =0
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48',
        'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    
        ]

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://www.amazon.com',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agents[randint(0,len(user_agents)-1)],
        'Cookie': 'audience=new-user;'
    }
    headers_reviews = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "referer": "https://www.amazon.com/Liquid-I-V-Multiplier-Electrolyte-Supplement/dp/B01IT9NLHW/ref=sr_1_1?keywords=liquid%2Biv&qid=1676553036&sr=8-1&th=1",
        "sec-ch-dpr": "1.25",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "sec-ch-viewport-width": "1229",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "viewport-width": "1229",
    }
    headers_product = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "sec-ch-viewport-width": "1229",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "viewport-width": "1229",
    }
    def rotate_headers(self , ref='',headers = None):
        
        user_agents = self.user_agents
        if headers is None:
            headers = self.headers
        
        headers["user-agent"] = user_agents[randint(0, len(user_agents) - 1)]
        if ref != '':
            headers['referer'] = ref
        return headers


    def __init__(self):
        df = pd.read_csv('./inputFiles/USbrands.csv')
        self.brands = [df.iloc[i]['Amazon Brands'] for i in range(len(df))]
        self.links = [df.iloc[i]['URL'] for i in range(len(df))]
        
    def start_requests(self):

        for count,url in enumerate(self.links):
            if '/stores/' in url:
                yield Request(
                    url,
                    callback=self.parse_store,
                    dont_filter=True,
                    headers=self.rotate_headers(), 
                    meta={'brand':self.brands[count]}
                )
            else:
                continue  
                yield Request(
                    url,
                    callback=self.parse_page,
                    dont_filter=True,
                    headers=self.rotate_headers(), 
                    meta={
                        'brand':self.brands[count]
                        }
                )
            break
    def parse_store(self,response):
        if response.css('#captchacharacters').extract_first():
            print('Captcha Found During Parse Store And App Try To Enable Proxy')

        brand = response.meta.get('brand')
        categories = ['Home']+response.xpath('//li[contains(@data-testid,"nav-item")]//a/span/text()').extract()
        catLinks = response.xpath('//li[contains(@data-testid,"nav-item")]//a/@href').extract()
        for itr in range(len(catLinks)):
            if self.base_urlUK is response.url:
                catLink = self.base_urlUK+catLinks[itr]
            else:
                catLink = self.base_urlUS+catLinks[itr]
            yield Request(
                catLink,
                callback=
                self.parse_category,
                headers=self.rotate_headers(ref=response.url), 
                meta={
                    'brand':brand,
                    }
                )

    def check_none(self,data):
        """
        If the data is None or an empty string, return 'N/A', otherwise return the data
        
        :param data: The data to be checked
        :return: the data if it is not None or empty.
        """
        if data == None or data == '':
            return 'N/A'
        return data

    def parse_category(self,response):
        if response.css('#captchacharacters').extract_first():
            print('Captcha Found During Parse Category And App Try To Enable Proxy')
        brand = response.meta.get('brand')
        script = response.xpath('//script[contains(text(),"var config =")]/text()').extract()[-1]
        formatedScript = script.split('var config = ')[-1].split('var widgetDOM')[0].strip()[:-1]
        try:

            jdata = json.loads(formatedScript)
        except:
            return
        try:
            temp = ''
            for product in jdata.get('content').get('products'):
                if self.base_urlUK in response.url:
                    pUrl = self.base_urlUK+product.get('links').get('viewOnAmazon').get('url')
                    temp = self.base_urlUK
                else:    
                    temp = self.base_urlUS
                    pUrl = self.base_urlUS+product.get('links').get('viewOnAmazon').get('url')
                if 'sspa/click?ie=' in pUrl:
                    print('Sponsor Product')
                    continue
                pUrl = pUrl.split('/ref')[0]
                item = AmazonUrls()
                item['brand'] = brand
                item['url'] = pUrl
                yield item
        except Exception as e:
            if self.base_urlUK in response.url:
                temp = self.base_urlUK
            else:    
                temp = self.base_urlUS
            url_asins = 'https://www.amazon.com/dp/'
            asins =[]
            for product in jdata.get('tiles'):
                if product.get('content').get('requestedAsins'):
                    [asins.append(x) for x in product.get('content').get('requestedAsins')]
            asins = set(asins)
            for asin in asins:
                item = AmazonUrls()
                item['brand'] = brand
                item['url'] = url_asins+asin
                yield item
    def parse_page(self,response):
        if response.css('#captchacharacters').extract_first():
            print("Captcha Found During Parse Page And App Try To Enable Proxy")
            yield Request(
                response.url,
                callback=self.parse_page,
                dont_filter=True,
                headers=self.rotate_headers(ref=response.url),
                meta={
                    "brand": response.meta.get("brand"),
                },
                
            )
        brand = response.meta.get('brand')

        productLinks = response.xpath('//h2/a/@href').extract()
        for product in productLinks:
            if self.base_urlUK in response.url:
                newProductLink = self.base_urlUK+product
            else:
                newProductLink = self.base_urlUS+product
            item = AmazonUrls()
            item['brand'] = brand
            if 'sspa/click?ie=' in newProductLink:
                print('Sponsor Product')
                item['url'] = newProductLink
                yield item
                continue

            newProductLink = newProductLink.split('/ref')[0]
            item['url'] = newProductLink
            yield item
        nextPage = response.xpath('//a[contains(@aria-label,"Go to next page,")]/@href').get()
        if nextPage:
            if self.base_urlUK in response.url:
                nextUrl = self.base_urlUK+nextPage
            else:
                nextUrl = self.base_urlUS+nextPage

            headers = self.rotate_headers(ref=response.url,headers=self.headers_product)
            yield Request(
                nextUrl,
                callback=self.parse_page,
                headers=headers,
                meta={"brand": brand},
                
            )
    
    

            

            

            
