import scrapy,json,re,os,platform,requests
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'g2_reviews'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-None-Match': 'W/8bc313e2516b45fc556a4ff61f252182',
}
    cookies={}
    CK=re.split('\r\n|\n',open('cookies.txt').read())
    for rs in CK:
        rs=rs.split('\t')
        if len(rs)==7:
            cookies[rs[-2]]=rs[-1]
    conn=None
    def start_requests(self):
        yield scrapy.Request(self.URL,callback=self.parse,dont_filter=True)
    def parse(self, response):
        URLS=re.split('\r\n|\n',open('urls.txt','r',encoding='utf-8').read())
        for URL in URLS:
            RUN=True
            Page=1
            while RUN:
                URL_LIST=str(URL).split('~')
                url=str(URL_LIST[1]).split('#')[0]+'?page='+str(Page)
                res=requests.get(url,headers=self.headers,cookies=self.cookies)
                while "<title>Just a moment...</title>" in res.text:
                    CK=re.split('\r\n|\n',open('cookies.txt').read())
                    for rs in CK:
                        rs=rs.split('\t')
                        if len(rs)==7:
                            self.cookies[rs[-2]]=rs[-1]
                    input("Get cookies and press ENTER to continues !!!")
                    res=requests.get(url,headers=self.headers,cookies=self.cookies)
                response=scrapy.Selector(text=res.text)
                Data=response.xpath('//div[@id="reviews"]//div[@itemprop="review"]')
                for row in Data:
                    item={}
                    item['Name']=row.xpath('.//meta[@itemprop="name"]/@content').get()
                    DT=row.xpath('.//div[contains(@class,"fw-regular")]/div').getall()
                    for i in range(len(DT)):
                        DT[i]=cleanhtml(DT[i])
                    item['Role']=''
                    item['Business Size']=''
                    if len(DT)>0:
                        item['Business Size']=DT[-1]
                        del DT[-1]
                        item['Role']='; '.join(DT)
                    TAGS=row.xpath('.//div[@class="tags--teal"]/div')
                    if TAGS:
                        item['Validated']='Yes'
                    else:
                        item['Validated']='No'
                    item['Source']=URL_LIST[0]
                    Star=row.xpath('.//div[contains(@class,"stars large xlarge--medium-down")]/@class').get()
                    Star=str(Star).split('stars-')[1]
                    item['Rating']=round(int(Star)/2,1)
                    item['Date']=row.xpath('.//time/@datetime').get()
                    item['Title']=str(row.xpath('.//h3[@itemprop="name"]/text()').get()).strip()
                    DT=row.xpath('.//div[@itemprop="reviewBody" and not(@data-poison-text)]/div')
                    for rs in DT:
                        TXT=cleanhtml(str(rs.xpath('./div').get()).replace('</p>','</p>\n'))
                        item[str(rs.xpath('./h5/text()').get()).strip()]=TXT
                    yield(item)
                next_page=response.xpath('//li/a[contains(text(),"Next")]')
                if next_page:
                    Page+=1
                else:
                    RUN=False