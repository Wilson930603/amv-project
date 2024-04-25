import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'humankind'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    IDS=[]
    def start_requests(self):
        URLS=re.split('\r\n|\n',open('urls.txt','r',encoding='utf-8').read())
        for urls in URLS:
            ID=str(urls).split('id=')[1]
            KEY=key_MD5((str(ID).split("&")[0]).split("?")[0])
            if not KEY in self.IDS:
                self.IDS.append(KEY)
                IDS=str(ID).split("|")
                if len(IDS)>=2:
                    IDS[1]=(str(IDS[1]).split("&")[0]).split("?")[0]
                    url='https://vhw8mjja9e.execute-api.us-west-1.amazonaws.com/customers/'+IDS[0]+'/recommendations/'+IDS[1]
                    yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'URL':urls})
                else:
                    open('err_urls.txt','a',encoding='utf-8').write(urls+'\n')
            else:
                open('dup_urls.txt','a',encoding='utf-8').write(urls+'\n')
    def parse(self, response):
        URL=response.meta['URL']
        try:
            Data=json.loads(response.text)
        except:
            Data={}
            open('err_urls.txt','a',encoding='utf-8').write(URL+'\n')
        if 'products' in Data:
            item={}
            item['_id']=key_MD5(URL)
            item['link']=URL
            i=0
            for row in Data['products']:
                i+=1
                item['Product '+str(i)+' Name']=row['name']
                item['Product '+str(i)+' Price']=row['currentPrice']
                item['Product '+str(i)+' Description']=cleanhtml(row['description'])
            yield(item)
                

                
        
