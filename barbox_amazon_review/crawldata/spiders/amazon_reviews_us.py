# -*- coding: utf-8 -*-
import scrapy,re,hashlib,html,os
from crawldata.functions import *
from datetime import datetime
class RunSpider(scrapy.Spider):
    name = 'amazon_reviews_us'
    domain='https://www.amazon.com'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    cookies = {
    'session-id': '131-0125478-6199950',
    'ubid-main': '133-3377614-8672136',
    'lc-main': 'en_US',
    'session-token': 'UDzKlwp5UmnIIfZyroMMFPJw0+w//oxfg74z80U4pxFB3+E+zAXPo5uKwvQh+39lqnYxlJmMV+aF6NVoV4IQWw3qMW9gAIx3TzFbC437GVZitzfYL/lJlGwdvO89eoCkCjYdHYyl0XnDDtsivIIbOVfGhgFcthI69VOt+TqWaNXzt4h99wDKkE72zgCXUpnVLeE5d+SdmG1JjdSlr9c2MSpzZWjg4QaKcVzt559+gsWc0NlIBh4vKGNoE1hlz+xW',
    'x-main': '"nRe15R2xOxeQ4?zLy?W0e4acHJiZr0VDvbvUq25RcI1wmViGJnvnUJ?insU37lUd"',
    'at-main': 'Atza|IwEBIFwaQcsQMb1qGMThAg2Wi3pi9Nt0AA68VUrJaLmH1Q4HvmMFtH0ck-hCZkW5UrXYzbx2b0ZI-djvdEA2ua4TnoYE3CHn4o2sF2UNbSiXNQjHkTDq_FV1Qj7DFfkRR0ZxVyESUPD81zuIHP0v6dzHirhjotRuMDp13tholBA0jrGBSYulCJlB_IU_dYZRcAVtV_xkhNzUqfIP6774_4bnDlxmnxF8GIhKAKnOAHuNOozMCQ',
    'sess-at-main': '"7DZiMRt+T+0qpPS+gftwInV9MAl/aVvuywKKdqccHXs="',
    'sst-main': 'Sst1|PQHziVCxOWKQEWlXZAmNgbOXCUCLRDaQfHX6W6rRwTXmDoprGFM94l4HbUolWHAH4eucWR4T2ac7fUY5Je7VHSe2I36tCqk0Uy0WfkJfb0cf8IshbispN-YooLyF5CYhrS_43GMgA_ib0Xj7347u_5xuBOVaz4d3rf4gP5eo4ufYvBEsEOrqEo1aggGNQ3eul0-d4DVLmPhkzpG6RMskJGooGPPyUG5yxE3weLkZsKH3KL25jII6ZAfAbCznzAdBgwbZDfhLY5hFYSxouhdsnTBMi5GqHgkIFHeNmlacSYlD3WE',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'csm-hit': 'tb:517ENA8GBWK5E75C5CN8+s-4E7AVB796A6NM37VY77T|1689949704179&t:1689949704179&adb:adblk_no',
}

    headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'device-memory': '8',
    'downlink': '9.15',
    'dpr': '1.25',
    'ect': '4g',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.25',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1536',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'viewport-width': '1536',
}


    def start_requests(self):
        LIST=re.split("\r\n|\n",open('urls.txt','r').read())
        for LS in LIST:
            row=str(LS).split('~')
            item={}
            item['Category']=row[0]
            item['Subcategory']=row[1]
            item['Product Name']=row[2]
            item['Link']=row[3]
            item['Name']=''
            item['# Star']=''
            item['Date']=''
            item['Title']=''
            item['Description']=''
            item['# Helpful']=''
            URL=str(item['Link']).split('/')
            url='https://www.amazon.com/'+URL[3]+'/product-reviews/'+URL[5]+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
            print('CRAWLING:',url)
            yield scrapy.Request(url,callback=self.parse_review,meta={'item':item,'URL':url,'Level':0},cookies=self.cookies,headers=self.headers)
    def parse_review(self,response):
        ITEM=response.meta['item']
        Level=response.meta['Level']
        URL=response.meta['URL']
        if response.status==200 and '(MEOW)' in response.text:
            Data=response.xpath('//div[@data-hook="review"]')
            if len(Data)>0:
                for row in Data:
                    item={}
                    item.update(ITEM)
                    item['Title']=str(row.xpath('.//*[@data-hook="review-title"]/span/text()').get()).strip()
                    DATE=str(row.xpath('.//*[@data-hook="review-date"]/text()').get()).strip()
                    if ' on ' in DATE:
                        item['Date']=str(DATE).split(' on ')[1]
                    item['# Star']=(str(row.xpath('.//*[contains(@data-hook,"review-star-rating")]/span/text()').get()).strip()).split()[0]
                    item['Description']=cleanhtml(row.xpath('.//*[@data-hook="review-body"]/span').get())
                    item['Name']=str(row.xpath('.//*[@class="a-profile-name"]/text()').get()).strip()
                    NUMBER=row.xpath('.//*[@data-hook="helpful-vote-statement"]/text()').get()
                    if NUMBER:
                        item['# Helpful']=(str(NUMBER).strip()).split()[0]
                    yield(item)
                next_page=response.xpath('//ul[@class="a-pagination"]//li[@class="a-last"]/a/@href').get()
                if next_page:
                    next_page=self.domain+next_page
                    print('\n ================',next_page)                    
                    print('CRAWLING:',next_page)
                    yield scrapy.Request(next_page,callback=self.parse_review,meta={'item':ITEM,'URL':next_page,'Level':0},cookies=self.cookies,dont_filter=True,headers=self.headers)
            else:
                print('\n ----------- NO REVIEW')
        elif Level<100:
            Level+=1
            print('\n ************ RE-CRAWL')
            print('CRAWLING:',URL)
            yield scrapy.Request(URL,callback=self.parse_review,meta={'item':ITEM,'URL':URL,'Level':Level},cookies=self.cookies,dont_filter=True,headers=self.headers)