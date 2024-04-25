import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'anbima_precos'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/jsondata/'
    else:
        URL='file:///' + os.getcwd()+'/jsondata/'
    def start_requests(self):
        files=os.scandir('./jsondata')
        for f in files:
            if str(f.name).endswith('.json'):
                url=self.URL+f.name
                yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        CODE=str(os.path.basename(response.url)).split('.json')[0]
        Data=json.loads(response.text)
        URL='https://data.anbima.com.br/debentures/'+CODE+'/precos'
        if len(Data)>0:
            i=0
            for row in Data:
                item={}
                item['URL']=URL
                item['Name']=CODE
                item['Date']=row['data_referencia']
                try:
                    item['VNA']=round(float(row['vna']),6)
                except:
                    item['VNA']=''
                try:
                    item['PU PAR']=round(float(row['pu_par']),6)
                except:
                    item['PU PAR']=''
                try:
                    item['PU Event']=round(float(row['juros']),6)
                except:
                    item['PU Event']=''
                if i<10:
                    item['Page']=1
                else:
                    item['Page']=int(i/10)
                i+=1
                yield(item)
        else:
            item={}
            item['URL']=URL
            item['Name']='Not Found'
            item['Date']='Not Found'
            item['VNA']='Not Found'
            item['PU PAR']='Not Found'
            item['PU Event']='Not Found'
            item['Page']='Not Found'
            yield(item)
