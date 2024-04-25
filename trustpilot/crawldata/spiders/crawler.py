import scrapy,json,dateparser
from crawldata.functions import *
from datetime import timedelta
class CrawlerSpider(scrapy.Spider):
    name = 'trustpilot'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0','Accept': '*/*','Accept-Language': 'en-GB,en;q=0.5','x-nextjs-data': '1','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'no-cors','Sec-Fetch-Site': 'same-origin','Pragma': 'no-cache','Cache-Control': 'no-cache'}
    def start_requests(self):
        f=open('urls.txt','r',encoding='utf-8')
        URLS=re.split('\r\n|\n', f.read())
        f.close()
        for URL in URLS:
            ID=(str(URL).split('/')[-1]).split('?')[0]
            page=1
            url='https://www.trustpilot.com/_next/data/businessunitprofile-consumersite-7597/review/'+ID+'.json?businessUnit='+ID+'&languages=all'
            yield scrapy.Request(url,callback=self.parse,meta={'ID':ID,'page':page},dont_filter=True,headers=self.headers)
    def parse(self,response):
        ID=response.meta['ID']
        page=response.meta['page']
        DATA=json.loads(response.text)
        Data=DATA['pageProps']['reviews']
        for row in Data:
            item={}
            item['KEY_']=row['id']
            item['Web_review']=ID
            item['Username']=row['consumer']['displayName']
            item['Location']=row['consumer']['countryCode']
            item['Number of Stars']=row['rating']
            item['Title']=row['title']
            item['Review']=row['text']
            if row['dates']['updatedDate']:
                item['Date of Review']=(dateparser.parse(row['dates']['updatedDate'])+timedelta(hours=7)).strftime('%Y-%m-%d')
            else:
                item['Date of Review']=(dateparser.parse(row['dates']['publishedDate'])+timedelta(hours=7)).strftime('%Y-%m-%d')
            if row['dates']['experiencedDate']:
                item['Date of Experience']=(dateparser.parse(row['dates']['experiencedDate'])+timedelta(hours=7)).strftime('%Y-%m-%d')
            else:
                item['Date of Experience']=item['Date of Review']
            item['Reply']=''
            item['Date of Reply']=''
            if 'reply' in row and row['reply']:
                item['Reply']=row['reply'].get('message','')
                if row['reply']['publishedDate']:
                    item['Date of Reply']=(dateparser.parse(row['reply']['publishedDate'])+timedelta(hours=7)).strftime('%Y-%m-%d')
            item['URL of Review']='https://www.trustpilot.com/reviews/'+row['id']
            yield(item)
        if len(Data)>=20:
            page+=1
            url='https://www.trustpilot.com/_next/data/businessunitprofile-consumersite-7597/review/'+ID+'.json?languages=all&page='+str(page)+'&businessUnit='+ID
            yield scrapy.Request(url,callback=self.parse,meta={'ID':ID,'page':page},dont_filter=True,headers=self.headers)