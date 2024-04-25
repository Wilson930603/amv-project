# -*- coding: utf-8 -*-
import scrapy,re,hashlib,html,os
from crawldata.functions import *
class RunSpider(scrapy.Spider):
    name = 'amazon_reviews'
    domain='https://www.amazon.com'
    cookies = {
    'session-id': '136-8912201-3919161',
    'ubid-main': '132-0892785-1462028',
    'x-amz-captcha-1': '1681145638261126',
    'x-amz-captcha-2': '9Z9zcQz8eCkIsP2l5FXaaQ==',
    'x-main': '"d?mFgsN6EhQrkOMYm3oKyt6w2xNDvRC7fOv3xMBw8zRnrnoMG@NxAj47OflTuYSI"',
    'at-main': 'Atza|IwEBIN1MaGkOsFI23c1MMo9gmIWnUkSZtBCYSd_gz7T0bQFCQLC1DiKoXA4CaRT-5AEidsK3eYBGufpGSNoG72C-kh7s5De6RgaXUdMZ0XpusV9f9h73lAz4wn1xZiM3PGtuLltMEh9PQXIj4sQWIl1revAhNSgf6SzSH2aoWjiWW-iqnN4ZM-n7_YD_vRJNppQNipkNZ0NvEuswXQCOsbPFNw1a',
    'sess-at-main': '"lcTJ7eJ7gfuMd6zSmCbbM9ctLtNz6FANttcACfElKwQ="',
    'sst-main': 'Sst1|PQH-gA5J7mlzX0LfMZoZSDbGCVn6nAJLbN1nOPKq8--NjM1o_MjMPpdA8FKJDYuhs9tofiYkifgAgFO07rkTua-_FXE7bKhSdqRLKM8DU5MTL35b5LtEmr8B8PiqhqGG8s6a6fbYdhwTAHkVCYMDxU9d5zDRQrdf-lQuirnvE_SdqFdAsCrf1n-hniu-9yrgqUK5PZW0MibV7SWoODHv0vuuI6rPnh7oqiKinl35LGIPHq4_FZNhKkorX8eDgPYYXswXPfMXqGHqMfwLZLwP126Apfp-iXPr8deidxZB6Ot6gKs',
    'lc-main': 'en_US',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'session-token': 'gtoez9VOpYRMEPBhkZm2WzKSDJBoPQx5OZLZFE+jf3i0Rpr/7QrMLIsUThB1gmxh0Ens9PhWpAs0YTRfkREMXr0ACuD0XMaT/8NISflWdYZorscdlX62bZ39kf3KcEINaS4ESWgV4OXREzoGQu2o7HVW5ygg0fB42lh2vhGCCrCK1inv7oKsidYPLo5PM8PIArwJX+KffJ78Yqk5Qerp3FWixIUdC1P19kl448NCrudXQxoSoUp3P8iFCQOqFWn3',
    'csm-hit': 'tb:7RB2VSJDEPDCHKYT3ZVQ+s-7RB2VSJDEPDCHKYT3ZVQ|1681867519156&t:1681867519156&adb:adblk_no',
}

    TMP={"Product":"","Retailer Name":"","Title":"","Review Star":"","Is Verified":"","Has Response":"","Review Title":"","Review Text":"","Review Date":"","Review URL":"","Category":"","Is Discontinued By Manufacturer":"","Product Dimensions":"","Item model number":"","UPC":"","Manufacturer":"","ASIN":"","Brand":"","Ingredients":"","Active Ingredient":"Liquid Volume","Skin Type":"","Style":"","Material type free":"","Review Location":"","Review ID":"","Reviewer":"","# of people":""}
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
                    urls=str(LIST[i]).split('~')
                    item={}
                    item['ID']=i+1
                    item['Product']=str(urls[0]).strip()
                    item['Retailer Name']=str(LIST[i]).split('/')[2]
                    url=str(urls[1]).strip()
                    yield scrapy.Request(url,callback=self.parse,meta={'item':item,'Level':0},dont_filter=True,cookies=self.cookies)
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
                if not 'ASIN' in item:
                    item['ASIN']=str(response.url).split('/dp/')[1].split('/')[0]
                url_review=self.domain+'/'+Get_String(item['Title'])+'/product-reviews/'+item['ASIN']+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageSize=20'
                yield scrapy.Request(url_review,callback=self.parse_review,meta={'item':item,'Level':0},cookies=self.cookies)
            else:
                print('\n ============= NOT FOUND')
                #yield scrapy.Request(response.url,callback=self.parse,meta={'item':item,'Level':Level},dont_filter=True,cookies=self.cookies)
        elif Level<100:
            Level+=1
            print('\n ************ RE-CRAWL')
            yield scrapy.Request(response.url,callback=self.parse,meta={'item':item,'Level':Level},dont_filter=True,cookies=self.cookies)
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
                        item['Review URL']=self.domain+str(row.xpath('.//a[@data-hook="review-title"]/@href').get()).strip()
                    else:
                        item['Review URL']=''
                    DATE=str(row.xpath('.//*[@data-hook="review-date"]/text()').get()).strip()
                    if ' on ' in DATE:
                        item['Review Date']=str(DATE).split(' on ')[1]
                        if ' in the ' in DATE:
                            item['Review Location']=self.Get_String (str(DATE).split(' in the ')[1].split(' on ')[0])
                        elif ' in ' in DATE:
                            item['Review Location']=self.Get_String (str(DATE).split(' in ')[1].split(' on ')[0])
                    item['Review Star']=(str(row.xpath('.//*[contains(@data-hook,"review-star-rating")]/span/text()').get()).strip()).split()[0]
                    VERI=str(row.xpath('.//*[@data-hook="avp-badge"]/text()').get()).strip()
                    if 'Verifizierter' in VERI:
                        item['Is Verified']='Yes'
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
                    yield scrapy.Request(self.domain+next_page,callback=self.parse_review,meta={'item':ITEM,'Level':0},cookies=self.cookies,dont_filter=True)
            else:
                print('\n ----------- NO REVIEW')
        elif Level<100:
            Level+=1
            print('\n ************ RE-CRAWL')
            yield scrapy.Request(response.url,callback=self.parse_review,meta={'item':ITEM,'Level':Level},cookies=self.cookies,dont_filter=True)
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