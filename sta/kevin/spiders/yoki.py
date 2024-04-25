import scrapy,json,csv,os
from os import path
class CrawlerSpider(scrapy.Spider):
    name = 'yoki'
    start_urls = ['https://www.yoki.com.br/tipo-produto/yoki-acompanhamentos/','https://www.yoki.com.br/tipo-produto/yoki-pipocas/','https://www.yoki.com.br/tipo-produto/yoki-graos-e-cereais/','https://www.yoki.com.br/tipo-produto/yoki-farinaceos/','https://www.yoki.com.br/tipo-produto/yoki-sobremesas/','https://www.yoki.com.br/tipo-produto/yoki-salgadinhos-e-snacks/']
    def start_requests(self):
        for url in self.start_urls:
            if path.exists("yoki.csv"):
                os.remove("yoki.csv")
            with open('yoki.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                field = ["url", "name"]
                writer.writerow(field)
            yield scrapy.Request(url,callback=self.get_listing,dont_filter=True)
    def get_listing(self,response):
        # cururl=response.url
        hrefs=response.xpath('//a[@class="products-item"]/@href').getall()
        i=0
        for href in hrefs:
            print(href)
            url=href
            name=response.xpath('//span[@class="link"]/text()').getall()[i]
            with open('yoki.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([url, name])
            i+=1
        # if len(hrefs)>=9:
        #     pagenum=response.meta['page']+1
        #     url=str(cururl).replace(str(response.meta['page']),str(pagenum))
        #     print(url)
        #     yield scrapy.Request(url,callback=self.get_listing,meta={'page':pagenum},dont_filter=True)