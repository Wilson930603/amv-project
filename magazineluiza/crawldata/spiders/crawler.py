import scrapy,json,re
from crawldata.functions import *
from datetime import datetime
class CrawlerSpider(scrapy.Spider):
    name = 'magazineluiza'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    cookies = {
    'MLPARCEIRO': '71815',
    '_gcl_au': '1.1.2109894479.1687962750',
    '_scid': '8cd338cd-a25d-49b1-b057-8166061f3876',
    '_pin_unauth': 'dWlkPU5qVmpOVFE1WWprdE9XUTRZUzAwTXpGbExXSmhPVFl0TkdWbE56Vm1Nemt4TlRFeQ',
    '_sctr': '1^%^7C1687885200000',
    '__bid': '14ffb0e3-b017-4418-822c-c227b2963c26',
    '_ga_LCJ5VBTH8V': 'GS1.1.1688016951.2.1.1688017522.14.0.0',
    '_ga': 'GA1.3.763294014.1687962752',
    '_ga_C98RVP2QRJ': 'GS1.1.1688016951.2.1.1688017522.14.0.0',
    '__uzma': 'eb441f3b-d8c7-4b73-ba54-070fdc887767',
    '__uzmb': '1687962752',
    '__uzme': '1231',
    '__uzmc': '464232512744',
    '__uzmd': '1688017474',
    'stwu': 'temp_9dc2fd90-15c0-11ee-af00-c724e5c23491',
    'stwt': '1',
    '__privaci_cookie_consent_uuid': '029dbeee-3c73-4355-8771-96ffab505243:3',
    '__privaci_cookie_consent_generated': '029dbeee-3c73-4355-8771-96ffab505243:3',
    '__privaci_cookie_consents': '{consents:{1:1,2:1,3:1,4:1,6:1},location:HN^#VN,lang:en,gpcInBrowserOnConsent:false,gpcStatusInPortalOnConsent:false,status:record-consent-success,implicit_consent:true}',
    '_gid': 'GA1.3.853089642.1687962755',
    '_clck': '1btmhcn^|2^|fcv^|0^|1274',
    '_hjSessionUser_562226': 'eyJpZCI6IjQ5ZGIzOGRmLWUzOTctNWM4Yi1hMGNjLTk4MzRmN2RlY2FjYyIsImNyZWF0ZWQiOjE2ODc5NjI3NTYwMzYsImV4aXN0aW5nIjp0cnVlfQ==',
    '_fbp': 'fb.2.1687962756048.329474056',
    '_tt_enable_cookie': '1',
    '_ttp': 'oQiOzKKvHWoC7TERv7YLejRJUM5',
    '_clsk': 'hvfe37^|1688017481536^|3^|0^|x.clarity.ms/collect',
    'noe_freight': 'AUTO',
    'noe_hub_shipping_enabled': '1',
    'toggle_wishlist': 'false',
    'FCCDCF': '1',
    'ml2_redirect_8020': '0',
    'FCNEC': '1',
    'mixer_shipping': 'AUTO',
    'mixer_hub_shipping': 'true',
    '_hjIncludedInSessionSample_562226': '1',
    '_hjSession_562226': 'eyJpZCI6IjdhNTdkYmMwLWIyZGQtNGFiYS04NjI0LTFlMTE5ZmRkYjkxMCIsImNyZWF0ZWQiOjE2ODgwMTY5NTM0NzUsImluU2FtcGxlIjp0cnVlfQ==',
    '_hjAbsoluteSessionInProgress': '0',
    '_uetsid': '9dfa0f9015c011ee9a62a1f5d7eb49e1',
    '_uetvid': '9dfa29f015c011eebddaeb0fe40218b3',
    '_scid_r': '8cd338cd-a25d-49b1-b057-8166061f3876',
    '_gat_UA-42817937-2': '1',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'x-nextjs-data': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
    def start_requests(self):
        KEYS=re.split('\r\n|\n',open('keys.txt').read())
        for key in KEYS:
            key=str(key).replace(' ','+')
            url='https://www.magazineluiza.com.br/_next/data/RK7HJl3MHMU1683H5sQpi/busca/'+key+'.json?path1='+key+'&page=1'
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'key':key},headers=self.headers,cookies=self.cookies)
    def parse(self, response):
        key=response.meta['key']
        DATA=json.loads(response.text)
        Data=DATA['pageProps']['data']['search']
        for row in Data['products']:
            item={}
            item['url']='https://www.magazineluiza.com.br/busca/'+key
            item['name']=row['title']
            item['original_price']=row['price']['price']
            item['price']=row['price']['bestPrice']
            yield(item)
        if Data['pagination']['page']<Data['pagination']['pages']:
            url='https://www.magazineluiza.com.br/_next/data/RK7HJl3MHMU1683H5sQpi/busca/'+key+'.json?path1='+key+'&page='+str(Data['pagination']['page']+1)
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'key':key},headers=self.headers,cookies=self.cookies)