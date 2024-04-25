import scrapy,json,os,glob,re,lxml.html.clean,requests

class RunSpider(scrapy.Spider):
    name = 'yelp_reviews'
    start_urls=['https://www.yelp.com']
    def parse(self,response):
        f=open('urls.txt','r')
        URLS=re.split('\r\n|\n', f.read())
        f.close()
        for url in URLS:
            item={}
            item['Yelp URL']=url
            yield scrapy.Request(url,callback=self.parse_data,meta={'ITEM':item,'ID':'','Start':0},dont_filter=True)
    def parse_data(self,response):
        ITEM=response.meta['ITEM']
        ID=response.meta['ID']
        Start=response.meta['Start']
        if response.status==200:
            if ID=='':
                ID=response.xpath('//meta[@name="yelp-biz-id"]/@content').get()
                print(ID)
                if ID:
                    url='https://www.yelp.com/biz/'+ID+'/review_feed?rl=en&q=&sort_by=relevance_desc&start='+str(Start)
                    yield scrapy.Request(url,callback=self.parse_data,meta={'ITEM':ITEM,'ID':ID,'Start':Start},dont_filter=True)
                else:
                    print('RE-CRAWL ROW: ',ITEM['Yelp URL'])
                    yield scrapy.Request(response.url,callback=self.parse_data,meta={'ITEM':ITEM,'ID':'','Start':0},dont_filter=True)
            else:
                DATA=json.loads(response.text)
                REVIEWS=DATA['reviews']
                for row in REVIEWS:
                    user=row['user']
                    item={}
                    item.update(ITEM)
                    item['User Name']=user['markupDisplayName']
                    item['User # of Fridends']=user['friendCount']
                    item['User # of Reviews']=user['reviewCount']
                    item['User # of Pictures']=user['photoCount']
                    item['Location']=user['displayLocation']
                    item['Date']=row['localizedDate']
                    item['Star']=row['rating']
                    item['Text']=self.cleanhtml(row['comment']['text'])
                    item['Useful']=row['feedback']['counts']['useful']
                    yield(item)
                if DATA['pagination']['totalResults']>Start+10:
                    url=str(response.url).split('&start=')[0]+'&start='+str(Start+10)
                    yield scrapy.Request(url,callback=self.parse_data,meta={'ITEM':ITEM,'ID':ID,'Start':Start+10},dont_filter=True)
        else:
            print('RE-CRAWL ROW: ',ITEM['Yelp URL'])
            yield scrapy.Request(response.url,callback=self.parse_data,meta={'ITEM':ITEM,'ID':'','Start':0},dont_filter=True)

    def cleanhtml(self,content):
        content=str(content)
        content=re.sub(">", "> ", content)
        content=re.sub("> =", ">=", content)
        content=content.replace('\u200b','')
        cleaner = lxml.html.clean.Cleaner(allow_tags=[''],remove_unknown_tags=False,style=True,)
        html = lxml.html.document_fromstring(content)
        html_clean = cleaner.clean_html(html)
        Result=html_clean.text_content().strip()
        return self.kill_space(Result)
    def kill_space(self,xau):
        xau=(' '.join(xau.split())).strip()
        return xau