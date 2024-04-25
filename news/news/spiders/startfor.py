from datetime import datetime
import re
from urllib.parse import urljoin
from news.items import NewsItem
import scrapy
import json
import pytz


class ShephardSpider(scrapy.Spider):
    name = 'startfor'
    # allowed_domains = ['x']
    start_urls = ['https://www.shephardmedia.com']
    flag = True
    def start_requests(self):
        # import requests/

        url = "https://worldview.stratfor.com/api/next-api/content/list"
        i = 0
        while self.flag:
            
            payload = "{\"page\":"+str(i)+",\"offset\":null,\"limit\":\"12\",\"type\":[\"article\",\"sectioned_content\"],\"sort_by\":[\"created\",\"DESC\"],\"credentials\":\"include\",\"options\":{\"exclude_homepage_highlighted_content\":1,\"exclude_global_perspectives\":0,\"exclude_snapshots\":0,\"exclude_interactives\":0}}"
            # payload = "{\"page\":10,\"offset\":null,\"limit\":\"12\",\"type\":[\"article\",\"sectioned_content\"],\"sort_by\":[\"created\",\"DESC\"],\"credentials\":\"include\",\"options\":{\"exclude_homepage_highlighted_content\":1,\"exclude_global_perspectives\":0,\"exclude_snapshots\":0,\"exclude_interactives\":0}}"
            
            headers = {
            'Accept': 'application/json, text/plain, */*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Content-Length': '261',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'ev_sid=6447ebed44fa284c787c8548; ev_did=6447ebed44fa284c787c8547',
            'Host': 'worldview.stratfor.com',
            'Origin': 'https://worldview.stratfor.com',
            'Pragma': 'no-cache',
            'Referer': 'https://worldview.stratfor.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }   
            i += 1
            # self.flag = False
            yield scrapy.Request(url,method = 'POST',headers = headers,body= payload,callback = self.parse, dont_filter = True)
        
    def parse(self,response):
        jo = json.loads(response.body)
        # print(jo)
        # input("wait")
        if jo['nodes'] != []:
            for d in jo['nodes']:
                title = d['title']
                date = pytz.timezone('Europe/London').localize(datetime.utcfromtimestamp(int(d['created'])),is_dst=None).strftime('%d/%m/%Y')
                
                try:
                    category = d['article_type']['name']
                except Exception:
                    category = None

                if category == 'Columns' and type(d['column_type']) == type({}):
                    category = d['column_type']['name']
                elif category == 'Media' and type(d['media_type']) == type({}):
                    category = d['media_type']['name']
                elif category == None:
                    category = d['forecast_type']['name'] + ' Forecast'
                url = urljoin("https://worldview.stratfor.com/",d['path_alias'])
                if title == 'Vulnerabilities in the Terrorist Attack Cycle':
                    print(int(d['created']))
                    input("wait")
                item = NewsItem()
                item['Category'] = category
                item['Title'] = title
                item['Date'] = date
                item['URL'] = url
                yield item
        else:
            self.flag = False


