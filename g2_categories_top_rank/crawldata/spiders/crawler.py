import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'g2_categories_top_rank'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    cookies = {
    'cf_clearance': 'DLE.S4Y2UaxOSEjrEsYLslYf_RZKDyNKD7O_bdqYh1Y-1689873197-0-250.2.1689873197',
    'osano_consentmanager_uuid': 'feaa72f3-69a5-4e38-993b-799b6d767674',
    'osano_consentmanager': 'y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==',
    '_sp_id.6c8b': 'dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.7.1689873225.1688750676.9782565e-ac48-4d19-b270-855baf4f32ca.9675c748-e5e0-465f-8fa2-7c1344a206ac.128c8f17-ebdd-418d-af1b-4c97f5a88171.1689868030705.60',
    '_ga_MFZ5NDXZ5F': 'GS1.1.1689868029.6.1.1689873197.13.0.0',
    '_ga': 'GA1.2.1170638361.1686710004',
    'sp': 'f7c087c9-ba10-46ee-b441-2ae005dea18d',
    '_delighted_web': '{^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}^%^2C^%^22_delighted_lst^%^22:{^%^22t^%^22:^%^221688739237624^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}^%^2C^%^22_delighted_lrt^%^22:{^%^22t^%^22:^%^221688739680554^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}}}',
    'cf_chl_2': 'cb182dccc2cf26c',
    'AWSALB': '5YHU3YtNpdhY+dfRgp/cWUjrhopDMM7e0gAcAgvj17YidRG5XwrJa0LPQTlDu3ry44Ox7Yms3YcGFAaYf/SErVCeWFENPD4qU3on5lo8/uhnA3RmZLjevICxSacT',
    'AWSALBCORS': '5YHU3YtNpdhY+dfRgp/cWUjrhopDMM7e0gAcAgvj17YidRG5XwrJa0LPQTlDu3ry44Ox7Yms3YcGFAaYf/SErVCeWFENPD4qU3on5lo8/uhnA3RmZLjevICxSacT',
    'events_distinct_id': '969e0e53-e645-4179-8530-dc5fa1ec4a6e',
    'amplitude_session': '1689868026362',
    '_g2_session_id': 'd9143e527615dc114f8ad463cf238ef4',
    '_sp_ses.6c8b': '*',
    '_gid': 'GA1.2.1346799790.1689868030',
    '_gcl_au': '1.1.368039223.1689868033',
    'ln_or': 'eyI2Mzg1NDgsNzQxOCI6ImQifQ^%^3D^%^3D',
    '_fbp': 'fb.1.1689868033683.1383742449',
    '__adroll_fpc': '1eceb7677e02dc6988174d6a81557010-1689868033755',
    '__ar_v4': 'C6MKFN32KVBHZAS4DKYVVW^%^3A20230719^%^3A17^%^7CEEPCTRZ5RNC6ZCBB2PJM4J^%^3A20230719^%^3A17^%^7CNBMTYK27EJFT3GYAV7FM56^%^3A20230719^%^3A17',
    '__cf_bm': 'qYl7H5O5KjQ.Jjkjjt55vxGKIBn4l_whhZdZlVu0Oxw-1689872548-0-ATDu/mG5aHK42DstmkxEwnjLfFnhMCE5wK8jOXCXUlbZqqr6IMdKinaCigS/Q4Sl71ckPcYFtPqZ3LZrVUk4opM=',
    '_gat': '1',
    '_gat_t1': '1',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # 'Cookie': 'cf_clearance=DLE.S4Y2UaxOSEjrEsYLslYf_RZKDyNKD7O_bdqYh1Y-1689873197-0-250.2.1689873197; osano_consentmanager_uuid=feaa72f3-69a5-4e38-993b-799b6d767674; osano_consentmanager=y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==; _sp_id.6c8b=dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.7.1689873225.1688750676.9782565e-ac48-4d19-b270-855baf4f32ca.9675c748-e5e0-465f-8fa2-7c1344a206ac.128c8f17-ebdd-418d-af1b-4c97f5a88171.1689868030705.60; _ga_MFZ5NDXZ5F=GS1.1.1689868029.6.1.1689873197.13.0.0; _ga=GA1.2.1170638361.1686710004; sp=f7c087c9-ba10-46ee-b441-2ae005dea18d; _delighted_web={^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}^%^2C^%^22_delighted_lst^%^22:{^%^22t^%^22:^%^221688739237624^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}^%^2C^%^22_delighted_lrt^%^22:{^%^22t^%^22:^%^221688739680554^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}}}; cf_chl_2=cb182dccc2cf26c; AWSALB=5YHU3YtNpdhY+dfRgp/cWUjrhopDMM7e0gAcAgvj17YidRG5XwrJa0LPQTlDu3ry44Ox7Yms3YcGFAaYf/SErVCeWFENPD4qU3on5lo8/uhnA3RmZLjevICxSacT; AWSALBCORS=5YHU3YtNpdhY+dfRgp/cWUjrhopDMM7e0gAcAgvj17YidRG5XwrJa0LPQTlDu3ry44Ox7Yms3YcGFAaYf/SErVCeWFENPD4qU3on5lo8/uhnA3RmZLjevICxSacT; events_distinct_id=969e0e53-e645-4179-8530-dc5fa1ec4a6e; amplitude_session=1689868026362; _g2_session_id=d9143e527615dc114f8ad463cf238ef4; _sp_ses.6c8b=*; _gid=GA1.2.1346799790.1689868030; _gcl_au=1.1.368039223.1689868033; ln_or=eyI2Mzg1NDgsNzQxOCI6ImQifQ^%^3D^%^3D; _fbp=fb.1.1689868033683.1383742449; __adroll_fpc=1eceb7677e02dc6988174d6a81557010-1689868033755; __ar_v4=C6MKFN32KVBHZAS4DKYVVW^%^3A20230719^%^3A17^%^7CEEPCTRZ5RNC6ZCBB2PJM4J^%^3A20230719^%^3A17^%^7CNBMTYK27EJFT3GYAV7FM56^%^3A20230719^%^3A17; __cf_bm=qYl7H5O5KjQ.Jjkjjt55vxGKIBn4l_whhZdZlVu0Oxw-1689872548-0-ATDu/mG5aHK42DstmkxEwnjLfFnhMCE5wK8jOXCXUlbZqqr6IMdKinaCigS/Q4Sl71ckPcYFtPqZ3LZrVUk4opM=; _gat=1; _gat_t1=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


    conn=None
    CRAWLED=[]
    def start_requests(self):
        try:
            SQL="SELECT DISTINCT Category_URL FROM "+self.name
            Data=get_data_sql(self.conn,SQL)
            for row in Data:
                self.CRAWLED.append(row['Category_URL'])
        except:
            pass
        URLS=re.split('\r\n|\n',open('urls.txt','r',encoding='utf-8').read())
        for URL in URLS:
            if not URL in self.CRAWLED:
                url=URL+'?utf8=✓&order=popular'
                yield scrapy.Request(url,callback=self.parse,dont_filter=True,headers=self.headers,cookies=self.cookies)
            else:
                print('CRAWLED:',URL)
    def parse(self, response):
        Data=response.xpath('//div[@data-baby-grid-trigger]')
        i=0
        for row in Data:
            i+=1
            item={}
            item['Category URL']=str(response.url).split('?')[0]
            item['Ranking']=i
            item['Product Name']=row.xpath('.//div[@itemprop="name"]/text()').get()
            item['Product URL']=row.xpath('.//a[@data-event-options]/@href').get()
            item['Reviews']=Get_Number(str(row.xpath('.//span[@class="px-4th"]/text()').get()))
            item['Rating']=Get_Number(str(row.xpath('.//span[@class="fw-semibold"]/text()').get()))
            item['KEY_']=key_MD5(item['Category URL']+str(i))
            yield(item)