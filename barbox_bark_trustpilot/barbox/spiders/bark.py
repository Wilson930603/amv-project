import scrapy,json,csv,os, requests, urllib, shutil
class CrawlerSpider(scrapy.Spider):
    name = 'bark'
    cookies = {
        'secure_customer_sig': '',
        'localization': 'US',
        'cart_currency': 'USD',
        '_cmp_a': '%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22US%22%2C%22sale_of_data_region%22%3Afalse%7D',
        '_y': '391b749c-caf7-42f1-8133-62458d9df1bf',
        '_shopify_y': '391b749c-caf7-42f1-8133-62458d9df1bf',
        '_orig_referrer': 'https%3A%2F%2Fwww.barkbox.com%2F',
        '_landing_page': '%2F%3Futm_medium%3Drails-website%26utm_source%3Dbark_header%26utm_campaign%3D20220801_all-bark__eats_all_evergreen_control%26utm_term%3Deats',
        '_gcl_au': '1.1.1726273313.1689839870',
        '__kla_id': 'eyIkcmVmZXJyZXIiOnsidHMiOjE2ODk4Mzk4NzMsInZhbHVlIjoiaHR0cHM6Ly93d3cuYmFya2JveC5jb20vIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vZm9vZC5iYXJrLmNvLz91dG1fbWVkaXVtPXJhaWxzLXdlYnNpdGUmdXRtX3NvdXJjZT1iYXJrX2hlYWRlciZ1dG1fY2FtcGFpZ249MjAyMjA4MDFfYWxsLWJhcmtfX2VhdHNfYWxsX2V2ZXJncmVlbl9jb250cm9sJnV0bV90ZXJtPWVhdHMifSwiJGxhc3RfcmVmZXJyZXIiOnsidHMiOjE2ODk4Mzk5MjIsInZhbHVlIjoiaHR0cHM6Ly93d3cuYmFya2JveC5jb20vIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vZm9vZC5iYXJrLmNvLz91dG1fbWVkaXVtPXJhaWxzLXdlYnNpdGUmdXRtX3NvdXJjZT1iYXJrX2hlYWRlciZ1dG1fY2FtcGFpZ249MjAyMjA4MDFfYWxsLWJhcmtfX2VhdHNfYWxsX2V2ZXJncmVlbl9jb250cm9sJnV0bV90ZXJtPWVhdHMifX0=',
        '_ga_NKW49FBKXG': 'GS1.1.1689839873.1.1.1689839925.0.0.0',
        '_ga': 'GA1.2.1991040555.1689839873',
        '_ga_5GG4DSTK86': 'GS1.1.1689839873.1.1.1689839925.0.0.0',
        'ajs_anonymous_id': '9a4e383e-f318-4aeb-a199-2428a5050775',
        'cart': '46192c085f8ef38ed7167b7731a3945c',
        'cart_ts': '1689839938',
        'cart_sig': '655a1c7033deac0d62e9852c45f48e01',
        'cart_ver': 'gcp-us-east1%3A6',
        'tolstoy-anonymousId': '92dc2087-9577-41bc-831d-29148fb7c4e6',
        'tolstoy-anonymousId': '92dc2087-9577-41bc-831d-29148fb7c4e6',
        '_gid': 'GA1.2.86345426.1689839886',
        '_clck': 'wxqao1|2|fdg|0|1296',
        '_fbp': 'fb.1.1689839893067.2122004465',
        '_clsk': '1skanjz|1689860264469|1|1|t.clarity.ms/collect',
        'IR_gbd': 'bark.co',
        'IR_13983': '1689839931888%7C0%7C1689839931888%7C%7C',
        '_ruid': 'eyJ1dWlkIjoiZjgzOTAzYzYtYTYyNS00ZTI1LWIzMjQtMTFlMjY5OGIyMjYzIn0%3D',
        'IR_PI': '32aa4b5c-26d3-11ee-adea-d3c413a970a3%7C1689926297221',
        'irclickid': '~35VRQSLCwAsyzBHMOPW2SJKDIEwxBwzsvxohi~-975WONMFDCAwm',
        'rl_session': 'RudderEncrypt%3AU2FsdGVkX1%2BFRiN884HovyCcWYXl9tUpf3tzqGhyfnEAnjVngew6SaUmyOmLuZ82i3b49MnwZfKPz%2Fdzbxb682AMQYAqZN%2FEo%2B9nAiu26yd3tVxwftnNiwjxiVrPStYS9cPQme6IxGTctlv9tGn6pw%3D%3D',
        'rl_user_id': 'RudderEncrypt%3AU2FsdGVkX1%2BmfJsqsog7IxZbUuo0AQCKcvox7mjFuSo%3D',
        'rl_trait': 'RudderEncrypt%3AU2FsdGVkX1%2FUAXcx8Z8JBeMyb%2BiTedrgGdsi3kgpzpc%3D',
        'rl_group_id': 'RudderEncrypt%3AU2FsdGVkX1%2FIItoXhrrGFpk%2FXZ18qqPSDr3qWk%2FoSz8%3D',
        'rl_group_trait': 'RudderEncrypt%3AU2FsdGVkX1%2F4CMisjP2kt%2BuJD3W3mBMZYLJ9dC3xP4M%3D',
        'rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX19A%2B2OsyQGBKJLiUxCIonAM3zMR%2FNFluA9%2FRbpFv%2B0T%2F07kFPDxpwRDB6j6%2F8fd%2B8FEKZMcpc0tEQ%3D%3D',
        'rl_page_init_referrer': 'RudderEncrypt%3AU2FsdGVkX19bXGABD1ixGw3qs9wpkmfxK3pb%2FhaNVNwLs78ae8i%2BIJFCSscFcr5Gt4OJ1HvmMv2%2F8dFGYYkfog%3D%3D',
        'rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX1%2BC%2BDj6qtxq45t8EtfKF0n0vmFz7z5G%2BRU%3D',
        'kaktuspCurrentShownPerMonth': '0',
        'kaktuspStartDatePerMonth': 'Thu%2C%2020%20Jul%202023%2007%3A58%3A20%20GMT',
        'kaktuspCurrentShownPerDay': '0',
        'kaktuspStartDatePerDay': 'Thu%2C%2020%20Jul%202023%2007%3A58%3A20%20GMT',
        'rs_shopify_cart_identified_at': '1689857910087',
        'cjConsent': 'MHxOfDB8Tnww',
        'cjUser': '16498212-80ea-4ca7-bf0c-67bb584f0003',
        '_uetsid': '22d308a026d311ee91d3c7e16190af84',
        '_uetvid': '22d3375026d311eeaf39dd1d267a0055',
        '_s': '3768d13c-7364-44ca-b591-3afd47ed0d62',
        '_shopify_s': '3768d13c-7364-44ca-b591-3afd47ed0d62',
        'keep_alive': 'd6c32de6-802d-489c-a2a8-e5c70eff77fa',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://food.bark.co/collections/toppers',
        'Alt-Used': 'food.bark.co',
        'Connection': 'keep-alive',
        # 'Cookie': 'secure_customer_sig=; localization=US; cart_currency=USD; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22US%22%2C%22sale_of_data_region%22%3Afalse%7D; _y=391b749c-caf7-42f1-8133-62458d9df1bf; _shopify_y=391b749c-caf7-42f1-8133-62458d9df1bf; _orig_referrer=https%3A%2F%2Fwww.barkbox.com%2F; _landing_page=%2F%3Futm_medium%3Drails-website%26utm_source%3Dbark_header%26utm_campaign%3D20220801_all-bark__eats_all_evergreen_control%26utm_term%3Deats; _gcl_au=1.1.1726273313.1689839870; __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE2ODk4Mzk4NzMsInZhbHVlIjoiaHR0cHM6Ly93d3cuYmFya2JveC5jb20vIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vZm9vZC5iYXJrLmNvLz91dG1fbWVkaXVtPXJhaWxzLXdlYnNpdGUmdXRtX3NvdXJjZT1iYXJrX2hlYWRlciZ1dG1fY2FtcGFpZ249MjAyMjA4MDFfYWxsLWJhcmtfX2VhdHNfYWxsX2V2ZXJncmVlbl9jb250cm9sJnV0bV90ZXJtPWVhdHMifSwiJGxhc3RfcmVmZXJyZXIiOnsidHMiOjE2ODk4Mzk5MjIsInZhbHVlIjoiaHR0cHM6Ly93d3cuYmFya2JveC5jb20vIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vZm9vZC5iYXJrLmNvLz91dG1fbWVkaXVtPXJhaWxzLXdlYnNpdGUmdXRtX3NvdXJjZT1iYXJrX2hlYWRlciZ1dG1fY2FtcGFpZ249MjAyMjA4MDFfYWxsLWJhcmtfX2VhdHNfYWxsX2V2ZXJncmVlbl9jb250cm9sJnV0bV90ZXJtPWVhdHMifX0=; _ga_NKW49FBKXG=GS1.1.1689839873.1.1.1689839925.0.0.0; _ga=GA1.2.1991040555.1689839873; _ga_5GG4DSTK86=GS1.1.1689839873.1.1.1689839925.0.0.0; ajs_anonymous_id=9a4e383e-f318-4aeb-a199-2428a5050775; cart=46192c085f8ef38ed7167b7731a3945c; cart_ts=1689839938; cart_sig=655a1c7033deac0d62e9852c45f48e01; cart_ver=gcp-us-east1%3A6; tolstoy-anonymousId=92dc2087-9577-41bc-831d-29148fb7c4e6; tolstoy-anonymousId=92dc2087-9577-41bc-831d-29148fb7c4e6; _gid=GA1.2.86345426.1689839886; _clck=wxqao1|2|fdg|0|1296; _fbp=fb.1.1689839893067.2122004465; _clsk=1skanjz|1689860264469|1|1|t.clarity.ms/collect; IR_gbd=bark.co; IR_13983=1689839931888%7C0%7C1689839931888%7C%7C; _ruid=eyJ1dWlkIjoiZjgzOTAzYzYtYTYyNS00ZTI1LWIzMjQtMTFlMjY5OGIyMjYzIn0%3D; IR_PI=32aa4b5c-26d3-11ee-adea-d3c413a970a3%7C1689926297221; irclickid=~35VRQSLCwAsyzBHMOPW2SJKDIEwxBwzsvxohi~-975WONMFDCAwm; rl_session=RudderEncrypt%3AU2FsdGVkX1%2BFRiN884HovyCcWYXl9tUpf3tzqGhyfnEAnjVngew6SaUmyOmLuZ82i3b49MnwZfKPz%2Fdzbxb682AMQYAqZN%2FEo%2B9nAiu26yd3tVxwftnNiwjxiVrPStYS9cPQme6IxGTctlv9tGn6pw%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2BmfJsqsog7IxZbUuo0AQCKcvox7mjFuSo%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2FUAXcx8Z8JBeMyb%2BiTedrgGdsi3kgpzpc%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2FIItoXhrrGFpk%2FXZ18qqPSDr3qWk%2FoSz8%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2F4CMisjP2kt%2BuJD3W3mBMZYLJ9dC3xP4M%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX19A%2B2OsyQGBKJLiUxCIonAM3zMR%2FNFluA9%2FRbpFv%2B0T%2F07kFPDxpwRDB6j6%2F8fd%2B8FEKZMcpc0tEQ%3D%3D; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX19bXGABD1ixGw3qs9wpkmfxK3pb%2FhaNVNwLs78ae8i%2BIJFCSscFcr5Gt4OJ1HvmMv2%2F8dFGYYkfog%3D%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2BC%2BDj6qtxq45t8EtfKF0n0vmFz7z5G%2BRU%3D; kaktuspCurrentShownPerMonth=0; kaktuspStartDatePerMonth=Thu%2C%2020%20Jul%202023%2007%3A58%3A20%20GMT; kaktuspCurrentShownPerDay=0; kaktuspStartDatePerDay=Thu%2C%2020%20Jul%202023%2007%3A58%3A20%20GMT; rs_shopify_cart_identified_at=1689857910087; cjConsent=MHxOfDB8Tnww; cjUser=16498212-80ea-4ca7-bf0c-67bb584f0003; _uetsid=22d308a026d311ee91d3c7e16190af84; _uetvid=22d3375026d311eeaf39dd1d267a0055; _s=3768d13c-7364-44ca-b591-3afd47ed0d62; _shopify_s=3768d13c-7364-44ca-b591-3afd47ed0d62; keep_alive=d6c32de6-802d-489c-a2a8-e5c70eff77fa',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'If-None-Match': 'W/"cacheable:d450e5660f5d54243290900cef3c90fc"',
    }

    params = {
        'selling_plan': '1202651223',
    }

    params_o = {
        'limit': '5',
        'orderBy': 'rating desc',
        'lastEvaluated': '{"subscriberId_collectionId":"98e74aa8-de0f-4200-9ffd-632aa583617c:bc54ca94-c49d-4888-aa55-cf238b5790c7","reviewId":"2e40f289-b5cd-4c89-ba20-ded7c74ad0ac","_rating_dateCreated":"5:2023-06-19T22:56:35.130Z"}',
    }
    def start_requests(self):
        with open("bark.txt") as file:
            urls = file.read()
        lsturls = urls.split("\n")
        for url in lsturls:
            yield scrapy.Request(url,callback=self.get_reviews1, headers=self.headers,cookies=self.cookies, dont_filter=True)
    def get_reviews1(self,response):
        surl=response.url
        try:
            html=response.text.split('<script type="application/json" data-oke-metafield-data="">')
            for item in html:
                try:
                    htm=item.split('</script>')[0]
                    Data=json.loads(htm)
                    if "reviews" in Data:
                        try:
                            subscriberId_collectionId=Data['media'][0]['subscriberId_collectionId']
                            # print("page 1 "+subscriberId_collectionId+"\n")
                            reviewsNextUrl=Data['reviewsNextUrl']
                            tmp=reviewsNextUrl.split('%2C')
                            reviewId=tmp[1].split("%22%3A%22")[1].replace("%22","")
                            rating_dateCreated=tmp[2].split("%22%3A%22")[1].replace("%3A",":").replace("%7D","").replace("%22","")
                        except:
                            pass
                        subscriberId=Data['reviews'][0]['subscriberId']
                        productId=Data['reviews'][0]['productId']
                        for review in Data['reviews']:
                            Name=review['reviewer']['displayName']
                            Stars=review['rating']
                            Date=review['dateCreated'].split('T')[0]
                            Title=review['title']
                            Description=review['body']
                            Helpful=review['helpfulCount']
                            Not_Helpful=review['unhelpfulCount']
                            rid=review['reviewId']
                            with open('bark1.csv', 'a', newline='', encoding="utf-8") as file:
                                writer = csv.writer(file)
                                writer.writerow([Name, Stars, Date, Title, Description, Helpful, Not_Helpful])
                        if len(Data['reviews'])>=10:#if it's other pages
                            self.params_o['lastEvaluated']='{"subscriberId_collectionId":"'+subscriberId_collectionId+'","reviewId":"'+reviewId+'","_rating_dateCreated":"'+rating_dateCreated+'"}'
                            # print("Check: "+str(self.params_o))
                            # self.params_o['lastEvaluated']=subscriberId_collectionId                           
                            # self.params_o['lastEvaluated']['reviewId']=reviewId
                            # self.params_o['lastEvaluated']['_rating_dateCreated']=rating_dateCreated
                            url="https://api.okendo.io/v1/stores/"+subscriberId+"/products/"+productId+"/reviews"
                            # response = requests.get(url,params=self.params_o,headers=self.headers,)
                            # print("response: "+response.text)
                            yield scrapy.FormRequest(url,callback=self.get_reviews2, method='GET', headers=self.headers,cookies=self.cookies,formdata = self.params_o, meta={'surl':surl},dont_filter=True)
                except:
                    pass
        except:
            pass                   
    def get_reviews2(self,response):
        Data=json.loads(response.text)
        surl=response.meta['surl']
        for review in Data['reviews']:
            Name=review['reviewer']['displayName']
            Stars=review['rating']
            Date=review['dateCreated'].split('T')[0]
            Title=review['title']
            Description=review['body']
            Helpful=review['helpfulCount']
            Not_Helpful=review['unhelpfulCount']
            rid=review['reviewId']
            with open('bark1.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([Name, Stars, Date, Title, Description, Helpful, Not_Helpful])
        if len(Data['reviews'])>=5:#if it's other pages
            # print("start page 3")
            reviewsNextUrl=Data['nextUrl']
            tmp=reviewsNextUrl.split('%2C')
            subscriberId_collectionId=tmp[0].split("%22%3A%22")[1].replace("%22","").replace("%3A",":")
            reviewId=tmp[1].split("%22%3A%22")[1].replace("%22","")
            rating_dateCreated=tmp[2].split("%22%3A%22")[1].replace("%3A",":").replace("%7D","").replace("%22","")
            subscriberId=Data['reviews'][0]['subscriberId']
            productId=Data['reviews'][0]['productId']
            self.params_o['lastEvaluated']='{"subscriberId_collectionId":"'+subscriberId_collectionId+'","reviewId":"'+reviewId+'","_rating_dateCreated":"'+rating_dateCreated+'"}'
            # self.params_o['lastEvaluated']['subscriberId_collectionId']=subscriberId_collectionId
            # self.params_o['lastEvaluated']['reviewId']=reviewId
            # self.params_o['lastEvaluated']['_rating_dateCreated']=rating_dateCreated
            url="https://api.okendo.io/v1/stores/"+subscriberId+"/products/"+productId+"/reviews"
            yield scrapy.FormRequest(url,callback=self.get_reviews2, method='GET', headers=self.headers,cookies=self.cookies,formdata = self.params_o, meta={'surl':surl}, dont_filter=True)
        