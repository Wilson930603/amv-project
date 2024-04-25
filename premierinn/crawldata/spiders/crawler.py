import scrapy,json,re
from crawldata.functions import *
from datetime import datetime,timedelta

class CrawlerSpider(scrapy.Spider):
    name = 'premierinn'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    PRE_URL='https://www.premierinn.com/gb/en/'
    ROOM_TYPE={'DB':'double','DIS':'accessible','FAM':'family','TWIN':'twin'}
    def start_requests(self):
        url='https://www.premierinn.com/gb/en/hotels.html'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        Data=response.xpath('//h4/a/@href').getall()
        for url in Data:
            yield scrapy.Request(self.PRE_URL+url,callback=self.parse_list)
    def parse_list(self,response):
        Data=response.xpath('//google-maps/@hotels').get()
        if Data:
            Data=json.loads(Data)
            for ROW in Data:
                url='https://www.premierinn.com/gb/en/hoteldirectory/'+(ROW['id'][0])+'/'+ROW['id']+'.complete.data'
                yield scrapy.Request(url,callback=self.parse_data,meta={'ROW':ROW})
    def parse_data(self,response):
        ROW=response.meta['ROW']
        Data=json.loads(response.text)
        # Get the first of room type
        ROW['URL']=self.PRE_URL+'hotels'+ Data['links']['detailsPage']+'.html'
        ROW['facilityList']=Data['hotelRoomConfiguration']['tabItems']
        DAY=0
        START=(datetime.now()+timedelta(days=DAY)).strftime('%Y-%m-%d')
        END=(datetime.now()+timedelta(days=(DAY+1))).strftime('%Y-%m-%d')
        url='https://api.whitbread.co.uk/booking/hotels/'+ROW['id']+'/availability?adults=1&arrival='+START+'&bookingChannel=WEB&cellCodes=&children=0&cot=0&country=GB&departure='+END+'&language=en&rooms=1&type=DB'
        yield scrapy.Request(url,callback=self.parse_price,meta={'ROW':ROW,'DAY':DAY})
    def parse_price(self,response):
        ROW=response.meta['ROW']
        DAY=response.meta['DAY']
        Data=json.loads(response.text)
        if Data['available']==True and len(Data['ratePlans'])>0:
            item={}
            item['url']=ROW['URL']
            item['hotel name']=ROW['name']
            item['date']=(datetime.now()+timedelta(days=DAY)).strftime('%Y-%m-%d')
            TYPE=0
            try:
                room = Data['ratePlans'][0]['rooms'][0]
                if 'RB' in room['lettingType']:
                    item['price'] = room['totalCost']['amount']
                else:
                    item['price'] = room['alternativeRooms'][0]['totalCost']['amount']
                TYPE=1
            except:
                item['price']=Data['ratePlans'][0]['totalCost']['amount']
            RTYPE=self.ROOM_TYPE[Data['ratePlans'][0]['rooms'][0]['type']]
            FAC=[]
            for rs in ROW['facilityList']:
                if TYPE==0:
                    if rs['room']==RTYPE and "Standard" in rs['roomType']:
                        FAC=[]
                        for rcs in rs['facilityList']:
                            FAC.append(rcs['legend'])
                else:
                    if rs['room']==RTYPE and "Premier" in rs['roomType']:
                        FAC=[]
                        for rcs in rs['facilityList']:
                            FAC.append(rcs['legend'])
            item['amenities']=', '.join(FAC)
            item['KEY_']=ROW['id']+'_'+(datetime.now()+timedelta(days=DAY)).strftime('%Y-%m-%d')
            yield(item)
        DTIME=datetime.now()+timedelta(days=DAY)
        CHK=True
        if DTIME.year>datetime.now().year+1:
            CHK=False
        elif DTIME.year==datetime.now().year+1 and DTIME.month>datetime.now().month:
            CHK=False
        if CHK==True:
            DAY+=1
            START=(datetime.now()+timedelta(days=DAY)).strftime('%Y-%m-%d')
            END=(datetime.now()+timedelta(days=(DAY+1))).strftime('%Y-%m-%d')
            url='https://api.whitbread.co.uk/booking/hotels/'+ROW['id']+'/availability?adults=1&arrival='+START+'&bookingChannel=WEB&cellCodes=&children=0&cot=0&country=GB&departure='+END+'&language=en&rooms=1&type=DB'
            yield scrapy.Request(url,callback=self.parse_price,meta={'ROW':ROW,'DAY':DAY})
