from scrapy import Request, Spider
import json
from datetime import datetime
from w3lib.http import basic_auth_header
import pandas as pd
class Idealo(Spider):
    name = "amazon_products"
    download_delay = 1.5
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",

    }
    
    cookies = {
        'session-id': '133-2009823-3355860',
        'ubid-main': '131-5723522-3774750',
        'x-main': '"gwogDufbs8S01h8vw8h0HCmxTVd@7uTcCRevzTXescLoVos30p@rfavoxi4Z3PfJ"',
        'at-main': 'Atza|IwEBIHT0nygbSYr9CYDBgCm67AIGhAdBoLrjxMr3spsEVpG-s_AqoY5GJE25ER9bwUBxqplTMqdiGvoiL00jA3RIpya1ioI5KHZGPmGV4JjDy_U8-R30PLPcLJ0qyS9qKKyzna5ZaSdSd-gUf2v3fqBw5NiZbFhsYJoEzUMRWqvjQoL5QBFkYwoSb-_U-AwHdrFDwD2DjzVWZFwkYPRsJAMjtsllWyquovttz5VYrEVflwLzzgHux7xPFKBSdptafhdhJSE',
        'sess-at-main': '"NN2sm1kxs/E5uZwdnxFlLMQ/g4dT8mLaMAAbdER1p6Y="',
        'sst-main': 'Sst1|PQHYKQ_yLqBaN00EfKNmDMZ1CWOL7eyDFrOTKREcy_QhK2IMokjpPXIyfiZBmeDpx0yEVu_mNsfdwAMkD3gnt9elDPzwHHZ4_iYZNZfEawvhYD4Km6esoiEyk-I-l-vSkHOnHwWLAdnTROBNiO89QCs1j57aLQu3UJSr9ohzwqKWZtWV7BmO8-adWZYpCdaUIiKoD_nbMusrWonGyvzz6L3qyky9TcU11cG8sYyFwPRB57DvOuvhTL_HMeNIWyEAijXfxIx45KUX0C3pYiK_hfnlxE3eVF-0qqoQp-w_iU7aPes',
        'lc-main': 'en_US',
        'session-id-time': '2082787201l',
        'i18n-prefs': 'USD',
        's_nr': '1684165533275-New',
        's_vnum': '2116165533275%26vn%3D1',
        's_dslv': '1684165533278',
        'skin': 'noskin',
        'sp-cdn': '"L5Z9:PK"',
        'x-amz-captcha-1': '1689870557908506',
        'x-amz-captcha-2': '929KERz7xitzAmuf9CBiEQ==',
        'session-token': '"v8Lh9sRVhsCSsRtTdAicMXM4+IoMA775/80ON1ej7Xz5HZ+7qjNsESuSe9+d/nw2sfzlzOOGOFUxzhpKCN1B+WldaN66erqHEFRXoSFZt7L00FVnw3IqOrUiR6sZGgW6F73YzJCeEkiEJAFgzcjUcp4q8z1u/up4NIa7shUnVLNEzBWKVLQ2DeQ8HdU/EC1HJ0EYyvxhD04kBynjBh+d+gvLAYWCQojj8AJxf+1zvSV5U0xYzDY2f7PHJvRqJERfbYTK8ldPhO4="',
        'csm-hit': 'tb:s-HV0WD7YA9E54SAJN7EZG|1689866502816&t:1689866503485&adb:adblk_yes',
    }

    base_url = 'https://www.amazon.com'
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.run_date = datetime.now().strftime("%d/%m/%Y")
    def check_availablity(self,asins,url):
        for asin in asins:
            if asin in url:
                return False
        return True
    def start_requests(self):
        try:
            df = pd.read_csv('./datafolder/amazon_dataset.csv')
            asins = df["ASIN"].to_list()
        except:
            asins = []
        df2 = pd.read_csv('./datafolder/amazon_urls.csv')
        urls = df2["productUrl"].to_list()
        product_url = 'https://www.amazon.com/dp/'
        counter = 0
        for url in urls:
            if self.check_availablity(asins,url):
                print(url)
                counter+=1
                yield Request(
                    url=url,
                    headers=self.headers,
                    callback=self.information,
                    cookies=self.cookies
                    )
        print(counter)


    def information(self, response):
        if response.status == 200:
            meta = response.meta
            name = response.xpath('//span[@id="productTitle"]/text()').get()
            product_id = response.url.split("/dp/")[-1].split("/")[0]
            
            brand_amazon = response.xpath('//a[@id="bylineInfo"]/text()').get()
            if brand_amazon:
                brand_amazon = brand_amazon.replace('Visit the','').strip()
            
            
            if name:
                name = name.strip()
            
            items = {}
            items["ASIN"] = product_id
            items["StoreName"] = brand_amazon
            items['ProductName'] = name
            yield items            
