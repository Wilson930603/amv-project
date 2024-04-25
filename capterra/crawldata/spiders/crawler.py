import scrapy,re,json
from crawldata.functions import *

class CrawlerSpider(scrapy.Spider):
    name = 'capterra'
    def start_requests(self):
        f=open('urls.txt','r')
        LIST=re.split('\r\n|\n',f.read())
        f.close()
        for URL in LIST:
            if not str(URL).startswith('#'):
                ID=str(URL).split('/p/')[1].split('/')[0]
                url='https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId='+ID+'&size=200&from=0'
                yield scrapy.Request(url,callback=self.parse,meta={'FR':0,'URL':URL})
    def parse(self, response):
        FR=response.meta['FR']
        URL=response.meta['URL']
        DATA=json.loads(response.text)
        Data=DATA['hits']
        for row in Data:
            item={}
            item['Review URL']=URL
            item["Product"]=row['productName']
            item["Role"]=row['reviewer']['jobTitle']
            DT=[]
            try:
                if not row['reviewer']['industry'] is None:
                    DT.append(row['reviewer']['industry'])
            except:
                pass
            try:
                if not row['reviewer']['companySize'] is None:
                    DT.append(row['reviewer']['companySize'])
            except:
                pass
            item["Industry"]=', '.join(DT)
            item["Date"]=row['writtenOn']
            item["Title"]=row['title']
            item["Overall"]=row['generalComments']
            item["Pros"]=row['prosText']
            item["Cons"]=row['consText']
            item["Overall Rating"]=row['overallRating']
            item["Ease of Use"]=row['easeOfUseRating']
            item["Customer Service"]=row['customerSupportRating']
            item["Features"]=row['functionalityRating']
            item["Value for Money"]=row['valueForMoneyRating']
            item["Likelihood to Recommend"]=row['recommendationRating']
            item['Switched From']=''
            DT=[]
            for rs in row['switchedProducts']:
                DT.append(rs['productName'])
            item['Switched From']='; '.join(DT)
            item['Alternatives Considered']=''
            DT=[]
            for rs in row['alternativeProducts']:
                DT.append(rs['productName'])
            item['Alternatives Considered']='; '.join(DT)
            item['Used the software for']=row['reviewer']['timeUsedProduct']
            yield(item)
        if len(Data)>=200:
            FR+=200
            url=str(response.url).split('&from=')[0]+'&from='+str(FR)
            yield scrapy.Request(url,callback=self.parse,meta={'FR':FR,'URL':URL})