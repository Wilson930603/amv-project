import scrapy,json,csv,os
from os import path
class CrawlerSpider(scrapy.Spider):
    name = 'loja'
    def start_requests(self):
        url='https://www.loja.santahelena.com/144?map=productClusterIds&page=1'
        if path.exists("loja.csv"):
            os.remove("loja.csv")
        with open('loja.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["url", "name", "price", "stock"]
            writer.writerow(field)
        yield scrapy.Request(url,callback=self.get_listing,meta={'page':1},dont_filter=True)
    def get_listing(self,response):
        html=response.text.split('<script type="application/ld+json">')[1].split('</script>')[0]
        Data=json.loads(html)
        for item in Data['itemListElement']:
            link = item['item']['@id']
            yield scrapy.Request(link,callback=self.parse_page,dont_filter=True)
        if len(Data['itemListElement'])>=12:
            pagenum=response.meta['page']+1
            url='https://www.loja.santahelena.com/144?map=productClusterIds&page='+str(pagenum)
            yield scrapy.Request(url,callback=self.get_listing,meta={'page':pagenum},dont_filter=True)
    def parse_page(self, response):
        url=response.url
        name=""
        price=""
        stock=""
        html=response.text.split('<script type="application/ld+json">')[1].split('</script>')[0]
        Data=json.loads(html)
        name=Data['name']
        price=Data['offers']['offers'][0]['price']
        stock=response.text.split('"AvailableQuantity":')[1].split(',')[0]
        print(url)
        with open('loja.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([url, name, price, stock])
        # print(name+" - "+str(price)+" - "+str(stock))
    #     hrefs=response.xpath('//a[@class="id id__logo id__sq_large id__linked"]/@href').getall()
    #     for href in hrefs:
    #         link = 'https://workswith.worldpay.com'+href
    #         yield scrapy.Request(link,callback=self.parse_page,dont_filter=True)
    #     if len(hrefs)>=12:
    #         pagenum=response.meta['page']+1
    #         url='https://workswith.worldpay.com/en/listing?page='+str(pagenum)
    #         yield scrapy.Request(url,callback=self.get_listing,meta={'page':pagenum},dont_filter=True)
    # def parse_page(self, response):
    #     url=response.url
    #     name=""
    #     description=""
    #     integrated_to_worldpay_product_s=""
    #     vendor=""
    #     try:
    #         name=response.xpath('//h1[@class="title"]/text()').get()
    #     except:
    #         name=""
    #     try:
    #         description=response.xpath('//div[@class="description"]/text()').get()
    #     except:
    #         description=""
    #     i=0
    #     j=0
    #     for row in response.xpath('//h1[@class="integrated-vendor-info"]').getall():
    #         if response.xpath('//h1[@class="integrated-vendor-info"]//text()').getall()[j].strip()=="Integrated to Worldpay Product(s):":
    #             integrated_to_worldpay_product_s=response.xpath('//h1[@class="integrated-vendor-info"]//a/text()').getall()[i]
    #         if response.xpath('//h1[@class="integrated-vendor-info"]//text()').getall()[j].strip()=="Vendor:":
    #             vendor=response.xpath('//h1[@class="integrated-vendor-info"]//a/text()').getall()[i]
    #         i+=1
    #         j+=2
    #     with open('worldpay.csv', 'a', newline='', encoding="utf-8") as file:
    #         writer = csv.writer(file)
    #         writer.writerow([url, name, description, integrated_to_worldpay_product_s, vendor])