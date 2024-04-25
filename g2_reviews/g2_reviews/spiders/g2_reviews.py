import scrapy
import json
from datetime import datetime
from random import randint
class g2_Spider(scrapy.Spider):
    name = "g2"
    # download_delay = 1.5
    start_url = "https://www.g2.com/products/quickbooks-online-advanced/reviews?page={page}&_pjax=%23pjax-container"
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48',
            'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'user-agent': user_agents[randint(0,len(user_agents)-1)],
        }
    rating_checker = {
        "1":"0.5",
        "2":"1",
        "3":"1.5",
        "4":"2",
        "5":"2.5",
        "6":"3",
        "7":"3.5",
        "8":"4",
        "9":"4.5",
        "10":"5"
    }
    # define custom settings
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'PROXY_URL': 'http://7CE49GAVBXP63RRMTQ10R7Z725VJ53UC9PXCMY1XKSDFR4KY5LLVXOACPVCWXIFHKLXHJQB1XJKA336F:stealth_proxy=true&country_code=us@proxy.scrapingbee.com:8886',
        'PROXY_OPTIONS': {
            'max_retry_times': 3,
            'retry_http_codes': [500, 502, 503, 504, 400, 403, 404, 408],
            'backoff_factor': 1.5,
        },
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1
        # other settings as needed
        # ...
    }

    def start_requests(self):
        page = 1
        proxy_url = self.settings.get('PROXY_URL')
        proxy_options = self.settings.get('PROXY_OPTIONS')
        done = []
        for itr in range(1,13):
            if itr in done:
                print(f"page: {itr}, already extracted")
                continue
            yield scrapy.Request(
                self.start_url.format(page=itr),
                callback=self.information,
                headers=self.headers,
                meta={
                    'proxy': proxy_url,
                    'proxy_options': proxy_options
                }
            )

    def information(self,response):

        reviews = response.xpath('//div[@itemprop="review"]')
        counter = 0
        for review in reviews:

            name = review.xpath('.//span[@itemprop="author"]//a/text()').get(default='NA')
            role = review.xpath('.//div[@class="c-midnight-80 line-height-h6 fw-regular"]/div/text()').get(default='NA')
            business_size = " ".join(review.xpath('.//div[@class="c-midnight-80 line-height-h6 fw-regular"]/div//span/text()').extract())
            validated = review.xpath('.//div[text()="Validated Reviewer"]').get()
            if validated:
                validated = "Yes"
            else:
                validated = "No"

            source = review.xpath('.//div[contains(text(),"Review source:")]/text()').get()
            if source is not None:
                source = source.replace('Review source:','').strip()
            else:
                source = 'NA'
            rating = review.xpath('.//div[contains(@class,"stars")]/@class').get(default='NA')
            if rating!="NA":
                rating = rating.split()[-1].replace('stars-','')
                rating = self.rating_checker.get(rating,"0")

            date = review.xpath('.//time/text()').get(default='NA')
            title = review.xpath('.//h3/text()').get(default='NA')
            like_best = " ".join(review.xpath('.//div[@itemprop="reviewBody"]//h5[text()="What do you like best about QuickBooks Online Advanced?"]/../div/p/text()').extract())
            dislike = " ".join(review.xpath('.//div[@itemprop="reviewBody"]//h5[text()="What do you dislike about QuickBooks Online Advanced?"]/../div/p/text()').extract())
            benefit = " ".join(review.xpath('.//div[@itemprop="reviewBody"]//h5[text()="What problems is QuickBooks Online Advanced solving and how is that benefiting you?"]/../div/p/text()').extract())
            item = {}
            item["Name"] = name
            item["Role"] = role
            item["Business Size"] = business_size
            item["Validated?"] = validated
            item["Source"] = source
            item["Rating"] = rating
            item["Date"] = date
            item["Title"] = title
            item["What do you like best?"] = like_best
            item["What do you dislike?"] = dislike
            item["What problems are solved and how does it benefit you?"] = benefit
            yield item
            input(item)
            counter +=1


        print(f"{response.status}, {response.url}, {counter}")
