import scrapy,json,csv,os
from os import path
class CrawlerSpider(scrapy.Spider):
    name = 'dacolonia'
    cookies = {
        '_gcl_au': '1.1.1085429012.1687743343',
        'owa_v': 'cdh%3D%3E87b417ba%7C%7C%7Cvid%3D%3E1687743343978326537%7C%7C%7Cfsts%3D%3E1687743343%7C%7C%7Cdsfs%3D%3E0%7C%7C%7Cnps%3D%3E2',
        '_mddcom': '{}',
        '_ca-mdd': '{}',
        '_lf': '{%22lm%22:false%2C%22_ga%22:%2221781ff3-3561-c54f-7b2f-73ece9bfd085%22}',
        '_lfi': '3',
        '_lfe': '3',
        '_enviou.com-ca': '{%22tk%22:%2221052021045214ZTT%22}',
        '_ga': 'GA1.3.1124204779.1687743350',
        '_gid': 'GA1.3.1997290404.1687743350',
        '_fbp': 'fb.2.1687743355307.955306409',
        'showModalNews': 'hide',
        'owa_s': 'cdh%3D%3E87b417ba%7C%7C%7Clast_req%3D%3E1687770000%7C%7C%7Csid%3D%3E1687764106066433465%7C%7C%7Cdsps%3D%3E0%7C%7C%7Creferer%3D%3E%28none%29%7C%7C%7Cmedium%3D%3Edirect%7C%7C%7Csource%3D%3E%28none%29%7C%7C%7Csearch_terms%3D%3E%28none%29',
        'AvisoCookie': '1630047685223',
        '_gat': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://loja.dacolonia.com.br/pacoquinha-rolha-zero-acucar-pote-com-32-un-de-18g-cada',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
        # 'Cookie': '_gcl_au=1.1.1085429012.1687743343; owa_v=cdh%3D%3E87b417ba%7C%7C%7Cvid%3D%3E1687743343978326537%7C%7C%7Cfsts%3D%3E1687743343%7C%7C%7Cdsfs%3D%3E0%7C%7C%7Cnps%3D%3E2; _mddcom={}; _ca-mdd={}; _lf={%22lm%22:false%2C%22_ga%22:%2221781ff3-3561-c54f-7b2f-73ece9bfd085%22}; _lfi=3; _lfe=3; _enviou.com-ca={%22tk%22:%2221052021045214ZTT%22}; _ga=GA1.3.1124204779.1687743350; _gid=GA1.3.1997290404.1687743350; _fbp=fb.2.1687743355307.955306409; showModalNews=hide; owa_s=cdh%3D%3E87b417ba%7C%7C%7Clast_req%3D%3E1687770000%7C%7C%7Csid%3D%3E1687764106066433465%7C%7C%7Cdsps%3D%3E0%7C%7C%7Creferer%3D%3E%28none%29%7C%7C%7Cmedium%3D%3Edirect%7C%7C%7Csource%3D%3E%28none%29%7C%7C%7Csearch_terms%3D%3E%28none%29; AvisoCookie=1630047685223; _gat=1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    products=[]
    def start_requests(self):
        url='https://loja.dacolonia.com.br/'
        if path.exists("dacolonia.csv"):
            os.remove("dacolonia.csv")
        with open('dacolonia.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["url", "category", "name", "original_price", "discounted_price", "pix_price"]
            writer.writerow(field)
        yield scrapy.Request(url,callback=self.get_category, headers=self.headers,cookies=self.cookies, dont_filter=True)
    def get_category(self,response):
        hrefs=response.xpath('//ul[@class="nivel-um"]//a/@href').getall()
        for href in hrefs:
            yield scrapy.Request(href,callback=self.get_listing, headers=self.headers,cookies=self.cookies, dont_filter=True)
    def get_listing(self,response):
        hrefs=response.xpath('//a[@class="nome-produto cor-secundaria"]//@href').getall()
        for href in hrefs:
            if href not in self.products:
                link = href
                self.products.append(link)
                yield scrapy.Request(link,callback=self.parse_page, headers=self.headers,cookies=self.cookies, dont_filter=True)
    def parse_page(self, response):
        url=response.url
        category=""
        name=""
        original_price=""
        discounted_price=""
        pix_price=""
        html=response.xpath('//div[@class="breadcrumbs borda-alpha "]//ul//li//a/text()').getall()
        # print(str(html))
        category=html[len(html)-1].strip()
        name=response.xpath('//h1/text()').get().strip()
        opt=response.xpath('//span[@class="avise-tit"]').getall()
        if len(opt)<=1:
            try:
                original_price=response.xpath('//s[@class="preco-venda "]/text()').get().replace('R$ ','').strip()
            except:
                original_price=response.xpath('//strong[@class="cor-principal titulo"]/text()').get().replace('R$ ','').strip()
            try:
                discounted_price=response.xpath('//strong[@class="preco-promocional cor-principal "]/text()').get().replace('R$ ','').strip()
            except:
                discounted_price=response.xpath('//strong[@class="preco-promocional cor-principal titulo"]/text()').get().replace('R$ ','').strip()
            try:
                pix_price=response.xpath('//strong[@class="cor-secundaria"]/text()').get().replace('R$ ','').strip()
            except:
                pix_price=""
        with open('dacolonia.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([url, category, name, original_price, discounted_price, pix_price])