import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'booking_reviews'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    para_list=['aid','label','sid','cc1','pagename','srpvid','type','offset','rows']
    def start_requests(self):
        LIST=re.split('\r\n|\n', open('urls.txt','r').read())
        for LS in LIST:
            LS=str(LS).split('?')
            pagename=(str(LS[0]).split('/')[-1]).split('.')[0]
            paras=str(LS[1]).split('&')
            para={}
            para['pagename']=(str(LS[0]).split('/')[-1]).split('.')[0]
            para['cc1']=str(LS[0]).split('/')[-2]
            for pr in paras:
                if '=' in pr:
                    key=pr.split('=')[0]
                    val=pr.split('=')[1]
                    if not key in para:
                        para[key]=val
            para['type']='total'
            para['offset']=0
            para['rows']=10
            reivew_para=[]
            for k in self.para_list:
                if k in para:
                    reivew_para.append(k+'='+str(para[k]))
            url='https://www.booking.com/reviewlist.en-gb.html?'+('&'.join(reivew_para))
            yield scrapy.Request(url,callback=self.parse,meta={'para':para})
    def parse(self, response):
        para=response.meta['para']
        Data=response.xpath('//ul[@class="review_list"]/li')
        for row in Data:
            item={}
            item['KEY_']=row.xpath('./@data-review-url').get()
            item['page_name']=para['pagename']
            item['name']=row.xpath('.//span[@class="bui-avatar-block__title"]/text()').get()
            item['country']=row.xpath('.//span[@class="bui-avatar-block__subtitle"]/text()').get()
            item['room_type']=str(row.xpath('.//div[@data-room-id]//div[@class="bui-list__body"]/text()').get()).strip()
            item['reservation_nights']=(str(row.xpath('.//ul[contains(@class,"__stay-date")]//div[@class="bui-list__body"]/text()').get()).replace(' ·', '')).strip()
            item['reservation_date']=str(row.xpath('.//ul[contains(@class,"__stay-date")]//div[@class="bui-list__body"]/span/text()').get()).strip()
            item['reservation_people']=str(row.xpath('.//ul[contains(@class,"__traveller_type")]//div[@class="bui-list__body"]/text()').get()).strip()
            item['review_date']=(str(row.xpath('.//div[contains(@class,"c-review-block__right")]//span[@class="c-review-block__date"]/text()').get()).replace('Reviewed: ', '')).strip()
            item['review_title']=str(row.xpath('.//div[contains(@class,"c-review-block__right")]//h3/text()').get()).strip()
            item['review_pros']=''
            item['review_cons']=''
            TYPES=row.xpath('.//div[@class="c-review"]/div[@class="c-review__row"]')
            for TYPE in TYPES:
                TITLE=str(TYPE.xpath('.//span[@class="bui-u-sr-only"]//text()').get())
                if 'Disliked' in TITLE:
                    item['review_cons']=TYPE.xpath('.//span[@class="c-review__body"]/text()').get()
                elif 'Liked' in TITLE:
                    item['review_pros']=TYPE.xpath('.//span[@class="c-review__body"]/text()').get()
            item['review_score']=row.xpath('.//div[@class="bui-review-score__badge"]/text()').get()
            yield(item)
        if len(Data)>0:
            para['offset']=para['offset']+para['rows']
            reivew_para=[]
            for k in self.para_list:
                if k in para:
                    reivew_para.append(k+'='+str(para[k]))
            url='https://www.booking.com/reviewlist.en-gb.html?'+('&'.join(reivew_para))
            yield scrapy.Request(url,callback=self.parse,meta={'para':para})

        
