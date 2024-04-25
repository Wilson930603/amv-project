from scrapy import Spider, Request
from ..items import BanksItem
class Banks(Spider):
    name= 'banks'
    handle_httpstatus_list = [400,404,403,402,401]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "referer": "https://www.weddingwire.com/wedding-venues",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    def __init__(self, name=None, **kwargs):
        self.sites = [r.strip() for r in open('./links copy.txt','r').readlines()]
        super().__init__(name, **kwargs)
    def refine_url(self, url):
        url = url.strip('. /')
        if url.startswith('www'):
            url = 'https://'+url
        return url
    def catch_err(self, err):
        url = err.request.url
        items = BanksItem()
        items['websites'] = url
        items['Status'] = 404
        yield items
        # input(f'{status} - {url}')
    def start_requests(self):
        for site in self.sites:

            yield Request(
                url = self.refine_url(site),
                callback=self.main_page,
                headers = self.headers,
                dont_filter=True,
                errback=self.catch_err,
                meta={'download_timeout': 30, 'retry_times': 1,'url':site},
            )
            # break
    def main_page(self,response):
        meta = response.meta
        code = response.status
        if code == 200:
            status = response.url
        else:
            status = code
        items = BanksItem()
        url = meta.get('url')
        items["websites"] = url
        items['Status'] = status        
        yield items