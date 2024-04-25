import scrapy,json,re
from crawldata.functions import *
from datetime import datetime
from urllib.parse import unquote
class CrawlerSpider(scrapy.Spider):
    name = 'classpass'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    IDS=[]
    headers_json = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0','Accept': '*/*','Accept-Language': 'en-US','Content-Type': 'application/json','platform': 'web','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-GB,en;q=0.5','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1'}
    def start_requests(self):
        url='https://classpass.com/locations'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True,headers=self.headers)
    def parse(self, response):
        Data=response.xpath('//main//li//a')
        for row in Data:
            item={}
            item['location']=row.xpath('./text()').get()
            item['link']=row.xpath('./@href').get()
            if item['location']:
                item['location_id']=str(item['link']).split('/')[-1]
                json_data = {'autocomplete_type': 'geocode','query': item['location']}
                url='https://classpass.com/_api/unisearch/v1/location/autocomplete'
                yield scrapy.Request(url,callback=self.parse_location,meta={'ITEM':item},method="POST",body=json.dumps(json_data),headers=self.headers_json)
    def parse_location(self,response):
        ITEM=response.meta['ITEM']
        Data=json.loads(response.text)
        ITEM['place_id']=Data['data']['predictions'][0]['place_id']
        url='https://classpass.com/_api/unisearch/v1/location/details/'+ITEM['place_id']
        yield scrapy.Request(url,callback=self.parse_plance,meta={'ITEM':ITEM},headers=self.headers_json)
    def parse_plance(self,response):
        ITEM=response.meta['ITEM']
        Data=json.loads(response.text)
        row=Data['data']
        json_data = {'search_request': {'filters': {'date': datetime.now().strftime('%Y-%m-%d'),'lat': row['lat'],'lon': row['lon'],'place_id': row['place_id'],'result_type': 'VENUE','vertical': 'fitness','tag': [],'map_bounds': str(row['viewport_south_west_lon'])+','+str(row['viewport_south_west_lat'])+','+str(row['viewport_north_east_lon'])+','+str(row['viewport_north_east_lat'])},'venue_search_options': {'page_size': 50,'include_map_items': False}}}
        url='https://classpass.com/_api/unisearch/v1/layout/web_search_page'
        yield scrapy.Request(url,callback=self.parse_first_page,meta={'ITEM':ITEM},method="POST",body=json.dumps(json_data),headers=self.headers_json)
    def parse_first_page(self,response):
        ITEM=response.meta['ITEM']
        DATA=json.loads(response.text)
        Data=DATA['data']['modules']['web_search_results_01']['data']
        for row in Data['venue_tab_items']:
            if not row['venue_id'] in self.IDS:
                self.IDS.append(row['venue_id'])
                url='https://classpass.com/studios/'+row['alias']
                yield scrapy.Request(url,callback=self.parse_data,headers=self.headers,meta={'ITEM':ITEM})
            else:
                print('Existed: ',row['venue_id'])
        if len(Data['venue_tab_items'])>=50:
            json_data = {"search_request":{"cursor":Data['cursor']},"modules":["web_search_results_01"]}
            url='https://classpass.com/_api/unisearch/v1/layout/web_search_page'
            yield scrapy.Request(url,callback=self.parse_first_page,meta={'ITEM':ITEM},method="POST",body=json.dumps(json_data),headers=self.headers_json)
    def parse_data(self,response):
        ITEM=response.meta['ITEM']
        HTML=response.xpath('//script[@id="store"]/text()').get()
        DATA=json.loads(HTML)
        Data=DATA['entities']['venueByIdV2']['data']
        for K,row in Data.items():
            item={}
            item['URL']='https://classpass.com/studios/'+row['alias']
            try:
                item['Name']=row['name']+' - '+row['address']['city']
            except:
                item['Name']=row['name']
            item['Rating']=row['ratings']['mean']
            ADD=[]
            for k,v in row['address'].items():
                if v:
                    ADD.append(v)
            item['Address']=', '.join(ADD)
            item['Phone']=row.get('phone_number','')
            item['Website']=row.get('website','')
            item['Instagram']=row.get('instagram_handle','')
            item['Facebook']=row.get('facebook_page_url','')
            item['Twitter']=row.get('twitter','')
            yield(item)


        

        
