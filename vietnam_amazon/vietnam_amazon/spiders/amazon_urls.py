from scrapy import Request, Spider
import json
from datetime import datetime
from w3lib.http import basic_auth_header

class Idealo(Spider):
    #handle_httpstatus_list = [503]
    name = "amazon_url"
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
        'session-id': '130-8754148-8947840',
        'ubid-main': '130-5271127-1291108',
        'x-main': '"DngEkg7v463bEzUHikeDp4oea6E6IbTEOX3a?8jhJk7skID@y5eHbWuFfP5uPYqM"',
        'at-main': 'Atza|IwEBIKeahUA9c9Q_RYIryAxZfSGlvY0TVJyWN03un4lm9X_cTtdw-aZ2FyZ1um_RZgXceJjbv1OjXzU5oi-vz2UUd0p3d7ZGWxuTls5AD6a0gcssQ0b-O_im8YOIO8Sf8CJ-UqNmjnhmRCgOXxy1pJCviEhPespX5FPMwMlUz5Xxe7RrP9F4NZNj0lL4NXUncw1glTbg5ywg6B8XBwAOPoGdGE_xfdNAaLl2BBnD4bCYi8ufh-cw2-6JHM8s91uek6-cxEY',
        'sess-at-main': '"N53CWSP2th6srI1tHwFCoIuJ8wPBXSfSww8pV8/MEww="',
        'sst-main': 'Sst1|PQF2tAMbmkhF2IGOUYVT3grqCbH5wdiftmfsLRzop5k8vhxZu1-_M2NuwB1oBqEC84wwkeob4zUkC9QY79XR7zabAwIYBzKt8CnsmaD1_Lh2fsBpZqG_wN3RsHPIklX-qP8nwnJcoSvqQJND6rFlFabhKYlFWpLiXn3PerAeN1nLciDGJCBJNd9RYqJeeQiZ2WdVC8sIv9yILyT3yaF3NOSF72uyl4mzVJ6RWNgXPg0fyd6avZvmZQxchA-aML7P2884rHUMiJdtqaW_R3pXx5p9HH-AvzW7T7pTDOnYcKo_Wnk',
        'lc-main': 'en_US',
        'x-amz-captcha-1': '1689294476003380',
        'x-amz-captcha-2': 'N69JrJNY+zteiiALO4T0Sw==',
        'session-id-time': '2082787201l',
        'i18n-prefs': 'USD',
        'session-token': '"5Gw7K3JzY13Rxb19bQy+7kEOwaYYch0xvRAjdoh0rsWlob3lLAMERJJlkOtdS94axS0GzWbDV2Gy6q2baxyKMXOBep2Aoj7VT0Hww3h7FYpGUvCcyV/Ha153Th31Ztm6Dgtg99aRoK+GySutcbGm92czv8SdiKcqmktFw4MDoezOmlBBDHGRBPgMBpkAXoOf3Pzx59dpMq5MHOHg9pAQBrBCxRn7jR+A2udt2Q2Yf0FF9Iv9kiQJCxbA3R+bgRKu3DzPj2vglSs="',
        'csm-hit': 'tb:s-YEA7KRJJ5TDX8PZZ52D8|1689802344282&t:1689802344976&adb:adblk_yes',
    }
    base_url = 'https://www.amazon.com'
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.run_date = datetime.now().strftime("%d/%m/%Y")

    def start_requests(self):

        url = f"https://www.amazon.com/s?i=hpc&rh=n%3A3764441%2Cp_72%3A1248903011&content-id=amzn1.sym.16e37646-73e5-411d-be1c-663080c0b9df&pd_rd_r=3fd3b09b-2acc-4d3c-a6b6-0a04ae7062ba&pd_rd_w=6R09N&pd_rd_wg=argBG&pf_rd_p=16e37646-73e5-411d-be1c-663080c0b9df&pf_rd_r=ZN22NZN5YRV1BR6JKE2Y&qid=1689802888&ref=sr_pg_1"
        yield Request(
                url=url,
                headers=self.headers,
                callback=self.main_page,
                cookies=self.cookies,
                )

    def main_page(self, response):
        
        print(response.url)
        
        next_page = response.xpath('//a[contains(@aria-label,"Go to next page")]/@href').get()
        if next_page:
            next_url = self.base_url+next_page
            yield Request(
                url = next_url,
                headers=self.headers,
                callback=self.main_page,
                cookies=self.cookies
            )
        else:
            print(f'No next page found. Current Url {response.url}')
        products = response.xpath(
            '//a[@class="a-link-normal s-no-outline"]/@href'
        ).extract()
        base_url = self.base_url
        products = [ base_url+'/' + url.split('&url=%2F')[-1].split('%2Fref')[0].replace('%2F','/').strip(':443').strip('/') for url in products]
        for product in products:
            headers = self.headers
            headers['referer'] = response.url
            yield {
                "productUrl":product
            }

        
            
