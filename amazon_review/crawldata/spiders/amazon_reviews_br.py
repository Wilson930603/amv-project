# -*- coding: utf-8 -*-
import scrapy,re,hashlib,html,os
from crawldata.functions import *
class RunSpider(scrapy.Spider):
    name = 'amazon_reviews_br'
    domain='https://www.amazon.com.br'
    cookies = {
    'session-id': '140-4913937-3570316',
    'session-id-time': '2082787201l',
    'csm-hit': 'tb:B3ES0BRVN25DBEM7YAXQ+s-DGY3T3RBYM0PE5QM1QET^|1687962565643&t:1687962565643&adb:adblk_no',
    'ubid-acbbr': '132-8796873-0312505',
    'session-token': 'EgXErkERUueg9CQHG1P59WRGwjLyi2jGVOAX1ez7lgpbuBFJ5rVIZIiFi/hHrBYG/omPNGG+6WV8Z9L3MrWOzuHCLxBK3hXDFzpPaYwc7bv/vVxZ7XqqmO85DFTEH/lhiDI3EVBmH/c/kkIR1FkEiCNyyWu4Eop+9dKF8lslIIUf7Q+mO7QAqJ3U9mqePi37XpvvZUYjlqziKcUbKqcZuVPsZYifXamaM6rd/5bbE/LdXPGjz0qUAg1ygCwViIU6',
    'lc-acbbr': 'pt_BR',
    'x-acbbr': 'HuxJiybC7Vxc7YAnlI9V7Vp1K2lBpzJsTtiG4h26nkbdlMMwy9T87WGSj?l^@1L4x',
    'at-acbbr': 'Atza^|IwEBIJEZ46QHS9S3MltDAmoRXy05s71Vu5HBdkif0WWNrl5zSw8AvClfpw1dXcNAF0jjU2DxecLEXBrL89GNvenuoVdXks3IFModdLIh92mAPXTp4725MflkVRoqxjfwy_b3KvvcW3JvFmZM6dI3HgNHBsbRoTPgC25riRMZV3yKEolP3auSbInpwIJTd0TSO5ifmVZlAv3vqojQ-GdjXKy_XtofQo3S-RsQ0RUeA-I9rdPiuA',
    'sess-at-acbbr': 'c3UwldrjMHh4yoYvXSV6j4Q8iNx4QVmKJ5MvWi5oolI=',
    'sst-acbbr': 'Sst1^|PQEVpFIeNEsWnOur4GIKlp17CbUHqe9EHKIGmoop3LtOnCg8rRPGHS44bRO1605NLozWQFJjPkgkKP1rHIOG5I3ksXXnrwUv0sh4a85xlN91SY5FtBHAQyAaCs8BlcHszimHve5kOTw-bmgBJS5owKvbl-Dp6km_CyeZbOWzC_HbCW5jyvJ9wzfEre-RR72xW0z4OMtBNow3MDLhZg8gNcRZhJP5R2LSTogG_1tWR4VMrUxKuPzxOFONrvZBRm5STO4EyOJuZN2MvO1RYRppmyUyzBgySqy1jjGmWrs7u2wNB1A',
    'i18n-prefs': 'BRL',
}
    headers = {
    'authority': 'www.amazon.com.br',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1.25',
    'ect': '4g',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.25',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1536',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'viewport-width': '1536',
}

    TMP={"Product":"","Retailer Name":"","Title":"","Review Star":"","Is Verified":"","Has Response":"","Review Title":"","Review Text":"","Review Date":"","Review URL":"","Category":"","Is Discontinued By Manufacturer":"","Product Dimensions":"Dimensões do produto","Item model number":"Número do modelo","UPC":"","Manufacturer":"Fabricante","ASIN":"","Brand":"Marca","Ingredients":"Ingredientes","Active Ingredient":"Ingredientes especiais","Skin Type":"","Style":"","Material type free":"","Review Location":"","Review ID":"","Reviewer":"","# of people":""}
    START=0
    LIMIT=1
    if os.path.exists('CRAWLED.txt'):
        START=int(open('CRAWLED.txt','r').read())
        print('START:',START)
    def __init__(self, START=None, **kwargs):
        if not START is None:
            self.START=int(START)
        super().__init__(**kwargs)
    def start_requests(self):
        LIST=re.split("\r\n|\n",open('urls.txt','r').read())
        Start=self.START
        End=Start+self.LIMIT
        if End<=len(LIST):
            open('CRAWLED.txt','w').write(str(End))
            for i in range(Start,End):
                if not str(LIST[i]).startswith('#'):
                    item={}
                    item['ID']=i+1
                    item['Product']=str(LIST[i]).split('/')[3]
                    item['Retailer Name']=str(LIST[i]).split('/')[2]
                    url=LIST[i]
                    yield scrapy.Request(url,callback=self.parse,meta={'item':item,'Level':0},dont_filter=True,cookies=self.cookies,headers=self.headers)
    def parse(self,response):
        item=response.meta['item']
        Level=response.meta['Level']
        if response.status==200 and '(MEOW)' in response.text:
            PRODUCT_NAME=response.xpath('//h1/span/text()').get()
            if not PRODUCT_NAME is None:
                item['Title']=str(PRODUCT_NAME).strip()
                item['Category']=html.unescape(self.kill_space(self.cleanhtml(response.xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]').get())))
                Data=response.xpath('//div[@id="productOverview_feature_div"]//tr')
                for row in Data:
                    item[self.cleanhtml(str(row.xpath('./td[1]').get())).strip()]=self.cleanhtml(str(row.xpath('./td[2]').get())).strip()
                Data=response.xpath('//div[@id="detailBullets_feature_div"]//li/span[@class="a-list-item"]')
                for row in Data:
                    TITLE=(self.cleanhtml(str(row.xpath('./span[1]').get())).strip()).replace(':','')
                    item[str(TITLE).strip()]=self.cleanhtml(str(row.xpath('./span[2]').get())).strip()
                Data=response.xpath('//table[contains(@id,"productDetails_techSpec_")]//tr')
                for row in Data:
                    TITLE=self.cleanhtml(str(row.xpath('./th').get())).strip()
                    item[str(TITLE).strip()]=self.cleanhtml(str(row.xpath('./td').get())).strip()
                if not 'ASIN' in item:
                    item['ASIN']=str(response.url).split('/dp/')[1].split('/')[0]
                url_review=self.domain+'/'+item['Product']+'/product-reviews/'+item['ASIN']+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageSize=20'
                yield scrapy.Request(url_review,callback=self.parse_review,meta={'item':item,'Level':0},cookies=self.cookies,headers=self.headers)
            else:
                print('\n ============= NOT FOUND')
                #yield scrapy.Request(response.url,callback=self.parse,meta={'item':item,'Level':Level},dont_filter=True,cookies=self.cookies)
        elif Level<100:
            Level+=1
            print('\n ************ RE-CRAWL')
            yield scrapy.Request(response.url,callback=self.parse,meta={'item':item,'Level':Level},dont_filter=True,cookies=self.cookies,headers=self.headers)
        else:
            f=open('Errors.txt','a',encoding='utf-8')
            f.write('\n'+response.url)
            f.close()
    def parse_review(self,response):
        ITEM=response.meta['item']
        Level=response.meta['Level']
        if response.status==200 and '(MEOW)' in response.text:
            Data=response.xpath('//div[@data-hook="review"]')
            if len(Data)>0:
                for row in Data:
                    item={}
                    item.update(ITEM)
                    item['Review Title']=str(row.xpath('.//*[@data-hook="review-title"]/span/text()').get()).strip()
                    item['Review ID']=row.xpath('./@id').get()
                    LINK=row.xpath('.//a[@data-hook="review-title"]/@href').get()
                    if LINK:
                        item['Review URL']=self.domain+LINK
                    else:
                        item['Review URL']=''
                    DATE=str(row.xpath('.//*[@data-hook="review-date"]/text()').get()).strip()
                    if ' em ' in DATE:
                        item['Review Date']=str(DATE).split(' em ')[1]
                        if ' no ' in DATE:
                            item['Review Location']=self.Get_String (str(DATE).split(' no ')[1].split(' em ')[0])
                        elif ' in ' in DATE:
                            item['Review Location']=self.Get_String (str(DATE).split(' in ')[1].split(' em ')[0])
                    item['Review Star']=(str(row.xpath('.//*[contains(@data-hook,"review-star-rating")]/span/text()').get()).strip()).split()[0]
                    item['Review Text']=self.cleanhtml(row.xpath('.//*[@data-hook="review-body"]/span').get())
                    item['Reviewer']=str(row.xpath('.//*[@class="a-profile-name"]/text()').get()).strip()
                    item['Is Verified']='No'
                    Verify=row.xpath('.//*[@data-hook="avp-badge"]')
                    if Verify:
                        item['Is Verified']='Yes'
                    item['# of people']=''
                    NUMBER=row.xpath('.//*[@data-hook="helpful-vote-statement"]/text()').get()
                    if NUMBER:
                        item['# of people']=(str(NUMBER).strip()).split()[0]
                    STYLE=row.xpath('.//*[@data-hook="format-strip"]/text()').get()
                    item['Skin Type']=STYLE
                    item['Style']=''
                    if STYLE and (str(STYLE).strip()).startswith('Style:'):
                        item['Style']=(str(STYLE).replace("Style:", "")).strip()
                    ITEM_DATA={}
                    #print(item)
                    for k,v in self.TMP.items():
                        ITEM_DATA[k]=''
                        if k in item:
                            ITEM_DATA[k]=item[k]
                        else:
                            if v!="":
                                if v in item:
                                    ITEM_DATA[k]=item[v]
                    ITEM_DATA['KEY_']=item['ASIN']+'_'+ITEM_DATA['Review ID']
                    print(ITEM_DATA)
                    yield(ITEM_DATA)

                next_page=response.xpath('//li[@class="a-last"]/a/@href').get()
                if next_page:
                    yield scrapy.Request(self.domain+next_page,callback=self.parse_review,meta={'item':ITEM,'Level':0},cookies=self.cookies,dont_filter=True,headers=self.headers)
            else:
                print('\n ----------- NO REVIEW')
        elif Level<100:
            Level+=1
            print('\n ************ RE-CRAWL')
            yield scrapy.Request(response.url,callback=self.parse_review,meta={'item':ITEM,'Level':Level},cookies=self.cookies,dont_filter=True,headers=self.headers)
    def Get_Number(self,xau):
        KQ=re.sub(r"([^0-9.])","", str(xau).strip())
        return KQ
    def cleanhtml(self,raw_html):
        raw_html=str(raw_html).replace('<br>','\n').replace('</',' \n</')
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext=str(cleantext).replace('\u200f','').replace('\u200e','') .replace('\xa0',' ').replace('\n\n\n\n','\n').replace('\n\n\n','\n').replace('\n\n','\n')
        cleantext=(' '.join(cleantext.split())).strip()
        return cleantext
    def kill_space(self,xau):
        xau=str(xau).replace('\t','').replace('\r','').replace('\n','')
        xau=(' '.join(xau.split())).strip()
        return xau
    def key_MD5(self,xau):
        xau=(xau.upper()).strip()
        KQ=hashlib.md5(xau.encode('utf-8')).hexdigest()
        return KQ
    def Get_String(self,xau):
        KQ=re.sub(r"([^A-Za-z0-9])"," ", str(xau).strip())
        KQ=" ".join(KQ.split())
        return KQ