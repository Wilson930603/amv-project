import scrapy,json,csv,os, requests, urllib, shutil
class CrawlerSpider(scrapy.Spider):
    name = 'chewy'
    cookies = {
        'AWSALB': 'do9a01OYYXFMCOEBZfyKG704pHI/lkjhex/TIuFUNu+zTNsnW9tyDSxDGslhF9ZPxUFrhaafqIIkdtQN3qpjHUBKt9IuS3OqM7HGPWs3Z/PsuBToy99l45QGOOFI',
        'AWSALBCORS': 'do9a01OYYXFMCOEBZfyKG704pHI/lkjhex/TIuFUNu+zTNsnW9tyDSxDGslhF9ZPxUFrhaafqIIkdtQN3qpjHUBKt9IuS3OqM7HGPWs3Z/PsuBToy99l45QGOOFI',
        'pid': 'ArQcAHkbTvaTRSv-IYTM1g',
        'sid': '8a2b8ab0-d8f5-4be2-b01f-b88992d59653',
        'x-feature-preview': 'false',
        'AKA_A2': 'A',
        'sbsd': '000000000096bc8a7445dc9c628c5803cf9b3fe21bf3314aa2071c3491323387bb36381464df9139d9-f10e-4407-b771-dbb0e3fceaa416926113301689932430',
        'akavpau_defaultvp': '1689932794~id=8e9d11ecd04c2208cf6a4fd7faba8e52',
        'akaalb_chewy_ALB': '1689933094~op=chewy_com_ALB:www-chewy-use2|~rv=100~m=www-chewy-use2:0|~os=43a06daff4514d805d02d3b6b5e79808~id=8a1041bd74cf6020fa596e7381bdfdf5',
        '_abck': '141F824A95D918C24296A15D2A6CEF14~0~YAAQOD4SAlMzLSyJAQAAcA3Tdwq5G2HwzRnmOctwfArNgY51Usx13p6F4wdheWFrNeZnnmkfflFOxlUpiqhD5dRc8viELMuY7zZxJGa5duzOceDF+5dfTuX8QFl6jI3IhfuVk9pJXgTPjJW4nhlolPzp9h9jg4lFiTrLfH/HxHjUI4TyjPOYSIob4WuFpqMVQ/cwdsqjOlWJi7SBwzs9KemwnKBSo4ScGXY1c0Eie6UJS/qQwQoXtX+h7zSRUh/YqpS+bCZ1mjcMgEi9sNAr3j7QQP3lr/whjqWSS8i9ieirHBndVBjPi+Ox/wGT0XeZtSEg2mBfljEZsdrreZUn7cKblY69zfw+CWK6yJHidLOochuvwVNy0805CqItSVKRTMY8xfDt9ZusQrOMgRpkC+3KbQYeHaS0~-1~||-1||~-1',
        'ak_bmsc': '86B692EBD61B82683A8068241B227147~000000000000000000000000000000~YAAQOD4SAvgwLSyJAQAAKuHSdxQ/8JXl+y3Jv5WIgcqe6M029/c2KVMGY+gLTiSiTHlGIwNk2s5W6QhjTwigr4Ab6QrtkAK9oBw9ePgti3q/3Npw+vsZ1xmy8G1ffNl8m0PovptVI5Po1OtJWjafZ1znwd3PWZiHslQrH+xA03XBmEMl1i/IVFAkX1xN9is9RkoyPJKeNcmCryOlFCpIWrDAXXGlmtCJupcrb1Tb92pSGZ7Q3s/O8HMfeXOOHHhFpOtFS9MOEMPE8hevNxlHWdT43smufnYrc/CpryHVXd58FiVZRkD3Bq4+aAR3xt9Z2R0I5sFfhah9lImBrGCQBBYVT1zcSEVfv+7ot4eMbgyTQYCrDKVj9wzq0e82+Mdd3Nm0lXaMQXJDqFLn4hUp9j9ry9TFBjnAYZqaOTNPZN693o85PC7kSDv0OBYqrChcMqNFWt7W6vBkETVzXbEfIlPaHVlttYU8swWRkZN+/a7U3sxFbq6FiCkvkw==',
        'bm_sz': '9BD40B052E3486A2B600F602611A5542~YAAQOD4SAuIpLSyJAQAA5oDSdxSnziJqDAI0+oXIHrwCgEYIYdaNdXNpXqngT9Gp/Sdv9YwatbupReIXFEpty+X3yGdvGv5per0CSIvMcQRAxzhC/InRCwgJR6xbTVUYqp+3EFWjKbCoqgB9pZm1tYBeRSBYnDmDvsMbnUe9bX3Mtau5zJ8NlwljVOPAAELV/3V0wF/+HZRTBW7GR0QlzgIvLKhalbu/0NZkzQTy95nhV4Fpcll4oLdzL8mLDWt2oUxdgwceqFSGLAJozIbn2WJKjSudAT73XxAFhvQOkuJf3Q==~4469811~3425857',
        'bm_sv': '10FE33938CD692CFCEFCF41486077ECC~YAAQOD4SAvM4LSyJAQAAi1PTdxTH9hyRUSNvSx92k8euqs25ZDo9PKhjfvGgv9iNZ6Sd1KchVy/J8aCSohWKRYyCWJYZD6ky+IPlQqZVQoP6mULrtLVxlIGKLUdwUljv+7CBJ5/7hhENC036kiIbbd2mJG11KxLiy8bS7N8n3wcLN4puXmgs4gjwzGuvH1cjf0crMwqMzN2d281maubVnQ9n7yUyqbTpBm9y1TjQW+JUNqpNVXvS/qLxwsmAyiA=~1',
        'abTestingAnonymousPID': 'ArQcAHkbTvaTRSv-IYTM1g',
        'RT': '"z=1&dm=www.chewy.com&si=479806df-43b7-4594-b805-bf3a1985ed19&ss=lkce4w64&sl=1&tt=1hnu&rl=1&ld=1ho6"',
        '_gcl_au': '1.1.2067679901.1689932452',
        'pageviewCount': '1',
        '_ga_GM4GWYGVKP': 'GS1.1.1689932457.1.0.1689932477.40.0.0',
        '_ga': 'GA1.2.861311296.1689932457',
        'ajs_anonymous_id': '70e10db2-02cd-4dec-b711-210ad9b77cc2',
        '_mibhv': 'anon-1689932468606-6124114106_6593',
        '_uetsid': 'bb054b9027aa11eeb881336d29545015',
        '_uetvid': 'bb053fe027aa11eea61fa16cbbfb2777',
        '_gid': 'GA1.2.374810693.1689932485',
        '_tt_enable_cookie': '1',
        '_ttp': 'ScEbolY9TtlK-27GyDYz5Wn28y1',
        '_fbp': 'fb.1.1689932491755.1972394541',
        'FPLC': 'D9NlvRvXB%2BRlIupwy0YVqfh6Q4%2F5PXvQ58qmu9toZ89d8mYCSkzZrgIMIwltcxUlfeRg76Ji2qeKWnmFZrVNu3CafsX%2BoPiZZkWS8cRq%2FP81E9N%2Fy0tHoJS85Jre7Q%3D%3D',
        'FPID': 'FPID1.2.q0KjhTAcJgTdAW7NAjsudHjQosUmY3r4v6r54MEhIvs%3D.1689932457',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Jul+21+2023+02%3A41%3A38+GMT-0700+(Pacific+Daylight+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.chewy.com%2Fvictor-classic-hi-pro-plus-formula%2Fdp%2F120687&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1',
        'addshoppers.com': '2%7C1%3A0%7C10%3A1689932507%7C15%3Aaddshoppers.com%7C44%3ANThjNGRmNzI3ZmQ2NDU3ZjgxZDA3NWJlYWVjMjQzZDY%3D%7C234b0fc394f2481b43c52de19bc0908f379f28b7046cde828ec8da34bdc72865',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Referer': 'https://www.chewy.com/victor-classic-hi-pro-plus-formula/dp/120687',
        'Origin': 'https://www.chewy.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        # 'Cookie': 'AWSALB=do9a01OYYXFMCOEBZfyKG704pHI/lkjhex/TIuFUNu+zTNsnW9tyDSxDGslhF9ZPxUFrhaafqIIkdtQN3qpjHUBKt9IuS3OqM7HGPWs3Z/PsuBToy99l45QGOOFI; AWSALBCORS=do9a01OYYXFMCOEBZfyKG704pHI/lkjhex/TIuFUNu+zTNsnW9tyDSxDGslhF9ZPxUFrhaafqIIkdtQN3qpjHUBKt9IuS3OqM7HGPWs3Z/PsuBToy99l45QGOOFI; pid=ArQcAHkbTvaTRSv-IYTM1g; sid=8a2b8ab0-d8f5-4be2-b01f-b88992d59653; x-feature-preview=false; AKA_A2=A; sbsd=000000000096bc8a7445dc9c628c5803cf9b3fe21bf3314aa2071c3491323387bb36381464df9139d9-f10e-4407-b771-dbb0e3fceaa416926113301689932430; akavpau_defaultvp=1689932794~id=8e9d11ecd04c2208cf6a4fd7faba8e52; akaalb_chewy_ALB=1689933094~op=chewy_com_ALB:www-chewy-use2|~rv=100~m=www-chewy-use2:0|~os=43a06daff4514d805d02d3b6b5e79808~id=8a1041bd74cf6020fa596e7381bdfdf5; _abck=141F824A95D918C24296A15D2A6CEF14~0~YAAQOD4SAlMzLSyJAQAAcA3Tdwq5G2HwzRnmOctwfArNgY51Usx13p6F4wdheWFrNeZnnmkfflFOxlUpiqhD5dRc8viELMuY7zZxJGa5duzOceDF+5dfTuX8QFl6jI3IhfuVk9pJXgTPjJW4nhlolPzp9h9jg4lFiTrLfH/HxHjUI4TyjPOYSIob4WuFpqMVQ/cwdsqjOlWJi7SBwzs9KemwnKBSo4ScGXY1c0Eie6UJS/qQwQoXtX+h7zSRUh/YqpS+bCZ1mjcMgEi9sNAr3j7QQP3lr/whjqWSS8i9ieirHBndVBjPi+Ox/wGT0XeZtSEg2mBfljEZsdrreZUn7cKblY69zfw+CWK6yJHidLOochuvwVNy0805CqItSVKRTMY8xfDt9ZusQrOMgRpkC+3KbQYeHaS0~-1~||-1||~-1; ak_bmsc=86B692EBD61B82683A8068241B227147~000000000000000000000000000000~YAAQOD4SAvgwLSyJAQAAKuHSdxQ/8JXl+y3Jv5WIgcqe6M029/c2KVMGY+gLTiSiTHlGIwNk2s5W6QhjTwigr4Ab6QrtkAK9oBw9ePgti3q/3Npw+vsZ1xmy8G1ffNl8m0PovptVI5Po1OtJWjafZ1znwd3PWZiHslQrH+xA03XBmEMl1i/IVFAkX1xN9is9RkoyPJKeNcmCryOlFCpIWrDAXXGlmtCJupcrb1Tb92pSGZ7Q3s/O8HMfeXOOHHhFpOtFS9MOEMPE8hevNxlHWdT43smufnYrc/CpryHVXd58FiVZRkD3Bq4+aAR3xt9Z2R0I5sFfhah9lImBrGCQBBYVT1zcSEVfv+7ot4eMbgyTQYCrDKVj9wzq0e82+Mdd3Nm0lXaMQXJDqFLn4hUp9j9ry9TFBjnAYZqaOTNPZN693o85PC7kSDv0OBYqrChcMqNFWt7W6vBkETVzXbEfIlPaHVlttYU8swWRkZN+/a7U3sxFbq6FiCkvkw==; bm_sz=9BD40B052E3486A2B600F602611A5542~YAAQOD4SAuIpLSyJAQAA5oDSdxSnziJqDAI0+oXIHrwCgEYIYdaNdXNpXqngT9Gp/Sdv9YwatbupReIXFEpty+X3yGdvGv5per0CSIvMcQRAxzhC/InRCwgJR6xbTVUYqp+3EFWjKbCoqgB9pZm1tYBeRSBYnDmDvsMbnUe9bX3Mtau5zJ8NlwljVOPAAELV/3V0wF/+HZRTBW7GR0QlzgIvLKhalbu/0NZkzQTy95nhV4Fpcll4oLdzL8mLDWt2oUxdgwceqFSGLAJozIbn2WJKjSudAT73XxAFhvQOkuJf3Q==~4469811~3425857; bm_sv=10FE33938CD692CFCEFCF41486077ECC~YAAQOD4SAvM4LSyJAQAAi1PTdxTH9hyRUSNvSx92k8euqs25ZDo9PKhjfvGgv9iNZ6Sd1KchVy/J8aCSohWKRYyCWJYZD6ky+IPlQqZVQoP6mULrtLVxlIGKLUdwUljv+7CBJ5/7hhENC036kiIbbd2mJG11KxLiy8bS7N8n3wcLN4puXmgs4gjwzGuvH1cjf0crMwqMzN2d281maubVnQ9n7yUyqbTpBm9y1TjQW+JUNqpNVXvS/qLxwsmAyiA=~1; abTestingAnonymousPID=ArQcAHkbTvaTRSv-IYTM1g; RT="z=1&dm=www.chewy.com&si=479806df-43b7-4594-b805-bf3a1985ed19&ss=lkce4w64&sl=1&tt=1hnu&rl=1&ld=1ho6"; _gcl_au=1.1.2067679901.1689932452; pageviewCount=1; _ga_GM4GWYGVKP=GS1.1.1689932457.1.0.1689932477.40.0.0; _ga=GA1.2.861311296.1689932457; ajs_anonymous_id=70e10db2-02cd-4dec-b711-210ad9b77cc2; _mibhv=anon-1689932468606-6124114106_6593; _uetsid=bb054b9027aa11eeb881336d29545015; _uetvid=bb053fe027aa11eea61fa16cbbfb2777; _gid=GA1.2.374810693.1689932485; _tt_enable_cookie=1; _ttp=ScEbolY9TtlK-27GyDYz5Wn28y1; _fbp=fb.1.1689932491755.1972394541; FPLC=D9NlvRvXB%2BRlIupwy0YVqfh6Q4%2F5PXvQ58qmu9toZ89d8mYCSkzZrgIMIwltcxUlfeRg76Ji2qeKWnmFZrVNu3CafsX%2BoPiZZkWS8cRq%2FP81E9N%2Fy0tHoJS85Jre7Q%3D%3D; FPID=FPID1.2.q0KjhTAcJgTdAW7NAjsudHjQosUmY3r4v6r54MEhIvs%3D.1689932457; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+21+2023+02%3A41%3A38+GMT-0700+(Pacific+Daylight+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.chewy.com%2Fvictor-classic-hi-pro-plus-formula%2Fdp%2F120687&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1; addshoppers.com=2%7C1%3A0%7C10%3A1689932507%7C15%3Aaddshoppers.com%7C44%3ANThjNGRmNzI3ZmQ2NDU3ZjgxZDA3NWJlYWVjMjQzZDY%3D%7C234b0fc394f2481b43c52de19bc0908f379f28b7046cde828ec8da34bdc72865',
    }

    json_data = {
        'operationName': 'Reviews',
        'variables': {
            'sort': 'MOST_RELEVANT',
            'id': '120687',
            'after': 'YXJyYXljb25uZWN0aW9uOjE5',
        },
        'extensions': {},
        'query': 'query Reviews($id: String!, $after: String, $feature: String, $filter: ReviewFilter, $sort: ReviewSort = MOST_RELEVANT, $hasPhoto: Boolean, $reviewText: String) {\n  product(id: $id) {\n    id\n    ...Reviews\n    ...ReviewFeatures\n    __typename\n  }\n}\n\nfragment Reviews on Product {\n  id\n  partNumber\n  name\n  reviews(\n    after: $after\n    feature: $feature\n    filter: $filter\n    first: 10\n    sort: $sort\n    hasPhoto: $hasPhoto\n    reviewText: $reviewText\n  ) {\n    totalCount\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    edges {\n      node {\n        id\n        ...Review\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Review on Review {\n  id\n  contentId\n  helpfulness\n  photos {\n    ...UserGeneratedPhoto\n    __typename\n  }\n  rating\n  submittedAt\n  submittedBy\n  contributorBadge\n  isIncentivized\n  text\n  title\n  __typename\n}\n\nfragment UserGeneratedPhoto on UserGeneratedPhoto {\n  __typename\n  caption\n  fullImage\n  thumbnail\n}\n\nfragment ReviewFeatures on Product {\n  id\n  partNumber\n  reviewFeatures\n  __typename\n}\n',
    }
    def start_requests(self):
        with open("chewy.txt") as file:
            urls = file.read()
        lsturls = urls.split("\n")
        for url in lsturls:
            yield scrapy.Request(url,callback=self.get_reviews_1, headers=self.headers,cookies=self.cookies, dont_filter=True)
    def get_reviews_1(self,response):
        url=response.url
        html=response.text.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0]
        Data=json.loads(html)
        item=Data['props']['pageProps']['__APOLLO_STATE__']
        j=1
        for rv in item:
            if rv.split(':')[0]=='Product':
                itemname=item[rv]['name']
                id=item[rv]['entryID']
                for cu in item[rv]:
                    if cu.split(':')[0]=='reviews':
                        endCursor=item[rv][cu]['pageInfo']['endCursor']
            if rv.split(':')[0]=='Review':
                Name=item[rv]['submittedBy']
                Stars=item[rv]['rating']
                Date=item[rv]['submittedAt'].split('T')[0]
                Title=item[rv]['title']
                Description=item[rv]['text']
                Helpful=item[rv]['helpfulness']
                with open('chewy.csv', 'a', newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([itemname, url, Name, Stars, Date, Title, Description, Helpful])
                j+=1
        if j>=10:
            self.json_data['variables']['after']=endCursor
            self.json_data['variables']['id']=id
            self.headers['Referer']=url
            murl='https://www.chewy.com/api/pdp/graphql'
            yield scrapy.Request(murl,callback=self.get_reviews_2, method='POST', headers=self.headers,cookies=self.cookies,body = json.dumps(self.json_data), meta={'urldetail':url,'itemname':itemname,'id':id},dont_filter=True)
    def get_reviews_2(self,response):
        Data=json.loads(response.text)
        items=Data['data']['product']['reviews']['edges']
        url=response.meta['urldetail']
        itemname=response.meta['itemname']
        id=response.meta['id']
        endCursor=Data['data']['product']['reviews']['pageInfo']['endCursor']
        j=1
        for it in items:
            Name=it['node']['submittedBy']
            Stars=it['node']['rating']
            Date=it['node']['submittedAt'].split('T')[0]
            Title=it['node']['title']
            Description=it['node']['text']
            Helpful=it['node']['helpfulness']
            with open('chewy.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([itemname, url, Name, Stars, Date, Title, Description, Helpful])
            j+=1
        if j>=10:
            self.json_data['variables']['after']=endCursor
            self.json_data['variables']['id']=id
            self.headers['Referer']=url
            murl='https://www.chewy.com/api/pdp/graphql'
            yield scrapy.Request(murl,callback=self.get_reviews_2, method='POST', headers=self.headers,cookies=self.cookies,body = json.dumps(self.json_data), meta={'urldetail':url,'itemname':itemname,'id':id},dont_filter=True)