import scrapy,json,cloudscraper,time
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'indeed'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','mobile': False },delay=10)
    def start_requests(self):
        start=0
        url='https://www.indeed.com/cmp/Baxter-1/reviews?fcountry=US&floc=Bloomington%2C+IN&ftopic=mgmt&start='+str(start)
        yield scrapy.Request(url,callback=self.parse,meta={'start':start})
    def parse(self, response):
        start=response.meta['start']
        HTML=None
        while HTML is None:
            try:
                HTML=self.scraper.get(response.url)
            except:
                print('Wait 3 seconds !!!')
                time.sleep(3)
        RES=scrapy.Selector(text=HTML.text)
        Data_str=RES.xpath('//script[@id="comp-initialData"]/text()').get()
        Data=json.loads(Data_str)
        data=Data['reviewsList']
        data['items'].append(data['featuredReview'])
        for row in data['items']:
            item={}
            item['start']=row['overallRating']
            item['title']=row['title']['text']
            item['position']=row['normJobTitle']
            if row['currentEmployee']==True:
                item['is_current']='Current Employee'
            else:
                item['is_current']='Former Employee'
            item['lcation']=row['location']
            item['date']=row['submissionDate']
            item['review_text']=row['text']['text']
            item['pros_text']=''
            if 'pros' in row:
                item['pros_text']=row['pros']['text']
            item['cons_text']=''
            if 'cons' in row:
                item['cons_text']=row['cons']['text']
            item['helpful']=row['helpful']
            item['unhelpful']=row['unhelpful']
            yield(item)
        if len(data['items'])>10:
            start+=20
            url='https://www.indeed.com/cmp/Baxter-1/reviews?fcountry=US&floc=Bloomington%2C+IN&ftopic=mgmt&start='+str(start)
            yield scrapy.Request(url,callback=self.parse,meta={'start':start})