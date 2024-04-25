import scrapy,json,re,requests,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'tripadvisor'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'content-type': 'application/json',
    'x-requested-by': 'TNI1625!AKQf6Kts5FaGnY9iEeZFV0sf0LE+Q7uS0P0D5xgbuhi6IclncZeovZJyNi8EpiLvqGsYKoEyvMg0stPamoUV50H1zNvJMf7aKUr1Z1VoeoEDumIuioqyPF3BwJgnA2HKj5fxVKLFJd/8rsgKmNtsGKcXb3v/X9D2E2CHi+dufMOQ',
    'Origin': 'https://www.tripadvisor.com',
    'Proxy-Authorization': 'Basic a3pDSWpmazhnN091YjRTN3Ytb3k5VXBaZC13NndNM2FOemV3TW8tUDRCNjk3b2pMMUJhV0UyMllOSEVsczZFUmRxUDRVSDBWUjVFbUUweTVjYkpIaFpXUGE5V0lfcjBBM25HOElxUU1tT1U9OjE=',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    url='https://www.tripadvisor.com/data/graphql/ids'
    def start_requests(self):
        URLS=re.split('\r\n|\n',open('urls.txt','r',encoding='utf-8').read())
        for url in URLS:
            urls=str(url).split('/')[3]
            ids=str(urls).split('-')
            G=int(Get_Number(ids[1]))
            D=int(Get_Number(ids[2]))
            offset=0            
            yield scrapy.Request(self.URL,callback=self.parse,meta={'D':D,'G':G,'offset':offset},dont_filter=True)
    def parse(self, response):
        D=response.meta['D']
        G=response.meta['G']
        offset=response.meta['offset']
        json_data = [{'query': '0eb3cf00f96dd65239a88a6e12769ae1','variables': {'interaction': {'productInteraction': {'interaction_type': 'CLICK','site': {'site_name': 'ta','site_business_unit': 'Hotels','site_domain': 'www.tripadvisor.com',},'pageview': {'pageview_request_uid': '4529fcb0-a4b4-4b8b-86cb-cd1cf4f9119f','pageview_attributes': {'location_id': D,'geo_id': G,'servlet_name': 'Hotel_Review',},},'user': {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0','site_persistent_user_uid': 'web373a.42.116.168.136.187E07639B8','unique_user_identifiers': {'session_id': '122FCB8646B14F409E03B2656F8B233A',},},'search': {},'item_group': {'item_group_collection_key': '4529fcb0-a4b4-4b8b-86cb-cd1cf4f9119f',},'item': {'product_type': 'Hotels','item_id_type': 'ta-location-id','item_id': D,'item_attributes': {'element_type': '','action_name': 'REVIEW_FILTER_LANGUAGE',},},},},},},{'query': '05ee4484c857bedd3a8bb64a1642744c','variables': {'key': 'locationReviewFilters_'+str(D),'val': '[]',},},{'query': 'ea9aad8c98a6b21ee6d510fb765a6522','variables': {'locationId': D,'offset': offset,'filters': [],'prefs': None,'initialPrefs': {},'limit': 10,'filterCacheKey': None,'prefsCacheKey': 'locationReviewPrefs_'+str(D),'needKeywords': False,'keywordVariant': 'location_keywords_v2_llr_order_30_en',},},]
        response = requests.post(self.url, headers=self.headers, json=json_data)
        Data=json.loads(response.text)
        for row in Data:
            if 'data' in row:
                rs=row['data']
                if 'locations' in rs:
                    rcs=rs['locations']
                    for rc in rcs:
                        data=rc['reviewListPage']['reviews']
                        for rs1 in data:
                            item={}
                            item['KEY_']=rs1['id']
                            item['url']='https://www.tripadvisor.com'+rc['url']
                            item['review_url']='https://www.tripadvisor.com'+rs1['url']
                            item['name']=rs1['userProfile']['displayName']
                            try:
                                item['country']=rs1['userProfile']['hometown']['location']['additionalNames']['long']
                            except:
                                item['country']=''
                            item['review_date']=rs1['createdDate']
                            item['review_score']=rs1['rating']
                            item['review_title']=rs1['title']
                            item['review_text']=rs1['text']
                            item['reservation_date']=rs1['tripInfo']['stayDate']
                            for r in rs1['additionalRatings']:
                                item[str(r['ratingLabel']).lower().replace(' ','_')]=r['rating']
                            yield(item)
                        if len(data)>=10:
                            offset+=10
                            yield scrapy.Request(self.URL,callback=self.parse,meta={'D':D,'G':G,'offset':offset},dont_filter=True)