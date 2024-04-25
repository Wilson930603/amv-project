import datetime
import math
from urllib.parse import urljoin
from centos.items import CentosItem
import scrapy


class CentossSpider(scrapy.Spider):
    name = 'centoss'
    allowed_domains = ['x']
    start_urls = ['https://forums.centos.org/viewforum.php?f=54',
                  'https://forums.centos.org/viewforum.php?f=55',
                  'https://forums.centos.org/viewforum.php?f=56',
                  'https://forums.centos.org/viewforum.php?f=57']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        # "Cookie": "PHPSESSID=kga2orj4nbtqmtgfdadg8tgea6; path=/",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        # "Host": "www.palecek.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
         }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback = self.pagination,headers = self.headers,dont_filter=True)
    def pagination(self,response):
        totalitems = int(response.xpath("//div[@class = 'pagination']/text()").get().replace("topics","").strip())
        itemsperpage =25
        for p in range(0,math.ceil(totalitems/itemsperpage)):
            if p!=0:
                url = response.url+'&start='+str(p*25)
                yield scrapy.Request(url,callback = self.getforums,headers = self.headers,dont_filter=True)
            else:
                yield scrapy.Request(response.url,callback = self.getforums,headers = self.headers,dont_filter=True)
    def getforums(self,response):
        for forum in response.xpath("//div[@class = 'forumbg']/div/ul[@class = 'topiclist topics']/li"):
            forumurl = urljoin("https://forums.centos.org/",forum.xpath(".//dl/dt/div/a[@class = 'topictitle' ]/@href").get())
            yield scrapy.Request(forumurl,callback = self.parse,headers = self.headers,dont_filter = True,meta={'cpage':1})
        # yield scrapy.Request("https://forums.centos.org/viewtopic.php?f=54&t=80138",callback = self.parse,headers = self.headers,dont_filter = True,meta={'cpage':1})
        
    def parse(self, response):
        cpage = response.meta['cpage']
        title = response.xpath("//h2[@class = 'topic-title']/a/text()").get()
        user = response.xpath("//span[@class = 'responsive-hide']/strong/a/text()").extract()
        userurl = response.xpath("//span[@class = 'responsive-hide']/strong/a/@href").extract()
        date = response.xpath("//span[@class = 'responsive-hide']/following-sibling::text()").extract()
        posts = response.xpath("//strong[contains(text(),'Posts')]/following-sibling::a/text()").extract()
        joineddate =response.xpath("//strong[contains(text(),'Joined')]/following-sibling::text()").extract()
        pagepost = int(response.xpath("//div[@class = 'pagination']/text()").get().split(' ')[0].strip())
        totalpage = math.ceil(pagepost/10)
        print(joineddate)
        print(pagepost)
        print(len(title))
        
        for p in range(0,len(user)):

            item = CentosItem()
            item['URL'] = response.url
            item['Title'] = title
            item['User'] = user[p]
            item['UserUrl'] = urljoin("https://forums.centos.org/",userurl[p])
            item['Date'] = datetime.datetime.strptime(date[p].strip().split(" ")[0].strip(), "%Y/%m/%d").strftime("%d/%m/%Y")
            item['Posts'] = posts[p]
            item['Joined'] = datetime.datetime.strptime(joineddate[p].strip().split(" ")[0].strip(), "%Y/%m/%d").strftime("%d/%m/%Y")
            yield item

        if totalpage>cpage:
            print("insideif")
            print(response.url)
            for p in range(1,math.ceil(pagepost/10)):
                try:
                    myurl = response.url.split('&sid')[0].split('&start=')[0]+'&start='+str(p*10)
                except Exception:
                    myurl = response.url+'&start='+str(p*10)
                cpage += 1
                yield scrapy.Request(myurl,callback = self.parse,headers = self.headers,dont_filter=True,meta={'cpage':cpage})


        