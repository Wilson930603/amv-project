import scrapy,json
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'tredence'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    cookies = {'_t_ds': 'cc695d31679745222-24cc695d3-0cc695d3','_abck': '6C0D198348F729812896A9B7996C4A47~0~YAAQX2YzuI/gmwyHAQAAbkKeGAnqdIbYd/rPwl7aX5yV9+vuyL+1yRDxtPxQ+V/O6hB1CrUa+qpWERfm4gm7nbWRJg98ijUZd5DmN81DB2N9K6FDfhTgOBGHGH14SG9erzjIsjKw0i1B+D0FxYViRVFZtqlANtziYW1I3mqsy83+dho18OD4m3/vACRhJ486ju+MfRMDjkxn4ZnsFlCwZ7vKmBw3iPcdLuidtRbjeBEWVdCOQTPfXBkD2vZjn2d9JzBzrr6mc13q865zPBkWDsYhyePEkykfIoSrccbp2RlqdaogjC1siogrJ5vx98KnaATYiQcEfRoeAcN4k7rzX+H17y0bQCWALWonvurn0j7yDJJ1UF6bwLCPXjCqyr2DqsYRT+aZ6EjBpiCmYBFRMyU0omkvnwZCgQ==~-1~||-1||~-1','ak_bmsc': '881139FFD179126C43B4FE0236EF6E3D~000000000000000000000000000000~YAAQX2YzuOHfmwyHAQAARyGeGBOFzMc+GLZ0c7b5iL3NNGaHkaCFCrUbVOMRBMc4smPs5jJbS4xAZpqv6hdJWSGzZwszAJEjrDTHE5eL1T9cDzyThK2hI/kJviVNDSC8o3frJ36PeWboH/h9406FlpQqW57tED/4OdiHlPsk9UKo7xByldlMixRpH13aLpWrNpkBanaC2ibvclA3sxRVpsEQTggzTeuRKOMZERvSHRO4Td+1yQzkq5kgGmVMX4N10HwEjQPHFWnN+WSmM7tidQT8rVxRryM1inOOziTSf09e4J8JjwQLd7d6MxiCXlKerVIeDAnXhFQ+0kNVxn01K/Ql/3UnSpAVaoUk2GxU9Ci4GBi8WNtxdyoXdKsrnRyuLMmSzvY6zNI8yNcMwPlUx/0adg40ujhNTXHbn1g+WIZ0JUNrQu7nkSOIIqsCazrVZnurpcjtvWMkOv9Gn4UNrbQQ','bm_sz': 'F87668DEE6564B8E26FEA75ABACCEB8C~YAAQX2YzuFLfmwyHAQAAoQaeGBMlpEjlYN9hkgWVkmG5tqOF0tpN2BHNtPLql3AUnhjbPcY4QtXDvAP8byF0cv21QLUDx9EbcXlNeRAfljdRuF/b+PZB4fpwDrg5/6f5bOgi/5vnd3fNVL8YCBK1e8/kFm84kAsfzQqZgQfGAWfCn5QCCZ1bcKm2e8pMalKteDudUB5gvjGBE+6kLRB8SuJomnI0IDAeYQ8+8P9/EaaifVo0xf/vzKIY4TD0QUE6K5cHK79/31SkTMFdSoM8r7Tu1gtJJamiqNpMqK3U2aA3nFA=~3359796~3750199','_did': '8b4ab65696','bs_rnd': 'Mde7c27M','_odur': 'e93fb9b108','bm_mi': 'D91C59CA49A1A594B41100CDB8C969B0~YAAQX2YzuFffmwyHAQAArweeGBMr6vnFDRkmrXB5eM2I3isR1EX9qUTwjQmzurLTnQ/E5GcA0HccIeWsxaCxkfpBx8Wjbu9+6zJk8XMXVWaLOSZDl6bjtJb/F6ylytnx+ENmKyu4bp9RCVV0oXl0kEYJqJake2s2A9zw8/lY3BN6mkWTKAbAOe8mXSD5DZreMhEKh8IxGaF6XBDNB8ofelFLg2BMxW/3vVCwfWF6Hwj+0vLS23c4bz1tYFpWfgKiculMR2fz71G9ccOXqc7f8W6lYBu41ObOkz17WHlzk1zHGliU0+Kxu08xDEdnzQIzOpQM0oRQlwQlhBY=~1','bm_sv': '445DAD9DB1A4264AB003DB3D2E62BACA~YAAQX2YzuGjtmwyHAQAASfWgGBMJGJ9WONJn2o6mb5i7v3f7OvdFjDJZlM+8VBFGMhmw15OgLwMKtfuPPWvzZAzfyaxY4wdsoIZx+SZA7WmFuaLq+8WWJaz1b9wUZ/Q1kyzxEP7UJDJ8NXMwtEOn1+bCGJizKrRYtf/Xu2J/n70KyMe8ubBlm7IGq/JjCrr9OQ6hrm9jOJJvyacsLm0mM+5Y3oo8yZ2YkTzgrJ7R69sQ2K8UeOzFK917frXiMJ2zOA==~1','page_visit': '1','7e5d03287561b86f0a1216e3aa6fb8041s7': 'v0%7CUB4iL0%2FtT69DdgxmtW0e1m3CY3BdDvRWR474XWosO6%2BYFF265rOUvw%2B5GCjFZ7sxpwYPMBXgDdDWjerQnMpceiq6o7ou%2FLM0jMOFlbbpu%2FenL5F86E5xnNrhwgCz3gxKZB7g0rDE1HZMZHA4rpxZNZyz5F%2FZoPeXeLR8fzIWYlg%3D','_gcl_au': '1.1.260306385.1679745226','dfp': '9b3acd7ad6cdc49c7d345f7ce0601339','_ga': 'GA1.2.1401955267.1679745227','_gid': 'GA1.2.1449463592.1679745227','LPVID': 'llMDE0YWM4MGI5ZTFmOTNl','LPSID-77159344': 'YWtmhGlyTcGi247lovdX-w','kycEligibleCookie1360722': '0','ACCESS': '1679745364','UNID': 'DmVYhkVuCbJ9auiZd3O6qpFAe64NAP0aZ7ZIaMRw','pvId': '0','UNPC': '1360722','UNCC': '123739023','_uv123739023': 'isSet','HOWTORT': 'ul=1679745403330&r=https%3A%2F%2Fresdex.naukri.com%2Fv3%2Fsearch%2FsavedSearches&hd=1679745403895&cl=1679745415434&nu=https%3A%2F%2Fresdex.naukri.com%2Fv3%2Fsearch%3FagentId%3D57537901','test': 'naukri.com','showEmailLB123739023': 'isSet','showDomainLB123739023': '1','isAddMobShown123739023': '1',}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0','Accept': 'application/json','Accept-Language': 'en-GB,en;q=0.5','AppId': '112','systemId': 'naukriIndia','Content-Type': 'application/json','X-transaction-ID': 'srp82221953101051114288745415790~~94fe88','Origin': 'https://resdex.naukri.com','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin',}
    url='https://resdex.naukri.com/cloudgateway-resdex/recruiter-js-profile-listing-services/v0/search/results/pageChange'
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    def start_requests(self):
        json_data = {'pageNo': 1,'miscellaneousInfo': {'companyId': 1360722,'rdxUserId': '123739023','rdxUserName': 'deepak.kinra@tredence.com','sid': 5903323241,'sidGroupId': 'd0e25a8c2e0a0fa2186048f1d0a4b21b','flowId': 'd0e25a8c2e0a0fa2186048f1d0a4b21b','flowName': 'search','fetchClusters': False,'fetchResumeTuples': True,'s2jEnabled': False}}
        yield scrapy.Request(self.url,callback=self.parse,meta={'json_data':json_data},method='POST',body=json.dumps(json_data),headers=self.headers,cookies=self.cookies)
    def parse(self, response):
        json_data=response.meta['json_data']
        Data=json.loads(response.text)['tuples']
        for row in Data:
            item={}
            item['Name']=row.get('jsUserName','')
            item['Experience']=str(row['experience'].get('years',''))+'y '+str(row['experience'].get('months',''))+'m'
            item['Salary']=row['ctcInfo'].get('lacs','')+' Lacs'
            item['City']=row.get('currentLocation','')
            item['Title']=row['employment']['current'].get('designation','')+' at '+row['employment']['current'].get('organization','')
            item['Views']=row.get('numberOfViews','')
            item['Downloads']=row.get('numberOfDownloads','')
            item['Modified on']=datetime.fromtimestamp(row.get('modifyDateMillis',0)/1000).strftime('%Y-%m-%d')
            item['Active']=datetime.fromtimestamp(row.get('activeDateMillis',0)/1000).strftime('%Y-%m-%d')
            yield(item)
        if len(Data)>=10:
            json_data['pageNo']+=1
            yield scrapy.Request(self.url,callback=self.parse,meta={'json_data':json_data},method='POST',body=json.dumps(json_data),headers=self.headers,cookies=self.cookies)