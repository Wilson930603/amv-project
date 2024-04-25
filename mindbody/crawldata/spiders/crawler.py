import scrapy,re,json
from crawldata.functions import *
from datetime import datetime,timedelta

class CrawlerSpider(scrapy.Spider):
    name = 'mindbodyonline'
    IDS=[]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0','Accept': 'application/vnd.api+json','Accept-Language': 'en-GB,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','content-type': 'application/vnd.api+json','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'cross-site','TE': 'trailers',}
    def start_requests(self):
        f=open('IDS.txt','r')
        LIST=re.split('\r\n|\n',f.read())
        f.close()
        for LS in LIST:
            LS=str(LS).split('~')
            Page=1
            data={"sort":"-_score,distance","page":{"size":100,"number":Page},"filter":{"categories":[],"radius":50000,"term":"","cmMembershipBookable":"any","latitude":LS[1],"longitude":LS[2],"categoryTypes":["Fitness"]}}
            yield scrapy.Request('https://prod-mkt-gateway.mindbody.io/v1/search/locations',callback=self.parse,headers=self.headers,body=json.dumps(data),method="POST",meta={'Page':Page,'LS':LS},dont_filter=True)
    def parse(self, response):
        DATA=json.loads(response.text)
        Data=DATA['data']
        print(len(Data))
        for rows in Data:
            row=rows['attributes']
            if not rows['id'] in self.IDS:
                self.IDS.append(rows['id'])
                item={}
                item['KEY_']=rows['id']
                item['URL']='https://www.mindbodyonline.com/explore/locations/'+row['slug']
                item['Category']=''
                for rs in row['categories']:
                    if item['Category']=='':
                        item['Category']=rs
                    else:
                        item['Category']+=' | '+rs
                item['Name']=row['name']
                item['Address']=row['address']
                if not row['address2'] is None:
                    item['Address']+=' '+row['address2']
                if not row['city'] is None:
                    item['Address']+=', '+row['city']
                if not row['state'] is None:
                    item['Address']+=', '+row['state']
                if not row['postalCode'] is None:
                    item['Address']+=' '+row['postalCode']
                item['Phone']=row['phone']
                item['Star']=row['averageRating']
                item['Reviews']=row['totalRatings']
                item['Price']=''
                TODAY=datetime.now().strftime('%Y-%m-%d')
                NEXTDAY=(datetime.now()+timedelta(30)).strftime('%Y-%m-%d')
                url='https://prod-mkt-gateway.mindbody.io/v1/availability/location?filter.location_slug='+row['slug']+'&filter.timezone=America%2FLos_Angeles&filter.start_time_from='+TODAY+'T00%3A00%3A00.000Z&filter.start_time_to='+NEXTDAY+'T23%3A59%3A59.999Z'
                yield scrapy.Request(url,callback=self.parse_time,headers=self.headers,meta={'item':item,'slug':row['slug']},dont_filter=True)
            else:
                print('Existed:',rows['id'])
        if DATA['meta']['start']<DATA['meta']['found']:
            Page=response.meta['Page']+1
            LS=response.meta['LS']
            print('CRAWL PAGE:',Page)
            data={"sort":"-_score,distance","page":{"size":100,"number":Page},"filter":{"categories":[],"radius":50000,"term":"","cmMembershipBookable":"any","latitude":LS[1],"longitude":LS[2],"categoryTypes":["Fitness"]}}
            yield scrapy.Request('https://prod-mkt-gateway.mindbody.io/v1/search/locations',callback=self.parse,headers=self.headers,body=json.dumps(data),method="POST",meta={'Page':Page,'LS':LS},dont_filter=True)
    def parse_time(self,response):
        item=response.meta['item']
        slug=response.meta['slug']
        DATA=json.loads(response.text)
        Data=DATA['data']
        if len(Data)>1:
            FROM=Data[0]['attributes']['date']
            data={"sort":"start_time","page":{"size":100,"number":1},"filter":{"radius":0,"startTimeRanges":[{"from":FROM+"T00:00:00.000Z","to":FROM+"T23:59:59.999Z"}],"locationSlugs":[slug],"include_dynamic_pricing":"true","inventory_source":["MB"]}}
            yield scrapy.Request('https://prod-mkt-gateway.mindbody.io/v1/search/class_times',callback=self.parse_price,headers=self.headers,body=json.dumps(data),method="POST",meta={'item':item},dont_filter=True)
        else:
            yield(item)
    def parse_price(self,response):
        item=response.meta['item']
        Data=json.loads(response.text)
        PRICE=Data['data']
        if len(PRICE)>0:
            CLASS_ID={}
            CLASS_DT=Data['included']
            for rs in CLASS_DT:
                if rs['type']=='course':
                    CLASS_ID[rs['id']]=rs['attributes']['name']
            for row in PRICE:
                try:
                    ID=row['relationships']['course']['data']['id']
                    if ID in CLASS_ID:
                        if item['Price']=='':
                            if not row['attributes']['pricingToken'] is None:
                                item['Price']=CLASS_ID[ID]+': $'+str(round(float(row['attributes']['pricingToken']['amount']),2))
                            else:
                                CHK=False
                                for rs in row['attributes']['purchaseOptions']:
                                    if rs['isSingleSession']==True and rs['isIntroOffer']==False and CHK==False:
                                        item['Price']=CLASS_ID[ID]+': $'+str(round(float(rs['pricing']['retail']),2))
                                        CHK=True
                        else:
                            if not row['attributes']['pricingToken'] is None:
                                item['Price']+=', '+CLASS_ID[ID]+': $'+str(round(float(row['attributes']['pricingToken']['amount']),2))
                            else:
                                CHK=False
                                for rs in row['attributes']['purchaseOptions']:
                                    if rs['isSingleSession']==True and rs['isIntroOffer']==False and CHK==False:
                                        item['Price']+=', '+CLASS_ID[ID]+': $'+str(round(float(rs['pricing']['retail']),2))
                                        CHK=True
                except:
                    pass
        yield(item)
