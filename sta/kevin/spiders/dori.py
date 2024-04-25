import scrapy,json,csv,os
from os import path
class CrawlerSpider(scrapy.Spider):
    name = 'dori'
    start_urls = ['https://dori.com.br/pettiz','https://dori.com.br/dori-snacks-salgados','https://dori.com.br/dori-snacks-doces','https://dori.com.br/gomets','https://dori.com.br/jubes','https://dori.com.br/deliket','https://dori.com.br/dori-granulado','https://dori.com.br/chococandy','https://dori.com.br/yogurte100','https://dori.com.br/bolete','https://dori.com.br/lua-cheia']
    def start_requests(self):
        for url in self.start_urls:
            if path.exists("dori.csv"):
                os.remove("dori.csv")
            with open('dori.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                field = ["url", "name"]
                writer.writerow(field)
            yield scrapy.Request(url,callback=self.get_listing,meta={'page':1},dont_filter=True)
    def get_listing(self,response):
        cururl=response.url
        hrefs=response.xpath('//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href').getall()
        i=1
        for href in hrefs:
            url=href
            name=response.xpath('//h2/text()').getall()[i]
            with open('dori.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([url, name])
            i+=1
        if len(hrefs)>=9:
            pagenum=response.meta['page']+1
            if pagenum==2:
                url=str(cururl)+"/page/"+str(pagenum)
            else:
                url=str(cururl).replace(str(response.meta['page']),str(pagenum))
            print(url)
            yield scrapy.Request(url,callback=self.get_listing,meta={'page':pagenum},dont_filter=True)