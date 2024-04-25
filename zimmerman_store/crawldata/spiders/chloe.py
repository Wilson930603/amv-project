import scrapy,json
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'chloe'
    #https://www.chloe.com/experience/us/boutiques/#search/coords/-3.7779621699060613,18.445181813782597/ne/73.35665080031822,173.6600255637826/sw/-80.91257514013034,-136.7696619362174/store-type/chloe,see-by-chloe
    start_urls=['https://www.chloe.com/experience/us/?yoox_storelocator_action=true&action=yoox_storelocator_get_all_stores']
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def parse(self, response):
        Data=json.loads(response.text)
        for row in Data:
            CHK=False
            for rs in row['store-type']:
                if rs['slug'] in ['see-by-chloe','chloe']:
                    CHK=True
            if CHK==True:
                item={}
                item['Country']=row['location']['country']['name']
                item['Title']=row['post_title']
                item['Address']=row['wpcf-yoox-store-geolocation-address']+', '+item['Country']
                yield(item)
