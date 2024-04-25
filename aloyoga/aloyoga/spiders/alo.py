import scrapy,json,csv,os, requests, urllib, shutil,ast
from scrapy import Selector
class CrawlerSpider(scrapy.Spider):
    name = 'alo'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.aloyoga.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.aloyoga.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }

    data = {
        'methods': '[{"method":"reviews","params":{"pid":"6239918260404","order_metadata_fields":{},"widget_product_id":"6239918260404","data_source":"default","page":1,"host-widget":"main_widget","is_mobile":false,"pictures_per_review":10}}]',
        'app_key': 'ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv',
        'is_mobile': 'false',
        'widget_version': '2022-08-23_11-27-57',
    }
    def start_requests(self):
        urls={"6239918260404":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/6239918260404/widget/reviews","6239922061492":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/6239922061492/widget/reviews","6239909839028":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/6239909839028/widget/reviews","4520937521270":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/4520937521270/widget/reviews","6239914033332":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/6239914033332/widget/reviews","7366563954868":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/7366563954868/widget/reviews","7366572310708":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/7366572310708/widget/reviews","4546373943414":"https://staticw2.yotpo.com/batch/app_key/ohYKQnKU978xXhdov6tKkYMA1R62IqCn2kKD0aDv/domain_key/4546373943414/widget/reviews"}
        with open('alo.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Star', 'Height', 'Body Type', 'Title', 'Description', 'Size', 'Overall Fit', 'Helpful', 'Not Helpful'])
        for key, url in urls.items():
            methods = json.loads(self.data['methods'])
            methods[0]['params']['pid'] = key
            methods[0]['params']['widget_product_id'] = key
            self.data['methods'] = json.dumps(methods)
            yield scrapy.FormRequest(url,callback=self.get_reviews, method='POST', headers=self.headers,formdata = self.data, meta={'page':1},dont_filter=True)
    def get_reviews(self,response):
        result=ast.literal_eval(response.text)
        html=result[0]['result'].replace('\"','"').replace("\n","").replace("\t","")
        sel = Selector(text=html)
        reviewblock=sel.xpath('//div[contains(@class,"yotpo-regular-box")]').getall()
        for index, value in enumerate(reviewblock):
            if index != 0:
                sele = Selector(text=value)
                name=sele.xpath('//span[contains(@class,"yotpo-user-name")]/text()').get()
                starlst=sele.xpath('//span[@class="sr-only"]/text()').get().strip().split(" ")
                star=""
                if len(starlst)>1:
                    star=starlst[0]
                yuf=sele.xpath('//span[@class="yotpo-user-field-description text-s"]/text()').getall()
                height=""
                body_type=""
                for idx, ans in enumerate(yuf):
                    if ans.strip()=='Height:':
                        height=sele.xpath('//span[@class="yotpo-user-field-answer text-s"]/text()').getall()[idx]
                    if ans.strip()=='Body Type:':
                        body_type=sele.xpath('//span[@class="yotpo-user-field-answer text-s"]/text()').getall()[idx]
                title=sele.xpath('//div[@class="content-title yotpo-font-bold"]/text()').get().strip()
                des=sele.xpath('//div[@class="content-review"]/text()').get().strip()
                size=""
                over=""
                so=sele.xpath('//div[@class="yotpo-question-field-description"]/text()').getall()
                for idx, ans in enumerate(so):
                    if ans.strip()=='Size:':
                        size=sele.xpath('//div[@class="yotpo-question-field-answer"]/text()').getall()[idx]
                fit=sele.xpath('//div[@class="product-related-fields-item-title font-color-gray text-s"]/text()').getall()
                for idf, fans in enumerate(fit):
                    if fans.strip()=='Fit':
                        over=sele.xpath('//div[@class="product-related-fields-item-value"]/text()').getall()[idf].strip()
                        break
                up=sele.xpath('//span[@class="y-label yotpo-sum vote-sum"]/text()').getall()[0].strip()
                down=sele.xpath('//span[@class="y-label yotpo-sum vote-sum"]/text()').getall()[1].strip()
                with open('alo.csv', 'a', newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([name, star, height, body_type, title, des, size, over, up, down])
        pagenumlst=sel.xpath('//nav/div/a/text()').getall()
        totalpage=int(pagenumlst[len(pagenumlst)-1])
        curentpage=response.meta['page']
        if curentpage<=totalpage:
            methods = json.loads(self.data['methods'])
            methods[0]['params']['page'] = page = curentpage+1
            self.data['methods'] = json.dumps(methods)
            yield scrapy.FormRequest(response.url,callback=self.get_reviews, method='POST', headers=self.headers,formdata = self.data, meta={'page':page},dont_filter=True)