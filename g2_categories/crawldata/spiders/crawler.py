import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'g2_categories'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    cookies = {
    'cf_clearance': 'u.UdY4rExLOwifP6f6kR5bM3TD6JYHIOENgmds94Ynw-1688749219-0-250',
    'osano_consentmanager_uuid': 'feaa72f3-69a5-4e38-993b-799b6d767674',
    'osano_consentmanager': 'y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==',
    '_sp_id.6c8b': 'dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.6.1688749271.1688741137.9675c748-e5e0-465f-8fa2-7c1344a206ac.dd509e80-60d4-4b92-a0a5-c848b6bd4caf.834f9a79-3fcf-4642-864d-b1e1cc8307c0.1688745005623.50',
    '_ga_MFZ5NDXZ5F': 'GS1.1.1688745006.5.1.1688749250.31.0.0',
    '_ga': 'GA1.2.1170638361.1686710004',
    'sp': 'f7c087c9-ba10-46ee-b441-2ae005dea18d',
    '_delighted_web': '{^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}^%^2C^%^22_delighted_lst^%^22:{^%^22t^%^22:^%^221688739237624^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}^%^2C^%^22_delighted_lrt^%^22:{^%^22t^%^22:^%^221688739680554^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}}}',
    'AWSALB': 'RaWi/xV+eIPSpBxfdscngikz+8g5ZGLr/QLOhjNnAu8eiZMUy+ihN2lE/gEwyrBf8ONexJos8lSLncAqhkHKHt8KJf8YmH32Je2kYJ1bNF41zpnlQCjjwUNaOwiY',
    'AWSALBCORS': 'RaWi/xV+eIPSpBxfdscngikz+8g5ZGLr/QLOhjNnAu8eiZMUy+ihN2lE/gEwyrBf8ONexJos8lSLncAqhkHKHt8KJf8YmH32Je2kYJ1bNF41zpnlQCjjwUNaOwiY',
    'events_distinct_id': '44b4369c-ef73-4858-a25d-3e23a3c471bc',
    '_g2_session_id': 'ae52e1266f8e8700e3a8a0516b706071',
    '_gid': 'GA1.2.1011692809.1688738845',
    '_sp_ses.6c8b': '*',
    'amplitude_session': '1688745003714',
    '__cf_bm': 'w4re94f_efH0MDaExHx1f0ypR.R42b_cK0aE.RtYDzk-1688748694-0-AZy4nHynL0k0WPNjRWm1ZMdjfq+/brZnhpzHuqGpqv9TmTeL4wcd3EoDSnHvVpIHv3oILSKUVKk+IV2Pepfrx8aP2qFJl8LzTNoav3N40Quf',
    'cf_chl_2': '1bcd23724b01619',
    '_gat': '1',
    '_gat_t1': '1',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # 'Cookie': 'cf_clearance=u.UdY4rExLOwifP6f6kR5bM3TD6JYHIOENgmds94Ynw-1688749219-0-250; osano_consentmanager_uuid=feaa72f3-69a5-4e38-993b-799b6d767674; osano_consentmanager=y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==; _sp_id.6c8b=dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.6.1688749271.1688741137.9675c748-e5e0-465f-8fa2-7c1344a206ac.dd509e80-60d4-4b92-a0a5-c848b6bd4caf.834f9a79-3fcf-4642-864d-b1e1cc8307c0.1688745005623.50; _ga_MFZ5NDXZ5F=GS1.1.1688745006.5.1.1688749250.31.0.0; _ga=GA1.2.1170638361.1686710004; sp=f7c087c9-ba10-46ee-b441-2ae005dea18d; _delighted_web={^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}^%^2C^%^22_delighted_lst^%^22:{^%^22t^%^22:^%^221688739237624^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}^%^2C^%^22_delighted_lrt^%^22:{^%^22t^%^22:^%^221688739680554^%^22^%^2C^%^22m^%^22:{^%^22token^%^22:^%^22G9aujXKMxlkk9VD5AqCrjIBb^%^22}}}}; AWSALB=RaWi/xV+eIPSpBxfdscngikz+8g5ZGLr/QLOhjNnAu8eiZMUy+ihN2lE/gEwyrBf8ONexJos8lSLncAqhkHKHt8KJf8YmH32Je2kYJ1bNF41zpnlQCjjwUNaOwiY; AWSALBCORS=RaWi/xV+eIPSpBxfdscngikz+8g5ZGLr/QLOhjNnAu8eiZMUy+ihN2lE/gEwyrBf8ONexJos8lSLncAqhkHKHt8KJf8YmH32Je2kYJ1bNF41zpnlQCjjwUNaOwiY; events_distinct_id=44b4369c-ef73-4858-a25d-3e23a3c471bc; _g2_session_id=ae52e1266f8e8700e3a8a0516b706071; _gid=GA1.2.1011692809.1688738845; _sp_ses.6c8b=*; amplitude_session=1688745003714; __cf_bm=w4re94f_efH0MDaExHx1f0ypR.R42b_cK0aE.RtYDzk-1688748694-0-AZy4nHynL0k0WPNjRWm1ZMdjfq+/brZnhpzHuqGpqv9TmTeL4wcd3EoDSnHvVpIHv3oILSKUVKk+IV2Pepfrx8aP2qFJl8LzTNoav3N40Quf; cf_chl_2=1bcd23724b01619; _gat=1; _gat_t1=1',
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
            SQL="SELECT Category_URL FROM "+self.name
            Data=get_data_sql(self.conn,SQL)
            for row in Data:
                self.CRAWLED.append(key_MD5(row['Category_URL']))
        except:
            pass
        url='https://www.g2.com/categories?view_hierarchy=true'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True,headers=self.headers,cookies=self.cookies)
    def parse(self, response):
        Data=response.xpath('//div[@class="paper"]//a/@href').getall()
        for row in Data:
            url='https://www.g2.com'+row
            KEY=key_MD5(url)
            if not KEY in self.CRAWLED:
                yield scrapy.Request(url,callback=self.parse_date,dont_filter=True,headers=self.headers,cookies=self.cookies)
            else:
                print('Existed:',url)
    def parse_date(self,response):
        item={}
        item['KEY_']=key_MD5(response.url)
        item['Category URL']=response.url
        item['Category Name']=response.xpath('//ol[@id="breadcrumbs"]//span[@itemprop="name"]/text()').getall()[-1]
        TITLE=response.xpath('//div[@id="product-list"]//h3/text()').get()
        DES=cleanhtml(response.xpath('//div[@class="admin-text"]').get())
        if TITLE:
            item['Category Description']=TITLE+"\n"+DES
        else:
            item['Category Description']=DES
        item['Number of Listings']=response.xpath('//div[@aria-live="polite"]//strong/text()').get()
        yield(item)