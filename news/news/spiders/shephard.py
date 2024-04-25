import datetime
import re
from news.items import NewsItem
import scrapy


class ShephardSpider(scrapy.Spider):
    name = 'shephard'
    # allowed_domains = ['x']
    start_urls = ['https://www.shephardmedia.com']
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_gcl_au=1.1.1905930614.1681972381; _gid=GA1.2.75161684.1681972382; _fbp=fb.1.1681972383564.639505139; ln_or=eyIzOTAxMDAxIjoiZCJ9; prism_26945780=b1eae664-56b2-464b-88f3-6adca5b6d654; shephard-policy-banner=hide; __gads=ID=1c6aacaca9ea3dfb:T=1681972395:S=ALNI_Mb2u7qvqwYXLZavXJVXv2ETdD3DiQ; __gpi=UID=00000c068f176ce8:T=1681972395:RT=1681972395:S=ALNI_Mb5_M__Z5LZX-NueBPWVCPs3k7YSQ; _ga=GA1.1.1002676968.1681972382; _ga_LX9QGV1KWR=GS1.1.1681972382.1.1.1681974037.60.0.0; _ga_ECP5TTBQYD=GS1.1.1681972382.1.1.1681974037.60.0.0',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback = self.pagination,headers = self.headers)

    def pagination(self,response):
        for i in range(1,1951):
            url = 'https://www.shephardmedia.com/news/?page='+str(i)
            yield scrapy.Request(url,callback = self.parse,headers = self.headers)

    def parse(self, response):
        for article in response.xpath("//section[@class = 'article-list']/ul/li"):
            title = article.xpath("./h2/a/@title").get()
            link = article.xpath("./h2/a/@href").get()
            category = article.xpath("./h4/a/@title").get()
            date = article.xpath("./p/text()").get().strip()
            date = datetime.date(day = int(re.sub(r'[^\d]','',date.split(' ')[0])),
                                 month=int(datetime.datetime.strptime(date.split(' ')[1], '%B').month),
                                 year = int(date.split(' ')[2])).strftime('%d/%m/%Y')
            item = NewsItem()

            item['Category'] = category
            item['Title'] = title
            item['Date'] = date
            item['URL'] = link  
            yield item

