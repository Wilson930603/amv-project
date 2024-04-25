import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'g2_product_scraping'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    cookies = {
    'cf_clearance': 'cHzBCxLGQNNGMgt1woO6_8hei6rB7FblyZtytJX7Ibs-1690225147-0-160.2.1690222829',
    'osano_consentmanager_uuid': 'feaa72f3-69a5-4e38-993b-799b6d767674',
    'osano_consentmanager': 'y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==',
    '_sp_id.6c8b': 'dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.10.1690225153.1690213464.27b799d5-ef18-433d-aaf2-9d3f35b8fa43.33f52ddd-b634-4675-a5d8-0e62d8f9376d.124c84fe-1682-4cff-88b6-1c45e9e82287.1690215459488.91',
    '_ga_MFZ5NDXZ5F': 'GS1.1.1690215459.9.1.1690225153.56.0.0',
    '_ga': 'GA1.2.1170638361.1686710004',
    'sp': 'f7c087c9-ba10-46ee-b441-2ae005dea18d',
    '_delighted_web': '{^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}^%^2C^%^22_delighted_lst^%^22:{^%^22t^%^22:^%^221688739237624^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}^%^2C^%^22_delighted_lrt^%^22:{^%^22t^%^22:^%^221688739680554^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}}}',
    'AWSALB': 'DhoZCjM8y6QrVo2IsGf9FwtXs8p844y13Sa7DkV1QXg92GVpzYX3CZ4HI7Ig30w3BH2su2B6aukCb9yBUaPJSNuFPneDpXmz/66mX/4KUaah6WyLZuX7rNVIWmLH',
    'AWSALBCORS': 'DhoZCjM8y6QrVo2IsGf9FwtXs8p844y13Sa7DkV1QXg92GVpzYX3CZ4HI7Ig30w3BH2su2B6aukCb9yBUaPJSNuFPneDpXmz/66mX/4KUaah6WyLZuX7rNVIWmLH',
    '_gcl_au': '1.1.368039223.1689868033',
    '_fbp': 'fb.1.1689868033683.1383742449',
    '__adroll_fpc': '1eceb7677e02dc6988174d6a81557010-1689868033755',
    '__ar_v4': 'NBMTYK27EJFT3GYAV7FM56^%^3A20230719^%^3A52^%^7CEEPCTRZ5RNC6ZCBB2PJM4J^%^3A20230719^%^3A52^%^7CC6MKFN32KVBHZAS4DKYVVW^%^3A20230719^%^3A52',
    'cf_chl_2': 'f22995672e16f45',
    'events_distinct_id': 'f7112255-1ef4-4493-8510-2bc2b0ea0246',
    '_g2_session_id': '05ea3d22917d5e315dde76573e240ff0',
    '_gid': 'GA1.2.185783933.1690209445',
    'ln_or': 'eyI2Mzg1NDgsNzQxOCI6ImQifQ^%^3D^%^3D',
    '_sp_ses.6c8b': '*',
    '__cf_bm': 'PvzMC1epGzXxBhQEpQQVqyOZON4ejXsyymkmEN8hMOI-1690225149-0-AfUHQjhFULGddtg5lNuVGz4sGfaSR93ztRK81xl8eajlIn9FbRYZiDt5dVELaV3/m0/7YCVt2+fcnXrjxb7a1wk=',
    'amplitude_session': '1690215461992',
    'ue-event-snowplow-8befcf01-f595-4905-b210-6d0f4752d8bd': 'W1siYWR2ZXJ0aXNlbWVudC12aWV3ZWQiLHsicHJvZHVjdF9pZCI6OTgzMTQs^%^0AInByb2R1Y3RfdXVpZCI6ImRmNGE5ZTdiLTczMjctNDI2YS1hODQ5LTQ2YjM5^%^0AMmFiNTAwMiIsInByb2R1Y3QiOiJNSVBSTyIsInZlbmRvcl9pZCI6NzUyMzMs^%^0AInByb2R1Y3RfdHlwZSI6IlByb3ZpZGVyIiwiYWRfaWQiOjEwMjc0NjAsInR5^%^0AcGUiOiJBZHZlcnRpc2luZzo6VXBsb2FkZWRJbWFnZSIsImNhdGVnb3JpZXMi^%^0AOlsiT3JhY2xlIEltcGxlbWVudGVycyBhbmQgQ29uc3VsdGFudHMiXSwiY2F0^%^0AZWdvcnlfaWRzIjpbMTAwMzYzOF0sInRhZyI6ImFkLmNhdGVnb3J5X2NvbXBl^%^0AdGl0b3IucHJvZHVjdF9sZWZ0X3NpZGViYXIiLCJhZG1pbl92aWV3ZXIiOmZh^%^0AbHNlLCJ1c2VyX3R5cGUiOiJndWVzdCJ9LCI4YmVmY2YwMS1mNTk1LTQ5MDUt^%^0AYjIxMC02ZDBmNDc1MmQ4YmQiLCJTcG9uc29yZWQgQ29udGVudCBWaWV3ZWQi^%^0ALCIxLTAtMCIsWyJhbXBsaXR1ZGUiXV1d^%^0A',
    '_gat': '1',
    '_gat_t1': '1',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.g2.com/products/netzoom/reviews?__cf_chl_tk=lbJjdA2UaIa9Rt0gLKReF60Yxn_Pu0p8NTWkUrf2TAo-1690225147-0-gaNycGzNERA',
    'Connection': 'keep-alive',
    # 'Cookie': 'cf_clearance=cHzBCxLGQNNGMgt1woO6_8hei6rB7FblyZtytJX7Ibs-1690225147-0-160.2.1690222829; osano_consentmanager_uuid=feaa72f3-69a5-4e38-993b-799b6d767674; osano_consentmanager=y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==; _sp_id.6c8b=dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.10.1690225153.1690213464.27b799d5-ef18-433d-aaf2-9d3f35b8fa43.33f52ddd-b634-4675-a5d8-0e62d8f9376d.124c84fe-1682-4cff-88b6-1c45e9e82287.1690215459488.91; _ga_MFZ5NDXZ5F=GS1.1.1690215459.9.1.1690225153.56.0.0; _ga=GA1.2.1170638361.1686710004; sp=f7c087c9-ba10-46ee-b441-2ae005dea18d; _delighted_web={^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}^%^2C^%^22_delighted_lst^%^22:{^%^22t^%^22:^%^221688739237624^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}^%^2C^%^22_delighted_lrt^%^22:{^%^22t^%^22:^%^221688739680554^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}}}; AWSALB=DhoZCjM8y6QrVo2IsGf9FwtXs8p844y13Sa7DkV1QXg92GVpzYX3CZ4HI7Ig30w3BH2su2B6aukCb9yBUaPJSNuFPneDpXmz/66mX/4KUaah6WyLZuX7rNVIWmLH; AWSALBCORS=DhoZCjM8y6QrVo2IsGf9FwtXs8p844y13Sa7DkV1QXg92GVpzYX3CZ4HI7Ig30w3BH2su2B6aukCb9yBUaPJSNuFPneDpXmz/66mX/4KUaah6WyLZuX7rNVIWmLH; _gcl_au=1.1.368039223.1689868033; _fbp=fb.1.1689868033683.1383742449; __adroll_fpc=1eceb7677e02dc6988174d6a81557010-1689868033755; __ar_v4=NBMTYK27EJFT3GYAV7FM56^%^3A20230719^%^3A52^%^7CEEPCTRZ5RNC6ZCBB2PJM4J^%^3A20230719^%^3A52^%^7CC6MKFN32KVBHZAS4DKYVVW^%^3A20230719^%^3A52; cf_chl_2=f22995672e16f45; events_distinct_id=f7112255-1ef4-4493-8510-2bc2b0ea0246; _g2_session_id=05ea3d22917d5e315dde76573e240ff0; _gid=GA1.2.185783933.1690209445; ln_or=eyI2Mzg1NDgsNzQxOCI6ImQifQ^%^3D^%^3D; _sp_ses.6c8b=*; __cf_bm=PvzMC1epGzXxBhQEpQQVqyOZON4ejXsyymkmEN8hMOI-1690225149-0-AfUHQjhFULGddtg5lNuVGz4sGfaSR93ztRK81xl8eajlIn9FbRYZiDt5dVELaV3/m0/7YCVt2+fcnXrjxb7a1wk=; amplitude_session=1690215461992; ue-event-snowplow-8befcf01-f595-4905-b210-6d0f4752d8bd=W1siYWR2ZXJ0aXNlbWVudC12aWV3ZWQiLHsicHJvZHVjdF9pZCI6OTgzMTQs^%^0AInByb2R1Y3RfdXVpZCI6ImRmNGE5ZTdiLTczMjctNDI2YS1hODQ5LTQ2YjM5^%^0AMmFiNTAwMiIsInByb2R1Y3QiOiJNSVBSTyIsInZlbmRvcl9pZCI6NzUyMzMs^%^0AInByb2R1Y3RfdHlwZSI6IlByb3ZpZGVyIiwiYWRfaWQiOjEwMjc0NjAsInR5^%^0AcGUiOiJBZHZlcnRpc2luZzo6VXBsb2FkZWRJbWFnZSIsImNhdGVnb3JpZXMi^%^0AOlsiT3JhY2xlIEltcGxlbWVudGVycyBhbmQgQ29uc3VsdGFudHMiXSwiY2F0^%^0AZWdvcnlfaWRzIjpbMTAwMzYzOF0sInRhZyI6ImFkLmNhdGVnb3J5X2NvbXBl^%^0AdGl0b3IucHJvZHVjdF9sZWZ0X3NpZGViYXIiLCJhZG1pbl92aWV3ZXIiOmZh^%^0AbHNlLCJ1c2VyX3R5cGUiOiJndWVzdCJ9LCI4YmVmY2YwMS1mNTk1LTQ5MDUt^%^0AYjIxMC02ZDBmNDc1MmQ4YmQiLCJTcG9uc29yZWQgQ29udGVudCBWaWV3ZWQi^%^0ALCIxLTAtMCIsWyJhbXBsaXR1ZGUiXV1d^%^0A; _gat=1; _gat_t1=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'If-None-Match': 'W/1eea07b8115d221caae597e8fd2d4ea8',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

    conn=None
    CRAWLED=[]
    URLS=[]
    TT=0
    CRAWLED_TXT=[]
    def start_requests(self):
        try:
            #SQL="SELECT DISTINCT Product FROM "+self.name+" WHERE Overview<>'' and Seller<>''"
            SQL="SELECT DISTINCT Product FROM "+self.name
            Data=get_data_sql(self.conn,SQL)
            for row in Data:
                self.CRAWLED.append(str(row['Product']).split('/')[4])
        except:
            pass
        if os.path.exists('CRAWLED.txt'):
            self.CRAWLED_TXT=re.split('\r\n|\n',open('CRAWLED.txt').read())
            for rs in self.CRAWLED_TXT:
                if rs!='' and not rs in self.CRAWLED:
                    self.CRAWLED.append(rs)
        self.URLS=re.split('\r\n|\n',open('urls.txt','r',encoding='utf-8').read())
        CHK=True
        while CHK==True:
            URL=self.URLS[self.TT]
            KEY=str(URL).split('/')[4]
            if not KEY in self.CRAWLED:
                CHK=False
                print('\n -----------',self.TT,URL)
                self.CRAWLED.append(KEY)
                yield scrapy.Request(URL,callback=self.parse,dont_filter=True,headers=self.headers,cookies=self.cookies,meta={'key':KEY})
            else:
                self.TT+=1
                #print('CRAWLED:',URL)
    def parse(self, response):
        if response.status<400:
            key=response.meta['key']
            KEY=str(response.url).split('/')[4]
            self.CRAWLED_TXT.append(key)
            if key!=KEY:
                open('CRAWLED.txt','a').write('\n'+key)
            item={}
            item['KEY_']=KEY
            item['Product']=str(response.url).split('?')[0]
            item['Overview']=cleanhtml(response.xpath('//div[@class="paper paper--nestable"]').get())
            item['Description']=''
            K=['Seller','Ownership','HQ Location','Total Revenue']
            for k in K:
                item[k]=''
            item['Company Website']=''
            item['Twitter']=''
            item['Twitter Followers']=''
            item['LinkedIn']=''
            item['LinkedIn FTE']=''
            Data=response.xpath('//div[contains(@class,"revealer-hex-")]')
            for row in Data:
                DIV=row.xpath('./div/text()').get()
                if DIV:
                    if 'Product Description' in DIV:
                        item['Description']='\n'.join(row.xpath('./p/text()').getall())
                    if 'Seller Details' in DIV:
                        data=row.xpath('.//div[@class="mb-half"]')
                        for rs in data:
                            title=rs.xpath('.//div[@class="fw-semibold"]')
                            label=title.xpath('./text()').get()
                            txt=title.xpath('../text()').getall()
                            for k in K:
                                if k in label:
                                    item[k]=txt[0]
                            if 'Company Website' in label:
                                item['Company Website']=json.loads(rs.xpath('.//a[@data-event-options]/@data-event-options').get())['url']
                            if 'Twitter' in label:
                                item['Twitter']=txt[0]
                                if len(txt)>1:
                                    item['Twitter Followers']=txt[1].split()[0]
                            if 'LinkedIn' in label:
                                try:
                                    item['LinkedIn']=json.loads(rs.xpath('.//a[@data-event-options]/@data-event-options').get())['url']
                                except:
                                    pass
                                if len(txt)>0:
                                    item['LinkedIn FTE']=txt[0].split()[0]
            yield(item)
            CHK=True
            while CHK==True:
                if os.path.exists('CRAWLED.txt'):
                    CRAWLED=re.split('\r\n|\n',open('CRAWLED.txt').read())
                    for rs in CRAWLED:
                        if rs!='' and not rs in self.CRAWLED:
                            self.CRAWLED.append(rs)
                URL=self.URLS[self.TT]
                KEY=str(URL).split('/')[4]
                if not KEY in self.CRAWLED:
                    CHK=False
                    print('\n ===========',self.TT,URL)
                    self.CRAWLED.append(KEY)
                    yield scrapy.Request(URL,callback=self.parse,dont_filter=True,headers=self.headers,cookies=self.cookies,meta={'key':KEY})
                else:
                    self.TT+=1
                    #print('CRAWLED:',URL)