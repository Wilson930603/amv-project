import scrapy,json,re,os,platform,random,requests
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'booking_mangomint'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0','Accept': 'application/json','Accept-Language': 'en-GB,en;q=0.5','Content-Type': 'application/json','X-Mt-Booking-CompanyId': '','Origin': 'https://booking.mangomint.com','Connection': 'keep-alive','Referer': '','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin'}
    json_data = {'staffId': None,'serviceId': None}
    url='https://booking.mangomint.com/api/v1/booking/app/startup'
    proxies=re.split('\r\n|\n',open('../proxy_10000.txt','r').read())
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    GOOD=[]
    DO=int(open('RUN.txt','r').read())+1
    START=DO*100000
    STOP=(DO+1)*100000
    print(START,'->',STOP)
    open('RUN.txt','w').write(str(DO))
    def start_requests(self):
        if self.STOP<=1000000:
            for ID in range(self.START,self.START+10,1):
                yield scrapy.Request(self.URL,callback=self.parse,meta={'ID':ID},dont_filter=True)
    def parse(self, response):
        ID=response.meta['ID']
        RUN=True
        while RUN:
            print('CRAWLING:',ID)
            if len(self.GOOD)>5:
                PR=self.proxies[random.randrange(0,len(self.GOOD))]
            else:
                PR=self.proxies[random.randrange(0,len(self.proxies))]
            proxy = { 'https' : PR}
            try:
                headers={}
                headers.update(self.headers)
                headers['X-Mt-Booking-CompanyId']=str(ID)
                headers['Referer']='https://booking.mangomint.com/'+str(ID)
                response = requests.post('https://booking.mangomint.com/api/v1/booking/app/startup', headers=headers, json=self.json_data, proxies=proxy,timeout=3)
                Data=json.loads(response.text)
                if not PR in self.GOOD:
                    self.GOOD.append(PR)
                if 'companyId' in Data:
                    item={}
                    item['KEY_']=Data['companyId']
                    item['Company Link']='https://www.mangomint.com/?utm_source=booking-widget&utm_content='+Data['companySchemaName']
                    try:
                        item['Logo Link']=Data['uiSettings']['companyLogoAttachment']['data']['url']
                    except:
                        item['Logo Link']=''
                    yield(item)
                open('CRAWLED.txt','a').write('\n'+str(ID))
                RUN=False
            except:
                if PR in self.GOOD:
                    G=[]
                    for pr in self.GOOD:
                        if pr!=PR:
                            G.append(pr)
                    self.GOOD=G
        if ID<self.STOP:
            ID+=10
            yield scrapy.Request(self.URL,callback=self.parse,meta={'ID':ID},dont_filter=True)