from audioop import add, ratecv
from cmath import inf
from ntpath import join
from subprocess import call
from urllib.parse import urljoin
import scrapy
import json
import pandas
from..items import *
import math
from time import gmtime, strftime
from..items import *
from urllib.parse import unquote
from w3lib.http import basic_auth_header
class Mytheresa(scrapy.Spider):
    name = 'mytheresa'
    download_delay = 0.5
    start_urls_dic = {
       'Women':'https://www.mytheresa.com/en-us/designers.html',
        'Men':'https://www.mytheresa.com/en-us/men/designers.html',
        'Kids':'https://www.mytheresa.com/en-us/kids/designers.html',
        'Life':'https://www.mytheresa.com/en-us/life/designers.html'
    }
    total = 0
    headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'lang': 'en',
    }
    def start_requests(self):
        """ Start request for Cars
        """
        for key in self.start_urls_dic.keys():
            yield scrapy.Request(self.start_urls_dic.get(key),headers=self.headers,callback=self.itemsurl,meta={'maincateg':key})
    def itemsurl(self,response):
        main_categ = response.meta['maincateg']
        brand = 0
        brand_arr = []
        if 'en-us/designers' in response.url:
            barnds_column=response.xpath('//div[@id="designer-list"]/div[contains(@class,"column")]/dl')
            
        else:
            barnds_column = response.xpath('//section[contains(@class,"service-section service-")]/div')
        for column in barnds_column:
            if 'en-us/designers' in response.url:
                brands_lis = column.xpath('.//dd/ul/li')
            else:
                brands_lis = column.xpath('.//p')
            brand = brand+len(brands_lis)
       
            for lis in brands_lis:
                coming_soon = lis.xpath('.//a[2]//text()').get()
                if not coming_soon:
                    coming_soon = lis.xpath('.//a//span//text()').get()
                if coming_soon and 'coming soon' in coming_soon.lower():
                    continue
                brand_link = lis.xpath('.//a/@href').get()
                brand_name = lis.xpath('.//a//span//text()').get()
                if not brand_name:
                    brand_name = lis.xpath('.//a//text()').get()
                if brand_name!= None:
                    brand_arr.append(brand_name)
                    # frame['brannds'].append(brand_name)
                    yield scrapy.Request(brand_link,headers=self.headers,dont_filter=True,callback=self.pagination,meta={'maincateg':main_categ})
  
    def pagination(self,response):
       
        main_categ = response.meta['maincateg']
        total_products = response.xpath('//p[contains(@class,"amount amount")]//text()').get()
        if not total_products:
            return
        else:
            total_products = total_products.strip().split()[0]
        self.total = self.total+int(total_products)
        per_page_len = response.xpath('//ul[contains(@class,"products-grid products-grid")]/li[contains(@class,"item")]')
        index = math.ceil(int(total_products)/int(len(per_page_len)))
        for i in range(1,index+1):
            page_link = response.url+'?p='+str(i)
            yield scrapy.Request(page_link,headers=self.headers,dont_filter=True,callback=self.brandpage,meta={'totalproduct':total_products,'maincateg':main_categ})
    def brandpage(self,response):
        products = response.xpath('//ul[contains(@class,"products-grid products-grid")]/li[contains(@class,"item")]')
        main_categ = response.meta['maincateg']       
        total_product = response.meta['totalproduct']
        for product in products:
            product_link = product.xpath('.//a/@href').get()
            title = product.xpath('.//@title').get()
            yield scrapy.Request(product_link,headers=self.headers,dont_filter=True,callback=self.productinfo,meta={'totalproduct':total_product,'maincateg':main_categ})
    def productinfo(self,response):
        na= 'N/A'
        total_product = response.meta['totalproduct']
        brand = response.meta['brand_name']
        brand = response.xpath('//div[@class="product-designer"]/span/a//text()').get()
        product_name = response.xpath('//div[@class="product-name"]//span//text()').get()
        price = response.xpath('//span[@class="price"]//text()').get()
        discount_price = response.xpath('//p[@class="special-price"]//span[@class="price"]//text()').get()
        if discount_price == None:
            discount_price = na
        categories = response.xpath('//div[@class="breadcrumbs"]//ul/li[contains(@class,"category")]')
        main_categ = response.meta['maincateg']
        if categories:
            categories = [cate.xpath('.//a//span//text()').get()  for cate in categories[1:] if brand not in cate.xpath('.//a//span//text()').get()]
            try:
                 product_categ = categories[0]
            except:
                  product_categ = na
            try:
                product_sub = categories[1]
            except:
                product_sub = na
            try:
                product_sub_categ = categories[2]
            except:
                product_sub_categ = na
        else:
            product_categ = na
            product_sub = na
            product_sub_categ = na

        items = FartechItem()
        items['ProductURL'] = response.url
        items['MainCategory'] = main_categ
        items['Brand'] = brand
        items['BrandTotalProducts'] = total_product
        items['ProductCategory'] = product_categ
        items['ProductSubcategory'] = product_sub
        items['ProductSubsubcategory'] = product_sub_categ
        items['ProductName'] = product_name
        items['Price'] = price
        items['DiscountPrice'] = discount_price
        yield items

