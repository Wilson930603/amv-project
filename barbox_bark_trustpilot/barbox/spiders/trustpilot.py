import scrapy,json,csv,os, requests, urllib, shutil
class CrawlerSpider(scrapy.Spider):
    name = 'trustpilot'
    cookies = {
        'TP.uuid': 'c52c5524-4dab-4418-b1c1-501cc36ce21d',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Jul+20+2023+16%3A19%3A02+GMT%2B0700+(Indochina+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=f3b8dff4-fff9-4744-a349-00339f5bad27&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1',
        'ajs_anonymous_id': '7566c0a0-c304-44d3-adba-59b2163f0bcb',
        'OptanonAlertBoxClosed': '2023-07-20T09:19:02.074Z',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        # 'Cookie': 'TP.uuid=c52c5524-4dab-4418-b1c1-501cc36ce21d; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jul+20+2023+16%3A19%3A02+GMT%2B0700+(Indochina+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=f3b8dff4-fff9-4744-a349-00339f5bad27&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; ajs_anonymous_id=7566c0a0-c304-44d3-adba-59b2163f0bcb; OptanonAlertBoxClosed=2023-07-20T09:19:02.074Z',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    def start_requests(self):
        url="https://www.trustpilot.com/review/barkbox.com"
        yield scrapy.Request(url,callback=self.get_reviews, headers=self.headers,cookies=self.cookies,meta={'page':0}, dont_filter=True)
    def get_reviews(self,response):
        html=response.text.split('<script type="application/ld+json" data-business-unit-json-ld="true">')[1].split('</script>')[0]
        reviews=json.loads(html)
        j=0
        for review in reviews['@graph']:
            if review['@type']=='Review':
                j+=1
                id=review['@id'].split('/')
                urldetail = "https://www.trustpilot.com/reviews/"+id[len(id)-1]
                yield scrapy.Request(urldetail,callback=self.get_reviewdetail, headers=self.headers,cookies=self.cookies, dont_filter=True)
        if j>=20:
            page=response.meta['page']+1
            url="https://www.trustpilot.com/review/barkbox.com?page="+str(page)
            yield scrapy.Request(url,callback=self.get_reviews, headers=self.headers,cookies=self.cookies,meta={'page':page}, dont_filter=True)
    def get_reviewdetail(self,response):
        url=response.url
        html=response.text.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0]
        review=json.loads(html)
        item=review['props']['pageProps']['review']
        name=item['consumer']['displayName']
        stars=item['rating']
        dateposted=item['dates']['publishedDate'].split('T')[0]
        dateex=item['dates']['experiencedDate']
        if dateex is None:
            dateex=dateposted
        else:
            dateex=dateex.split('T')[0]
        title=item['title']
        desc=item['text']
        useful=item['likes']
        with open('trustpilot.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, stars, dateposted, title, desc, dateex, useful, url])