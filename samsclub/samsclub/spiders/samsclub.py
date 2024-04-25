import scrapy
import json
from datetime import datetime
from random import randint


class Samsclub_Spider(scrapy.Spider):
    name = "samsclub"
    start_url = "https://www.samsclub.com/c"
    base_url = "https://www.samsclub.com"
    custom_settings = {
        # 'CLOSESPIDER_ITEMCOUNT': 500,
        'ROTATING_PROXY_LIST_PATH': 'proxies.txt',
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 200,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'CONCURRENT_REQUESTS_PER_IP':1,
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        },
        'DOWNLOAD_DELAY': 1,
        # 'LOG_FILE': f'./{name}_logs/{name}_{current_date}.log'
    }
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042",
        "Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    ]

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": user_agents[randint(0, len(user_agents) - 1)],
    }

    product_api = "https://www.samsclub.com/api/node/vivaldi/browse/v2/products/search?sourceType=1&limit=45&clubId=6609&offset={off_set}&searchCategoryId={cat_id}&br=true&secondaryResults=2&wmsponsored=1&wmsba=true"

    def get_cat(self,url):
        id = url.split('?')[0].split('/')[-1]
        return id
    def start_requests(self):
        yield scrapy.Request(
            self.start_url, 
            headers=self.headers, 
            callback=self.departments,
            # cookies=self.cookies
        )

    def departments(self, response):
        links = response.xpath(
            '//ul[@class="sc-category-more-categories-nav analytics"]/li/a[@class="bst-link bst-link-small bst-link-primary"]/@href'
        ).extract()
        cat_names = response.xpath(
            '//ul[@class="sc-category-more-categories-nav analytics"]/li/a[@class="bst-link bst-link-small bst-link-primary"]/text()'
        ).extract()

        for itr,link in enumerate(links):
            new_link = self.base_url + link
            if "/c/" in new_link:
                yield scrapy.Request(
                    new_link, 
                    headers=self.headers, 
                    callback=self.departments_sub,
                    # cookies=self.cookies,
                    meta={"product_cat":cat_names[itr],"url":new_link}
                )
            elif "/b/" in new_link:
                cat_id = self.get_cat(new_link)
                offset = 0

                yield scrapy.Request(
                    self.product_api.format(off_set=str(offset), cat_id=cat_id),
                    headers=self.headers,
                    callback=self.listing,
                    # cookies=self.cookies,
                    meta={"offset": offset, "cat_id": cat_id,"product_cat":cat_names[itr],"url":self.product_api.format(off_set=str(offset), cat_id=cat_id)},
                )

            # break

    def departments_sub(self, response):
        product_cat = response.meta.get("product_cat")
        url = response.meta.get('url')
        if 'https://www.samsclub.com/are-you-human?' in response.url:
            print(f'Blocked Trying again',url)
            # open('file.txt','a',encoding='UTF-8').write(f"{response.meta.get('url')}\n")
            yield scrapy.Request(
                    url, 
                    headers=self.headers, 
                    callback=self.departments_sub,
                    # cookies=self.cookies,
                    dont_filter=True,
                    meta={"product_cat":product_cat,"url":url}
                )
            return

        sub_depart = response.xpath(
            '//ul[@class="sc-category-more-categories-nav analytics"]/li/a[@class="bst-link bst-link-small bst-link-primary"]/@href'
        ).extract()
        if len(sub_depart) == 0:
            sub_depart = response.xpath(
                '//a[@class="bst-link bst-link-small bst-link-primary sc-featured-category-carousel-card"]/@href'
            ).extract()
        for itr, sub in enumerate(sub_depart):
            new_link = self.base_url + sub

            if "/c/" in new_link:
                yield scrapy.Request(
                    new_link, 
                    headers=self.headers, 
                    callback=self.departments_sub,
                    # cookies=self.cookies,
                    meta={"product_cat":product_cat,"url":new_link}
                )
            elif "/b/" in new_link:
                cat_id = self.get_cat(new_link)
                offset = 0

                yield scrapy.Request(
                    self.product_api.format(off_set=str(offset), cat_id=cat_id),
                    headers=self.headers,
                    callback=self.listing,
                    # cookies=self.cookies, 
                    meta={"offset": offset, "cat_id": cat_id,"product_cat":product_cat,"url":self.product_api.format(off_set=str(offset), cat_id=cat_id)},
                )

            # if itr == 10:
            #     break
            # break
    def listing(self, response):
        offset = response.meta.get("offset")
        cat_id = response.meta.get("cat_id")
        product_cat = response.meta.get("product_cat")
        url = response.meta.get('url')
        if 'https://www.samsclub.com/are-you-human?' in response.url:
            print(f'Blocked Trying again',url)
            # open('file.txt','a',encoding='UTF-8').write(f"{response.meta.get('url')}\n")
            yield scrapy.Request(
                url,
                headers=self.headers,
                callback=self.listing,
                dont_filter=True,
                # cookies=self.cookies,
                meta={"offset": offset, "cat_id": cat_id,"product_cat":product_cat,"url":url},
            )
            return
        data = json.loads(response.text)

        for product in data["payload"]["records"]:
            title = product["descriptors"].get("name", "NA")
            brand = product["manufacturingInfo"].get("brand", "NA")
            product_url = product["searchAndSeo"].get("url")
            if product_url:
                product_url = self.base_url + product_url
            try:

                price = product["skus"][0]["clubOffer"]["price"]["finalPrice"]["amount"]
            except:
                try:
                    price = product["skus"][0]["onlineOffer"]["price"]["finalPrice"]["amount"]
                except:
                    price = "NA"



            yield {
                "Store Name": self.name,
                "Product Category": product_cat,
                "Proudct SubCategory": "",
                "Product URL": product_url,
                "Product Title": title,
                "Product Brand": brand,
                "Product Price": price,
            }
            print('Success...')

        if len(data["payload"]["records"]) == 45:
            print("Next Page")
            yield scrapy.Request(
                self.product_api.format(off_set=str(offset + 45), cat_id=cat_id),
                headers=self.headers,
                callback=self.listing,
                # cookies=self.cookies,
                meta={"offset": offset + 45, "cat_id": cat_id,"product_cat":product_cat,"url":self.product_api.format(off_set=str(offset + 45), cat_id=cat_id)},
            )


