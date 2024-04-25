import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'reddit'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    domain='https://www.reddit.com'
    URL_LIST=re.split('\r\n|\n',open(name+'_urls.txt','r',encoding='utf-8').read())
    TOKEN=None
    def start_requests(self):
        url='https://www.reddit.com/account/sso/one_tap/?experiment_d2x_safari_onetap=enabled&experiment_d2x_google_sso_gis_parity=enabled&experiment_d2x_am_modal_design_update=enabled&experiment_mweb_sso_login_link=enabled&shreddit=true&use_accountmanager=true'
        yield scrapy.Request(url,callback=self.get_token,dont_filter=True)
    def get_token(self,response):
        self.TOKEN=response.xpath('//input[@name="csrf_token"]/@value').get()
        print(self.TOKEN)
        for URL in self.URL_LIST:
            # URL=self.URL_LIST[0]
            URL_STR=str(URL).split('~')
            Game=URL_STR[0]
            Subreddit=str(URL_STR[1]).split('/')[4]
            yield scrapy.Request('https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after=&t=DAY&name='+Subreddit,callback=self.parse,dont_filter=True,meta={'Subreddit':Subreddit,'Game':Game})
    def parse(self, response):
        Game=response.meta['Game']
        Subreddit=response.meta['Subreddit']
        Data=response.xpath('//shreddit-post')
        more_cursor=None
        fields=['id','permalink','comment-count','created-timestamp','post-title','post-type','score','author-id','author']
        for row in Data:
            url=row.xpath('./@content-href').get()
            item={}
            for alt in row.attrib:
                item[alt]=row.attrib[alt]
            if 'more-posts-cursor' in item:
                more_cursor=item['more-posts-cursor']
            item['permalink']=self.domain+item['permalink']
            item_data={}
            item_data['Game']=Game
            item_data['Subreddit']=Subreddit
            for k in fields:
                if k in item:
                    item_data[k]=item[k]
                else:
                    item_data[k]=""
            yield scrapy.Request(item['permalink'],callback=self.parse_content,meta={'item_data':item_data},dont_filter=True)
        if more_cursor:
            url='https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after='+more_cursor+'%3D%3D&t=DAY&name='+Subreddit
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'Subreddit':Subreddit,'Game':Game})
    def parse_content(self,response):
        item_data=response.meta['item_data']
        item_data['post-title']=item_data['post-title']+' \n ' + cleanhtml(response.xpath('//div[@slot="text-body"]').get())
        item_data['comment_url']='https://www.reddit.com/svc/shreddit/comments/runescape/'+item_data['id']
        yield scrapy.Request(item_data['comment_url'],callback=self.parse_comments,meta={'item_data':item_data},dont_filter=True)
    def parse_comments(self,response):
        item_data=response.meta['item_data']
        Data=response.xpath('//shreddit-comment')
        dt={'Game':'Game','Subreddit':'Subreddit','Post Date':'created-timestamp','Post':'post-title','Post Votes':'score','Post URL':'permalink','Comment Date':'comment_time','Comment':'comment','Comment Votes':'comment_votes'}
        cursor=None
        next_url=None
        for row in Data:
            item={}
            item.update(item_data)
            item['comment_id']=row.xpath('.//@thingid').get()
            item['comment_time']=row.xpath('.//faceplate-timeago/@ts').get()
            item['comment']=cleanhtml(row.xpath('.//div[@id="-post-rtjson-content"]').get())
            item['comment_votes']=row.xpath('./@score').get()
            cur=str(row.xpath('.//input[@name="cursor"]/@value').get())
            if len(str(cur))>len(str(cursor)):
                cursor=cur
            it_dt={}
            for k,v in dt.items():
                if v in item:
                    it_dt[k]=item[v]
                else:
                    it_dt[k]=''
            it_dt['Post Date']=str(it_dt['Post Date']).split('T')[0]
            it_dt['Comment Date']=str(it_dt['Comment Date']).split('T')[0]
            it_dt['_id']=key_MD5(str(it_dt['Game'])+str(item['Subreddit'])+str(it_dt['Comment Date'])+str(it_dt['Post URL'])+str(it_dt['Comment'])+str(it_dt['Comment Votes']))
            myquery = {"_id": it_dt['_id']}
            mydoc = self.mycol.find(myquery)
            FOUND=False
            for x in mydoc:
                FOUND=True
            if FOUND==False:
                yield(it_dt)
            else:
                print('Existed !!!!')
        nurls=response.xpath('//faceplate-partial[contains(@src,"more-comments") and (not(contains(@src,"startingDepth")))]/@src').get()
        cursors=(response.xpath('//input[@name="cursor"]/@value').getall())
        if nurls:
            data = {'cursor': cursors[-1],'csrf_token': self.TOKEN}
            next_url=self.domain+nurls
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0','Accept': 'text/vnd.reddit.partial+html, text/html;q=0.9','Accept-Language': 'en-GB,en;q=0.5','Content-Type': 'application/x-www-form-urlencoded','Referer': item_data['permalink'],'Origin': 'https://www.reddit.com','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','Connection': 'keep-alive'}
            yield scrapy.Request(next_url,method="POST",body=json.dumps(data),callback=self.parse_comments,meta={'item_data':item_data},dont_filter=True)
        
        

        
