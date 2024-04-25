import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'franchisetimes'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        o=0
        url='https://www.franchisetimes.com/search/?bl=1421000&o=0&l=25&f=json&altf=widget'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        DATA=json.loads(response.text)
        Data=DATA['assets']
        for row in Data:
            item={}
            item['Rank']=row['rank']
            item['Name']=row['name']
            item['System Sales']=Get_Number(row['sales'])
            item['Total Locations']=Get_Number(row['loc'])
            yield(item)
        if DATA['next']>0:
            url='https://www.franchisetimes.com/search/?bl=1421000&o='+str(DATA['next'])+'&l=25&f=json&altf=widget'
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)