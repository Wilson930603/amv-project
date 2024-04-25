import scrapy,json,re,os,platform
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'sullygnome'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    domain='https://www.sullygnome.com'
    URL_LIST=re.split('\r\n|\n',open(name+'_urls.txt','r',encoding='utf-8').read())
    URLS={}
    URLS['Average Monthly Viewers']='https://sullygnome.com/api/charts/barcharts/getconfig/gamemonthlystatsaverageviewers/7/~~ID~~/~~Subreddit~~/AverageViewers/%20/0/0/%20/1/0/'
    URLS['Peak Viewership']='https://sullygnome.com/api/charts/barcharts/getconfig/gamemonthlystatspeakviewers/7/~~ID~~/~~Subreddit~~/PeakViewers/%20/0/0/%20/1/0/'
    URLS['Total Hours Watched']='https://sullygnome.com/api/charts/barcharts/getconfig/gamemonthlystatswatchtime/7/~~ID~~/~~Subreddit~~/WatchTime/%20/0/0/%20/1/0/'
    URLS['Total Hours Streamed']='https://sullygnome.com/api/charts/barcharts/getconfig/gamemonthlystatsstreamtime/7/~~ID~~/~~Subreddit~~/StreamTime/%20/0/0/%20/1/0/'
    URLS['Average Channels Streaming']='https://sullygnome.com/api/charts/barcharts/getconfig/gamemonthlystatsaveragechannels/7/~~ID~~/~~Subreddit~~/AverageChannels/%20/0/0/%20/1/0/'
    URLS['Peack Channels Streaming']='https://sullygnome.com/api/charts/barcharts/getconfig/gamemonthlystatspeakchannels/7/~~ID~~/~~Subreddit~~/PeakChannels/%20/0/0/%20/1/0/'
    URLS['Average Viewer Rank']='https://sullygnome.com/api/charts/linecharts/getconfig/gamemonthlystatsaverageviewersrank/7/0/~~ID~~/~~Subreddit~~/AverageViewerRank/%20/0/0/%20/0/'
    URLS['Peak Viewer Rank']='https://sullygnome.com/api/charts/linecharts/getconfig/gamemonthlystatspeakviewersrank/7/0/~~ID~~/~~Subreddit~~/PeakViewerRank/%20/0/0/%20/0/'
    URLS['Average Channels Rank']='https://sullygnome.com/api/charts/linecharts/getconfig/gamemonthlystatsaveragechannelsrank/7/0/~~ID~~/~~Subreddit~~/AverageChannelRank/%20/0/0/%20/0/'
    URLS['Peak Channels Rank']='https://sullygnome.com/api/charts/linecharts/getconfig/gamemonthlystatspeakchannelsrank/7/0/~~ID~~/~~Subreddit~~/PeakChannelRank/%20/0/0/%20/0/'
    def start_requests(self):
        for URL in self.URL_LIST:
            URL_STR=str(URL).split('~')
            Game=URL_STR[0]
            Subreddit=(str(URL_STR[1]).split('/')[4]).replace('_',' ')
            ID=URL_STR[2]
            KEYS=list(self.URLS.keys())
            K=KEYS[0]
            url=self.URLS[K]
            url=str(url).replace('~~Subreddit~~',Subreddit).replace('~~ID~~',ID)
            del KEYS[0]
            DATASET=[]
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'Subreddit':Subreddit,'Game':Game,'K':K,'KEYS':KEYS,'ID':ID,'DATASET':DATASET})
    def parse(self, response):
        K=response.meta['K']
        ID=response.meta['ID']
        KEYS=response.meta['KEYS']
        Game=response.meta['Game']
        Subreddit=response.meta['Subreddit']
        DATASET=response.meta['DATASET']
        Data=json.loads(response.text)
        data=Data['data']['labels']
        dataset=Data['data']['datasets'][0]['data']
        if len(KEYS)==(len(self.URLS)-1):
            for i in range(len(data)):
                item={}
                item['_id']=key_MD5(Game+data[i])
                item['Game']=Game
                item['Month']=data[i]
                item[K]=dataset[i]
                DATASET.append(item)
        else:
            for i in range(len(dataset)):
                DATASET[i][K]=dataset[i]
        if len(KEYS)>0:
            K=KEYS[0]
            url=self.URLS[K]
            url=str(url).replace('~~Subreddit~~',Subreddit).replace('~~ID~~',ID)
            del KEYS[0]
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'Subreddit':Subreddit,'Game':Game,'K':K,'KEYS':KEYS,'ID':ID,'DATASET':DATASET})
        else:
            for row in DATASET:
                yield(row)


