from scrapy import Request, Selector, Spider

import pandas as pd
import json
from datetime import datetime
import os

try:
    from ..items import AmazonreviewsItem, AmazonUrls
except:
    from items import AmazonreviewsItem, AmazonUrls
from random import randint
import math
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import urllib.parse


class Spider_Amazon_links(Spider):
    name = "amazon_links"
    base_urlUS = "https://www.amazon.com"
    base_urlUK = "https://www.amazon.co.uk"
    handle_httpstatus_list = [404,302, 503, 403]
    download_delay = 0.3
    error = 0
    cookies = {
    'session-id': '133-2009823-3355860',
    'ubid-main': '131-5723522-3774750',
    'session-token': 'elIBw3dvhT7oriSfoKCPjtWVlu+NCLFGcidlVYllli3wyUJfibVZMmM4CrofbW9uKYtgfvd5s+Od97YUuP5n7dkpfcQsNbBabT2wd2t0TfWZTKLQsxbIMCpGLHdmLWegj6s2D2vRb/2/x4Ujs3M+bz5da4haETSkwZznxnTjyRfgaQar46tMyDBGnFW8z54qrX+PjyGOMH8/Z3SqDwi7LUSiMV3QfIpODviJbmXfhP/zOfvZLsapBG1jGny9dWLT',
    'x-main': '"gwogDufbs8S01h8vw8h0HCmxTVd@7uTcCRevzTXescLoVos30p@rfavoxi4Z3PfJ"',
    'at-main': 'Atza|IwEBIHT0nygbSYr9CYDBgCm67AIGhAdBoLrjxMr3spsEVpG-s_AqoY5GJE25ER9bwUBxqplTMqdiGvoiL00jA3RIpya1ioI5KHZGPmGV4JjDy_U8-R30PLPcLJ0qyS9qKKyzna5ZaSdSd-gUf2v3fqBw5NiZbFhsYJoEzUMRWqvjQoL5QBFkYwoSb-_U-AwHdrFDwD2DjzVWZFwkYPRsJAMjtsllWyquovttz5VYrEVflwLzzgHux7xPFKBSdptafhdhJSE',
    'sess-at-main': '"NN2sm1kxs/E5uZwdnxFlLMQ/g4dT8mLaMAAbdER1p6Y="',
    'sst-main': 'Sst1|PQHYKQ_yLqBaN00EfKNmDMZ1CWOL7eyDFrOTKREcy_QhK2IMokjpPXIyfiZBmeDpx0yEVu_mNsfdwAMkD3gnt9elDPzwHHZ4_iYZNZfEawvhYD4Km6esoiEyk-I-l-vSkHOnHwWLAdnTROBNiO89QCs1j57aLQu3UJSr9ohzwqKWZtWV7BmO8-adWZYpCdaUIiKoD_nbMusrWonGyvzz6L3qyky9TcU11cG8sYyFwPRB57DvOuvhTL_HMeNIWyEAijXfxIx45KUX0C3pYiK_hfnlxE3eVF-0qqoQp-w_iU7aPes',
    'lc-main': 'en_US',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'sp-cdn': '"L5Z9:PK"',
    'csm-hit': 'tb:E2Z65EE4ADD1CSHS7C46+s-87B9EDKVKH45JGFVTREV|1679555700127&t:1679555700127&adb:adblk_yes',
}
    headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'cookie': 'ubid-main=130-0250546-4554055; session-id-apay=260-7865894-8878705; session-id=143-4396210-7946434; skin=noskin; lc-main=en_US; x-main="z7wKa9bcxygj49QeSekKA@dHticYbh7oH0v8jQ04cbpRNpqFDlQ7Sf@LEIQ4mCt7"; at-main=Atza|IwEBIBxHjQlUPixbuKcRiiaHZM2Fg_Yx0l9zOY2IkQJge1mUGUdOuod-eA1rbRTtJ1Kcfkkba_55qZki8P9TlFoQyna3d0SQtO2MAaD1cvdK1FOPW5gDR8koIUZmZe8_JZMvpQ8dKf-rCInMeTuYk7njx5KlIALi2eT5uLrxzy8E2wnOr3a9dM19QzIIptYhtyW3YM09nEAdH3M8INs1SscUrgLm; sess-at-main="JYwb14q+dUZl3qoHnvtKunQfz/0ri11qGv4a/3aKIBY="; sst-main=Sst1|PQGFh2WvsLbo4USvq8uSg8sACfXYyPAuHM_-GgV_R0i4ZlI7FU-GYT5fOlRG2pHFTk2-oSHf1uQyu20_-07lACPCnDRE4vuw9o666RnUkYcYjmSBFYVOEffxvYPbI6wOIUf1Ez0twK70EDbZ2g4VTEXLaWa2Qnm8xLDNBiSG7-VaTGVmGZ_1oer9EkqxN9K8h7kq2yp0eFti35t8QdWlBqiTXHP1CQpq7muo3IVyCo1PAt5jTRRfUnIDvNLUvSXGkj6mtY1RzTk9bwrrIRskc6AIBZV38vp7xZDMPcDpEbKSlBQ; session-id-time=2082787201l; i18n-prefs=USD; csm-hit=tb:R9ANR3TFZVH1XPNT3GPM+b-XTHTVQWQJPQ9JR8PSEN7|1679347835735&t:1679347835735&adb:adblk_yes; session-token=wyNmYDwjqLDlwROhT7iOWn7EPIkBX36huIoVA3vCpgr2L2WVSDuJFgiIrPmRPIh5IkOL3XF9cC9KeVz6axUIefu2TWYZU3/rZouZh79niyqxllH1BbfuvqhC4wFcTgIXfGLZjekeWVWTQFVKje70ShjH476dXKww+nZd1kk2RxuMW74HilE7agGZ2bNFNEEWbM3juiItzZ3Lkbn6294DXyqXuFy96Nf89nPG715mUmHD/C0B0WiStQ==',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1',
    'ect': '4g',
    'origin': 'https://www.amazon.com',
    #'referer': 'https://www.amazon.com/Myprotein-Impact-Protein-Chocolate-Servings/product-reviews/B00CHJ470G/ref=cm_cr_arp_d_paging_btm_next_4?ie=UTF8&reviewerType=all_reviews&pageNumber=4&returnFromLogin=1',
    'rtt': '250',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-viewport-width': '1837',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'viewport-width': '1837',
    'x-requested-with': 'XMLHttpRequest',
    }
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48",
        "Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    ]

    headers_reviews = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US;q=0.9,en;q=0.8",
        "referer": "https://www.amazon.com/Liquid-I-V-Multiplier-Electrolyte-Supplement/dp/B01IT9NLHW/ref=sr_1_1?keywords=liquid%2Biv&qid=1676553036&sr=8-1&th=1",
        "sec-ch-dpr": "1.25",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "sec-ch-viewport-width": "1229",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "viewport-width": "1229",
        "cookie": 'ubid-main=130-0250546-4554055; sp-cdn="L5Z9:PK"; lc-main=en_US; session-id-apay=260-7865894-8878705; session-id=143-4396210-7946434; skin=noskin; session-token=+E+/H+2bPG1mzVqEzJ+Kk4uABMpUUuTTffCd/7JjBdtTGRsaDHUMIIBn/7qg1NnE/bmsaOOqVN3EI5tJ/qUGxoH0xzdtFIxMpRC7KdLHhc3HqYFXq0jCfPyjn/4KzT+2kHozfs69SNWM2SNgtwBmAbEXQCk0NTNNBpLrYR+HLiEx/o/iFF3JmqMC1tJLgdMbovK0qzHo1dQOBJ67NFT8CXNl5ZPMckgSkPhtKYbVdjvFatmUlJ1Dh8nz+yYKKP87; x-main=1wrMbUU3EdJq7lXz7KxwVCGCvhUpeJlFEp8AZwAH5PipbtsDBbWcPWxxx1e40eFb; at-main=Atza|IwEBIADf8nALV2LHyNpKihID1XdPl_NodZRpKM9cCdhuJqc-IODvmNXdGMFOt506UbwtDQPsNfzutD8y8zL79qkvduMfjad_WbqI5IacS3pM2ucSEHVmBUvFLN9WY9NnlE8PsUM7OzfUN3uLE1tbCQewZeYNsRoW-wGKzofRsjTyu2xNrlJS2tz6DYZC3QWjojd8_hx7Vw_AiKLqSJSItsv3MDBeWnBER4-M4wIzab6mlpGYJf7Y-ZQ6hSB4RukLef42L_k; sess-at-main="2i+z38+hTFow19D4PPvJWFOEfUrH1nTXTTbzqcZPjNU="; sst-main=Sst1|PQH_JU3mTK7xoJLdp-c3UUwaCQrD_Q9gtZe9QLFHWLtlNG9z9_KlaPsxjTFFcEdXS5LfeJ3F_h--zzx7W_3l6kjDdnVnTI3YAgSNMwfDxv5nExOAx0vXaHAQc7SpM2Qv2Ga-lpBeYtjT1lGuqAHdcdwn9e74cEQnopgqiw4tQcPi9PWhSNdEJlrBbWOY0d7_cIVPpexUVnBrJz2ij4viZRw_cbk2pwLO8BVRr-AuiLj3tipgKfSQPAKky72EWNNWcm0Zn8GH1M-_TuNUZL7MCtT3F0ZsWiVNI1UPmPsH-R4QCKE; session-id-time=2082787201l; i18n-prefs=USD; csm-hit=tb:s-FP9QFRQH8X1YXDMB948S|1679237234269&t:1679237234612&adb:adblk_yes',
    }
    headers_product = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US;q=0.9,en;q=0.8",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "sec-ch-viewport-width": "1229",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "viewport-width": "1229",
    }

    def rotate_headers(self, ref="", headers=None):
        user_agents = self.user_agents
        if headers is None:
            headers = self.headers

        headers["user-agent"] = user_agents[randint(0, len(user_agents) - 1)]
        if ref != "":
            headers["referer"] = ref
        return headers

    def rotateProxy(self, path="./proxy/proxy.txt"):
        f = open(path, "r")
        proxy = ["http://" + proxy.strip() for proxy in f.readlines()]
        f.close()
        visited_proxy = []
        count = 0
        while True:
            prox = proxy[randint(0, len(proxy) - 1)]
            if prox not in self.dead_proxy:
                yield prox

    def closed(self, reason):
        if len(self.data["Title"]) > 0:
            if not os.path.exists(self.failed_csv):
                pd.DataFrame(self.data).to_csv(self.failed_csv, index=False)
            else:
                pd.DataFrame(self.data).to_csv(
                    self.failed_csv, index=False, header=False, mode="a"
                )
        if len(self.failed_productLinks["url"]) > 0:
            if not os.path.exists(self.failed_products):
                pd.DataFrame(self.failed_productLinks).to_csv(
                    self.failed_products, index=False
                )
            else:
                pd.DataFrame(self.failed_productLinks).to_csv(
                    self.failed_products, index=False, header=False, mode="a"
                )

        f = open("dead_blocked_proxy.txt", "w")
        f.write("\n".join(self.dead_proxy))
        f.close()

    def __init__(self):
        self.failed_csv = "failed.csv"
        self.failed_products = "failed_products.csv"
        self.failed_productLinks = {
            "url": [],
            "brand": [],
        }
        self.data = {
            "Title": [],
            "Category": [],
            "Is_Discontinued_By_Manufacturer": [],
            "Product_Dimensions": [],
            "Item_model_number": [],
            "UPC": [],
            "Manufacturer": [],
            "ASIN": [],
            "Brand": [],
            "links": [],
        }
        fd = None
        try:
            fd = pd.read_csv(self.failed_products)
            self.brands = [fd.iloc[i]["brand"] for i in range(len(fd))]
            self.links = [fd.iloc[i]["url"] for i in range(len(fd))]
            os.remove(self.failed_products)
        except:
            fd = None
            df = pd.read_csv("./datafolder/data.csv")
            self.brands = [df.iloc[i]["brand"] for i in range(len(df))]
            self.links = [df.iloc[i]["url"] for i in range(len(df))]
        try:
            f = open("dead_blocked_proxy.txt", "r")
            self.dead_proxy = [proxy.strip() for proxy in f.readlines()]
        except:
            self.dead_proxy = []
        try:
            if fd is None:
                failed_df = pd.read_csv(self.failed_csv)
                failed_df.fillna("N/A", inplace=True)
                self.failed_links = [
                    failed_df.iloc[i]["links"] for i in range(len(failed_df))
                ]
                self.title = [failed_df.iloc[i]["Title"] for i in range(len(failed_df))]
                self.product_dimention = [
                    failed_df.iloc[i]["Category"] for i in range(len(failed_df))
                ]
                self.category = [
                    failed_df.iloc[i]["Is_Discontinued_By_Manufacturer"]
                    for i in range(len(failed_df))
                ]
                self.is_discontinue = [
                    failed_df.iloc[i]["Product_Dimensions"]
                    for i in range(len(failed_df))
                ]
                self.item_model = [
                    failed_df.iloc[i]["Item_model_number"]
                    for i in range(len(failed_df))
                ]
                self.upc = [failed_df.iloc[i]["UPC"] for i in range(len(failed_df))]
                self.maufacturer = [
                    failed_df.iloc[i]["Manufacturer"] for i in range(len(failed_df))
                ]
                self.asin = [failed_df.iloc[i]["ASIN"] for i in range(len(failed_df))]
                self.brand = [failed_df.iloc[i]["Brand"] for i in range(len(failed_df))]

                os.remove(self.failed_csv)
            else:
                self.failed_links = None

        except:
            self.failed_links = None
        self.rotate_proxy = self.rotateProxy()

    def start_requests(self):
        if self.failed_links:
            ## Resume Logic
            # input('Failed Process')
            for count, url in enumerate(self.failed_links):
                items = AmazonreviewsItem()
                items["Title"] = self.title[count]
                items["Category"] = self.product_dimention[count]
                items["Is_Discontinued_By_Manufacturer"] = self.category[count]
                items["Product_Dimensions"] = self.is_discontinue[count]
                items["Item_model_number"] = self.item_model[count]
                items["UPC"] = self.upc[count]
                items["Manufacturer"] = self.maufacturer[count]
                items["ASIN"] = self.asin[count]
                items["Brand"] = self.brand[count]
                if "ap/signin?openid.pape" in url:
                    newUrl = urllib.parse.unquote(url.split("return_to=")[-1])
                else:  #
                    newUrl = url
                if 'ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews' in newUrl:
                    yield Request(
                            newUrl,
                            callback=self.parse_reviews,
                            headers=self.rotate_headers(),
                            cookies=self.cookies,
                            errback=self.errback,
                            meta={
                                "items": items,
                                "brand":self.brand[count],
                                # "proxy": next(self.rotate_proxy),
                                # "download_timeout": 20,
                                # "max_retry_times": 0,
                                "max_pages":0,
                            },
                        )
                else:    
                    yield Request(
                        newUrl,
                        callback=self.parse_reviews,
                        headers=self.rotate_headers(),
                        cookies=self.cookies,
                        errback=self.errback,
                        meta={
                            "items": items,
                            # "proxy": next(self.rotate_proxy),
                            # "download_timeout": 20,
                            # "max_retry_times": 0,
                        },
                    )
        else:
            for count, url in enumerate(self.links):
                if "https://www.amazon.com/gp/slredirect/picassoRedirect.html" == url:
                    continue
                if "ap/signin?openid.pape" in url:
                    newUrl = urllib.parse.unquote(url.split("return_to=")[-1])
                else:  #
                    newUrl = url
                if "sspa/click?ie=" in url:
                    newUrl = urllib.parse.unquote(
                        url.split("&url=")[-1].split("ref")[0]
                    )
                    if self.base_urlUK in url:
                        newUrl = self.base_urlUK + newUrl
                    else:
                        newUrl = self.base_urlUS + newUrl
                yield Request(
                    newUrl,
                    callback=self.parse_product,
                    # dont_filter=True,
                    headers=self.rotate_headers(),
                    errback=self.errback,
                    meta={
                        "brand": self.brands[count],
                        # "proxy": next(self.rotate_proxy),
                        # "download_timeout": 20,
                        "max_retry_times": 0,
                    },
                )
                #break

    def check_none(self, data):
        """
        If the data is None or an empty string, return 'N/A', otherwise return the data

        :param data: The data to be checked
        :return: the data if it is not None or empty.
        """
        if data == None or data == "":
            return "N/A"
        return data

    def parse_product(self, response):
        if response.status in self.handle_httpstatus_list:
            self.error_product_saveToFile(response)
            return
        if response.css("#captchacharacters").extract_first():
            if response.meta.get("proxy"):
                self.dead_proxy.append(response.meta.get("proxy"))
            print("Captcha Found During Parse Products And App Try To Enable Proxy")
            if response.meta.get("try_again"):
                try_again = response.meta.get("try_again")+1
            else:
                try_again = 0
            if try_again == 2:
                self.error_product_saveToFile(response)
                print('MAX RETRY COUNT REACHED')
                return
            yield Request(
                response.url,
                callback=self.parse_product,
                dont_filter=True,
                errback=self.errback,
                headers=self.rotate_headers(
                    ref=response.url, headers=self.headers_product
                ),
                meta={
                    "brand": response.meta.get("brand"),
                    "category": response.meta.get("category"),
                    # "proxy": next(self.rotate_proxy),
                    # "download_timeout": 20,
                    # "max_retry_times": 0,
                    "try_again": try_again,
                },
            )

            return

        na = "N/A"
        brand = response.meta.get("brand")

        try:
            title = (
                response.xpath('//span[contains(@id,"productTitle")]/text()')
                .get()
                .strip()
            )
        except:
            title = na

        is_discontinued = response.xpath(
            '//span[contains(text(),"Is Discontinued By Manufacture")]/../span/text()'
        ).extract()
        if len(is_discontinued) == 2:
            is_discontinued = is_discontinued[-1]
        else:
            is_discontinued = na

        dimention = response.xpath(
            '//span[contains(text(),"Product Dimensions")]/../span/text() | //span[contains(text(),"Package Dimensions")]/../span/text()'
        ).extract()
        if len(dimention) == 2:
            dimention = dimention[-1]
        else:
            dimention = na

        modelNumber = (
            response.xpath(
                '//span[contains(text(),"Item model number")]/../span[2]/text() | //tr//th[contains(text(),"Item model number")]/following-sibling::td[1]/text()'
            )
            .get(default=na)
            .strip()
            .replace("‎", "")
        )

        upc = (
            response.xpath(
                '//span[contains(text(),"UPC")]/../span[2]/text() | //tr//th[contains(text(),"UPC")]/following-sibling::td[1]/text()'
            )
            .get(default=na)
            .strip()
            .replace("‎", "")
        )

        manufacturer = response.xpath(
            '//span[contains(text(),"Manufacturer")]/../span/text()'
        ).extract()
        if len(manufacturer) > 0:
            try:
                for itr, x in enumerate(manufacturer):
                    c = x.replace(" ", "").replace("\n", "").split(":")[0].strip()
                    if "Manufacturer" == c[:-1] or "Manufacturer" == c:
                        manufacturer = manufacturer[itr + 1]
                        break
                if type(manufacturer) == list:
                    manufacturer = na
            except:
                manufacturer = na
        else:
            manufacturer = na

        table = response.xpath(
            '//table[contains(@id,"productDetails_techSpec_section_1")]//tr'
        )
        for tr in table:
            if modelNumber == na:
                if tr.xpath(".//th/text()").get().strip() == "Item model number":
                    modelNumber = (
                        tr.xpath(".//td/text()").get().strip().replace("‎", "")
                    )
            if dimention == na:
                if (
                    tr.xpath(".//th/text()").get().strip() == "Package Dimensions"
                    or tr.xpath(".//th/text()").get().strip() == "Product Dimensions"
                ):
                    dimention = tr.xpath(".//td/text()").get().strip().replace("‎", "")
            if manufacturer == na or type(manufacturer) == list:
                if tr.xpath(".//th/text()").get().strip() == "Manufacturer":
                    manufacturer = (
                        tr.xpath(".//td/text()").get().strip().replace("‎", "")
                    )
            if upc == na:
                if (
                    tr.xpath(".//th/text()").get().strip() == "UPC"
                    or tr.xpath(".//th/text()").get().strip() == "upc"
                ):
                    upc = tr.xpath(".//td/text()").get().strip().replace("‎", "")

        asin = na
        if asin == na:
            asin = re.search(r"/[0-9A-Z]{10}", response.url).group(0)
            asin = asin[1:]

        category = "".join(
            [
                x.strip()
                for x in response.xpath(
                    '//div[contains(@id,"breadcrumbs_feature_div")]/ul/li//text()'
                ).extract()
                if x.strip() != ""
            ]
        )
        items = AmazonreviewsItem()

        items["Title"] = title

        items["Is_Discontinued_By_Manufacturer"] = is_discontinued
        items["Product_Dimensions"] = dimention
        items["Item_model_number"] = modelNumber
        items["UPC"] = upc
        items["Manufacturer"] = manufacturer
        items["ASIN"] = asin
        items["Brand"] = brand

        items["Category"] = self.check_none(category)

        reviewPage = response.xpath(
            '//a[contains(@data-hook,"see-all-reviews-link-foot")]/@href'
        ).get()

        if reviewPage:
            if self.base_urlUK in response.url:
                reviewUrl = self.base_urlUK + reviewPage
            else:
                reviewUrl = self.base_urlUS + reviewPage
            headers = self.rotate_headers(
                ref=response.url, headers=self.headers_reviews
            )

            yield Request(
                reviewUrl,
                callback=self.parse_reviews,
                headers=headers,
                errback=self.errback,
                meta={
                    "items": items,
                    "brand": brand,
                    # "proxy": next(self.rotate_proxy),
                    # "download_timeout": 20,
                    # "max_retry_times": 0,
                },
            )

    def parse_reviews(self, response):
        if response.status in self.handle_httpstatus_list:
            self.error_saveToFile(response)

            return
        if response.css("#captchacharacters").extract_first():
            if response.meta.get("proxy"):
                self.dead_proxy.append(response.meta.get("proxy"))
            print("Captcha Found During Parse Reviews And App Try To Enable Proxy")
            headers = self.headers_reviews
            headers["user-agent"] = self.user_agents[
                randint(0, len(self.user_agents) - 1)
            ]
            if response.meta.get("try_again"):
                try_again = response.meta.get("try_again")+1
            else:
                try_again = 0
            if try_again == 2:
                self.error_saveToFile(response)
                print('MAX RETRY COUNT REACHED')
                return
            yield Request(
                response.url,
                callback=self.parse_reviews,
                dont_filter=True,
                errback=self.errback,
                cookies=self.cookies,
                headers=self.rotate_headers(
                ref=response.url, headers=self.headers_reviews
                ),
                meta={
                    "items": response.meta.get("items"),
                    "max_pages": response.meta.get("max_pages"),
                    "brand": response.meta.get("brand"),
                    # "proxy": next(self.rotate_proxy),
                    # "download_timeout": 20,
                    # "max_retry_times": 0,
                    "try_again": try_again
                },
            )

            return

        na = "N/A"
        items = response.meta.get("items")
        brand = response.meta.get("brand")
        items["Brand"] = brand
        if brand is None:
            print("HERe")

        reviews = response.xpath(
            '//div[contains(@id,"cm_cr-review_list")]//div[contains(@id,"review-card")]'
        )

        for review in reviews:
            retailer_name = review.xpath(
                './/span[contains(@class,"a-profile-name")]/text()'
            ).get()
            review_star = review.xpath(
                './/i[contains(@data-hook,"review-star-rating")]/span/text()'
            ).get()
            if review_star:
                review_star = review_star.split("out")[0]
            reivew_title = review.xpath(
                './/a[contains(@data-hook,"review-title")]/span/text()'
            ).get()
            if reivew_title is None:
                reivew_title = review.xpath(
                    './/span[contains(@data-hook,"review-title")]/span/text()'
                ).get()
            verified = review.xpath(
                './/span[contains(@data-hook,"avp-badge")]/text()'
            ).get()
            if verified:
                verified = "Yes"
            else:
                verified = "No"
            try:
                review_text = "".join(
                    review.xpath(
                        './/span[contains(@data-hook,"review-body")]/span/text()'
                    ).extract()
                )
            except Exception as ex:
                review_text = na

            try:
                review_date = (
                    review.xpath('.//span[contains(@data-hook,"review-date")]/text()')
                    .get()
                    .split("on")[-1]
                    .strip()
                )
            except:
                review_date = na

            reivew_url = review.xpath(
                './/a[contains(@data-hook,"review-title")]/@href'
            ).get()
            if reivew_url:
                if self.base_urlUK in response.url:
                    reivew_url = self.base_urlUK + reivew_url
                else:
                    reivew_url = self.base_urlUS + reivew_url
            if self.base_urlUK in response.url:
                ret_name = self.base_urlUK
            else:
                ret_name = self.base_urlUS
            items["Retailer_Name"] = ret_name
            items["Review_Star"] = self.check_none(review_star)
            items["Is_Verified"] = self.check_none(verified)

            items["Has_Response"] = na  # Cant fid this one

            items["Review_Title"] = self.check_none(reivew_title)
            items["Review_Text"] = review_text
            items["Review_Date"] = review_date
            items["Review_URL"] = self.check_none(reivew_url)
            items["URL"] = response.url
            yield items
        temp = "/ref=cm_cr_arp_d_paging_btm_next_{pg1}?ie=UTF8&reviewerType=all_reviews&pageNumber={pg2}&returnFromLogin=1"
        headers = self.headers_reviews
        headers["user-agent"] = self.user_agents[randint(0, len(self.user_agents) - 1)]
        if not response.meta.get("max_pages"):
            page_count = math.ceil(
                int(
                    response.xpath(
                        '//div[@data-hook="cr-filter-info-review-rating-count"]/text()'
                    )
                    .get(default="NA")
                    .strip()
                    .split("ratings,")[-1]
                    .split()[0]
                    .replace(",", "")
                )
                / 10
            )
            if page_count > 500:
                page_count = 500
        else:
            return
        # input(page_count)
        for itr in range(2, page_count + 1):
            if "/product-reviews/" in response.url:
                reviewUrl = response.url.split("/ref")[0] + temp.format(
                    pg1=str(itr), pg2=str(itr)
                )
            print(reviewUrl)
            yield Request(
                reviewUrl,
                callback=self.parse_reviews,
                errback=self.errback,
                headers=self.rotate_headers(ref=response.url),
                cookies=self.cookies,
                meta={
                    "items": response.meta.get("items"),
                    "ref": response.url,
                    "brand": brand,
                    "max_pages": page_count,
                    # "proxy": next(self.rotate_proxy),
                    # "download_timeout": 20,
                    # "max_retry_times": 0,
                },
            )

    
    def errback(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)
            # input(f'Here is the HTTPERROR- {response.url}')
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)
            # input(f'Here is the DNS Lookup Error- {request.url}')

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)
            # input(f'Here is the Timeour error- {request.url} and meta->{request.meta}')
            self.dead_proxy.append(request.meta["proxy"])

            if "/dp/" in request.url:
                self.failed_productLinks["url"].append(request.url)
                self.failed_productLinks["brand"].append(request.meta.get("brand"))

            else:
                self.data["Title"].append(request.meta.get("items").get("Title"))
                self.data["Category"].append(request.meta.get("items").get("Category"))
                self.data["Is_Discontinued_By_Manufacturer"].append(
                    request.meta.get("items").get("Is_Discontinued_By_Manufacturer")
                )
                self.data["Product_Dimensions"].append(
                    request.meta.get("items").get("Product_Dimensions")
                )
                self.data["Item_model_number"].append(
                    request.meta.get("items").get("Item_model_number")
                )
                self.data["UPC"].append(request.meta.get("items").get("UPC"))
                self.data["Manufacturer"].append(
                    request.meta.get("items").get("Manufacturer")
                )
                self.data["ASIN"].append(request.meta.get("items").get("ASIN"))
                self.data["Brand"].append(request.meta.get("items").get("Brand"))
                self.data["links"].append(request.url)

    def error_product_saveToFile(self, request):
        self.failed_productLinks["url"].append(request.url)
        self.failed_productLinks["brand"].append(request.meta.get("brand"))

    def error_saveToFile(self, request):
        self.data["Title"].append(request.meta.get("items").get("Title"))
        self.data["Category"].append(request.meta.get("items").get("Category"))
        self.data["Is_Discontinued_By_Manufacturer"].append(
            request.meta.get("items").get("Is_Discontinued_By_Manufacturer")
        )
        self.data["Product_Dimensions"].append(
            request.meta.get("items").get("Product_Dimensions")
        )
        self.data["Item_model_number"].append(
            request.meta.get("items").get("Item_model_number")
        )
        self.data["UPC"].append(request.meta.get("items").get("UPC"))
        self.data["Manufacturer"].append(request.meta.get("items").get("Manufacturer"))
        self.data["ASIN"].append(request.meta.get("items").get("ASIN"))
        self.data["Brand"].append(request.meta.get("items").get("Brand"))
        self.data["links"].append(request.url)

