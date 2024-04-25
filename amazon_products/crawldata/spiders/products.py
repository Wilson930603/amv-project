import scrapy,json,re,os
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'products'
    domain='https://www.amazon.com'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0','Accept': 'application/json, text/plain, */*','Accept-Language': 'en-GB,en;q=0.5','Content-Type': 'application/json; charset=utf-8','Origin': 'https://www.amazon.com','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin'}
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        URLS=re.split('\r\n|\n', open('URLS.txt').read())
        for url in URLS:
            if '/page/' in url:
                Brand=str(url).split('/')[4]
                pageid=str(url).split('/page/')[1].split('?')[0]
                ASINList=[]
                if pageid=='9440DC15-574C-41FE-A08A-AFF9B9634879':
                    searchurl=url
                    if os.path.exists(pageid+'.html'):
                        HTML=open(pageid+'.html').read()
                        res=scrapy.Selector(text=HTML)
                        ASINLists=res.xpath('//li')
                        for row in ASINLists:
                            a=row.xpath('.//a/@href').get()
                            if a and '/dp/' in a:
                                ASINList.append(str(a).split('/dp/')[1].split('?')[0])
                    ASINList_post=[]
                    for i in range(25):
                        if len(ASINList)>0:
                            ASINList_post.append(ASINList[0])
                            del ASINList[0]
                    json_data = {'requestContext': {'obfuscatedMarketplaceId': 'ATVPDKIKX0DER','language': 'en-US','currency': 'USD'},'endpoint': 'ajax-data','ASINList': ASINList_post}
                    url='https://www.amazon.com/juvec'
                    yield scrapy.Request(url,callback=self.parse_data,method='POST',body=json.dumps(json_data),meta={'Brand':Brand,'Menu':'SHOP ALL','ASINList':ASINList},headers=self.headers)
                else:
                    yield scrapy.Request(url,callback=self.parse_list,meta={'Brand':Brand,'pageid':pageid,'ASINList':ASINList},dont_filter=True)
    def parse_list(self, response):
        Brand=response.meta['Brand']
        pageid=response.meta['pageid']
        ASINList=response.meta['ASINList']
        MENUS=[]
        Data=response.xpath('//div[@data-testid="navigation"]//nav/ul/li')
        for row in Data:
            DIV=row.xpath('.//li')
            LINKS=row.xpath('./a')
            if len(LINKS)>0:
                if len(DIV)>0:
                    for rs in DIV:
                        LINKGR=rs.xpath('./a')
                        for rs in LINKGR:
                            LINK=rs.xpath('./@href').get()
                            MENU=rs.xpath('.//text()').get()
                            url=self.domain+LINK
                            if str(url).count('/')==5:
                                MENUS.append(MENU)
                else:
                    LINK=LINKS.xpath('./@href').get()
                    MENU=LINKS.xpath('.//text()').get()
                    if str(MENU).upper()!='HOME':
                        url=self.domain+LINK
                        if str(url).count('/')==5:
                            MENUS.append(MENU)
        for menu in MENUS:
            searchurl='https://www.amazon.com/stores/page/'+pageid+'/search?terms='+menu
            yield scrapy.Request(searchurl,callback=self.parse_ASIN,meta={'Brand':Brand,'Menu':menu,'ASINList':ASINList})

    def parse_ASIN(self, response):
        Brand=response.meta['Brand']
        Menu=response.meta['Menu']
        ASINList=response.meta['ASINList']
        if len(ASINList)==0:
            ASINList=str(response.text).split('"ASINList":[')[1].split(']')[0]
            ASINList=json.loads('['+ASINList+']')
        ASINList_post=[]
        for i in range(25):
            if len(ASINList)>0:
                ASINList_post.append(ASINList[0])
                del ASINList[0]
        json_data = {'requestContext': {'obfuscatedMarketplaceId': 'ATVPDKIKX0DER','language': 'en-US','currency': 'USD'},'endpoint': 'ajax-data','ASINList': ASINList_post}
        url='https://www.amazon.com/juvec'
        yield scrapy.Request(url,callback=self.parse_data,method='POST',body=json.dumps(json_data),meta={'Brand':Brand,'Menu':Menu,'ASINList':ASINList},headers=self.headers)
    def parse_data(self,response):
        Brand=response.meta['Brand']
        Menu=response.meta['Menu']
        ASINList=response.meta['ASINList']
        Data=json.loads(response.text)
        #print(Data['products'])
        for row in Data['products']:
            item={}
            #item['KEY_']=Brand+'_'+Menu+'_'+row['asin']
            item['KEY_']=row['asin']
            item['Brand']=Brand
            #item['Keyword']=Menu
            item['Product URL']='https://www.amazon.com' + row['links']['viewOnAmazon']['url']
            item['Product Name']=row['title']['displayString']
            PRICE={}
            if 'marketplaceOfferSummary' in row:
                for K,V in row['marketplaceOfferSummary'].items():
                    if K=='newOfferSummary':
                        for k,v in V.items():
                            if k in ('maxPrice','minPrice'):
                                PRICE[K+'_'+k]=v['amount']
                if 'buyingOptions' in row:
                    for i in range(len(row['buyingOptions'])):
                        rcs=row['buyingOptions'][i]
                        if isinstance(rcs['price'], dict):
                            for rs in rcs['price']:
                                if isinstance(rcs['price'][rs], dict):
                                    if 'moneyValueOrRange' in rcs['price'][rs]:
                                        v=rcs['price'][rs]
                                        if 'label' in v:
                                            try:
                                                PRICE[Get_String(v['label'])+'_'+rs]=v['moneyValueOrRange']['value']['amount']
                                            except:
                                                print('\n --------')
                                                print(v['moneyValueOrRange'])
                item['Price']=PRICE.get('newOfferSummary_minPrice','')
                item['Discounted price']=''
                if 'newOfferSummary_minPrice' in PRICE and 'newOfferSummary_maxPrice' in PRICE and PRICE['newOfferSummary_minPrice']<PRICE['newOfferSummary_maxPrice']:
                    WAS=PRICE.get('Was_basisPrice','')
                    if WAS!='':
                        item['Price']=WAS
                        item['Discounted price']=PRICE.get('newOfferSummary_minPrice')
                item['Description']='; '.join(row['featureBullets']['featureBullets'])
                yield(item)

        if len(ASINList)>0:
            ASINList_post=[]
            for i in range(25):
                if len(ASINList)>0:
                    ASINList_post.append(ASINList[0])
                    del ASINList[0]
            json_data = {'requestContext': {'obfuscatedMarketplaceId': 'ATVPDKIKX0DER','language': 'en-US','currency': 'USD'},'endpoint': 'ajax-data','ASINList': ASINList_post}
            url='https://www.amazon.com/juvec'
            yield scrapy.Request(url,callback=self.parse_data,method='POST',body=json.dumps(json_data),meta={'Brand':Brand,'Menu':Menu,'ASINList':ASINList},headers=self.headers)


        
