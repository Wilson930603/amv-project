import scrapy,json,csv,os, requests, urllib, shutil,ast
from scrapy import Selector
class CrawlerSpider(scrapy.Spider):
    name = 'lulu'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://shop.lululemon.com/',
        'Origin': 'https://shop.lululemon.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    params = {
        'passkey': 'e82lq5pbxy7tur5plumvaqqyz',
        'ApiVersion': '5.4',
        'filter': [
            'productId:Align_Pant_Full_Length_28',
            'submissionTime:gt:1514739600',
            'ContentLocale:en_US',
        ],
        'FilteredStats': 'Reviews',
        'Include': 'Products',
        'Offset': '0',
        'Limit': '16',
        'Sort': 'SubmissionTime:desc',
        'search': '',
        'Locale': 'en_US',
    }
    def start_requests(self):
        proIdlst=["Align_Pant_Full_Length_28","Align_Pant_2","Align_Short_6","The_Mat_5mm","Flow_Y_Bra_Nulu","Strongfeel_Womens_Training_Shoe","Swiftly_Tech_SS_2","Align_Tank"]
        with open('lulu.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Stars', 'Title', 'Description', 'Date', 'Fits', 'Helpful'])
        for proid in proIdlst:
            del self.params['filter'][0]
            self.params['filter'].insert(0,'productId:'+proid)
            url="https://api.bazaarvoice.com/data/reviews.json"
            yield scrapy.FormRequest(url,callback=self.get_reviews, method='GET', headers=self.headers,formdata = self.params, meta={'params':self.params},dont_filter=True)
    def get_reviews(self,response):
        Data=json.loads(response.text)
        for item in Data['Results']:
            Name=item['UserNickname']
            Stars=item['Rating']
            Title=item['Title']
            Desc=item['ReviewText']
            Date=item['LastModificationTime'].split('T')[0]
            try:
                Fit=item['SecondaryRatings']['Fit_22']['ValueLabel']
            except:
                Fit=""
            if item['Helpfulness'] is None:
                Helpfulness=0
            else:
                Helpfulness=item['Helpfulness']
            with open('lulu.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([Name,Stars,Title,Desc,Date,Fit,Helpfulness])
        if len(Data['Results']) >= 16:
            params=response.meta['params']
            Offset = params['Offset']
            N_Offset = str(int(Offset)+16)
            params['Offset'] = N_Offset
            url=response.url
            yield scrapy.FormRequest(url,callback=self.get_reviews, method='GET', headers=self.headers,formdata = params,meta={'params':params},dont_filter=True)
        # open('lulu2.txt','a',encoding='utf-8').write(response.text)