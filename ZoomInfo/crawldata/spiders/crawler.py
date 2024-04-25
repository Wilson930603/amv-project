import scrapy,json,re,os,platform,requests
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'zoomInfo'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    cookies = {
    '_pxvid': 'bccd95cd-3850-11ee-9c4c-dbe558f3a4c5',
    'pxcts': 'bef29d1a-3850-11ee-8767-6e7153647252',
    '_gcl_au': '1.1.74197344.1691762995',
    '_gid': 'GA1.2.754440212.1691762995',
    'cesignupoption': '2',
    'userEmail': 'info%40crawler.pro.vn',
    'doziUser': 'info%40crawler.pro.vn',
    'ziMongoId': '31697769',
    'signupCountry': 'VN',
    'signupMethod': 'GOOGLE_OAUTH_CE_SIGNUP',
    'G_ENABLED_IDPS': 'google',
    '_ga_CVRYW5BMEY': 'GS1.2.1691765290.2.0.1691765290.60.0.0',
    '_ga': 'GA1.2.318707848.1691762995',
    'oktaMachineId': 'a9bfa015-4901-4515-1278-c36547b327b0',
    'ziid': '15zw7ab9lhSfEhgKVhb77ecPn6XV6YaKrf0bFHs2x4ZilkhAv-eQe9nttNWvCEeSfmxRs1Rb_1b63EIPEU-adw',
    'zisession': '15zw7ab9lhSfEhgKVhb77ecPn6XV6YaKrf0bFHs2x4ZilkhAv-eQe9nttNWvCEeSfmxRs1Rb_1Z2bbjYyUx5Bw3SGGWHjsOYr_UemRIcb1277KJ3enkLy6bersyAvwk0',
    'ziaccesstoken': 'eyJraWQiOiJMTjFWN2VNSHZtY251LXFPMDZ0aU93ZmZFZFdnY013UFpvenhOVGo0a1RzIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULms0blA1UFV6YkotdXRRQ3BqRzM5M0tkM0hrMGlnR2tLNmJtc0JyMmc3aXcub2FydXN5cmczSXlodG0wZUM2OTYiLCJpc3MiOiJodHRwczovL29rdGEtbG9naW4uem9vbWluZm8uY29tL29hdXRoMi9kZWZhdWx0IiwiYXVkIjoiYXBpOi8vZGVmYXVsdCIsInN1YiI6ImluZm9AY3Jhd2xlci5wcm8udm4iLCJpYXQiOjE2OTE3NjUzMDEsImV4cCI6MTY5MTg1MTcwMSwiY2lkIjoiMG9hOTlkc21ibkF4bGV2RjM2OTYiLCJ1aWQiOiIwMHU2d2N1NzN3ZHZTcUNObDY5NyIsInNjcCI6WyJvZmZsaW5lX2FjY2VzcyIsImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSJdLCJhdXRoX3RpbWUiOjE2OTE3NjUyOTgsImxhc3ROYW1lIjoiQ3Jhd2xlci5wcm8udm4iLCJ6aVNlc3Npb25UeXBlIjotMywiemlHcm91cElkIjowLCJ6aUNvbXBhbnlQcm9maWxlSWQiOiIiLCJ6aVBsYXRmb3JtcyI6WyJDT01NVU5JVFkiXSwiemlVc2VybmFtZSI6ImluZm9AY3Jhd2xlci5wcm8udm4iLCJmaXJzdE5hbWUiOiJJbmZvIiwiemlSb2xlcyI6IkJxUWdSc2c1Z0VFQXdCZ0F3R0VBQUFBQUFBQUFBQUFRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3IiwiemlVdWlkIjoiMGQ3MDhhZjktNzM0Mi00MmE3LTk3ODYtNzcxZjI2MzMyMWE5IiwiemlVc2VySWQiOjMxNjk3NzY5LCJ6aUluYWN0aXZpdHkiOjYwNDgwMCwiemlUZW5hbnRJZCI6MjA2MDU4MDEsImVtYWlsIjoiaW5mb0BjcmF3bGVyLnByby52biIsInNmQWNjb3VudElkIjoiMDAxRG8wMDAwMExlREpQSUEzIiwiemlNb25nb1VzZXJJZCI6IjMxNjk3NzY5In0.FROBX-WGxcCWf9U1UHnzojJ8evuorUWVD5jF35geVJyqfDbjm_qDparRvAbSFlWTvC1_mq4JegDynj1oiZAZy78h_xJmrRqFrOUY0zznqrAXKLHuqZw58DdA3FRLrTzoe3kAgzof9F4jphPWfPHEPrntYGgDXiXTzXnhD-b-eypwhoLwa0kQFWorcDklwiPnXI3e0Zp3mYdHRTmz2OhBQ6yYMddN0VYpSjukMQwMohqCXpvgecqhpQ2AWN_Rszg1D7Ref08HXQMZn1NyPPrs__2pchpSGP_qi0TiA6StMuFWRqgZCd8eT4wZdY_uXoO7j9NZisZF3U_WvV8vAZctrA',
    'parseSessionToken': '1',
    'userId': '31697769',
    'email': 'info%40crawler.pro.vn',
    'name': 'Info%20Crawler.pro.vn',
    'firstname': 'Info',
    'userZoomCompanyId': '20605801',
    'analyticsId': '31697769',
    '__cf_bm': 'f.yfMiGuu1Woe.ODJBvpxIgOTH9sropzGhEC3QiAXiE-1691765305-0-AUO+Ucu3yKyfeAbqLsHjnyeuG1Mtz+nathVDI65xGNGuYWaoyn21jkbPcX771+opWuEty+56ySPVaBuriqteuew=',
    '_cfuvid': 'tNYFYE_4_sauQdLm.yvfJtVuI8SJyOEK2Azbcp4d01I-1691765305140-0-604800000',
    '_ga_PP03JV8JP3': 'GS1.1.1691762995.1.1.1691765306.44.0.0',
    '_dd_s': 'rum=0&expire=1691766685524',
    'amplitude_id_14ff67f4fc837e2a741f025afb61859czoominfo.com': 'eyJkZXZpY2VJZCI6Ijc0ZWI5MGNmLTFhNTktNDNmNS1iYWRjLTY2MTc3OTg2MTk1YlIiLCJ1c2VySWQiOiIzMTY5Nzc2OSIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY5MTc2Mjk5OTEwNywibGFzdEV2ZW50VGltZSI6MTY5MTc2NTc4NTUzNywiZXZlbnRJZCI6MTQzLCJpZGVudGlmeUlkIjo5LCJzZXF1ZW5jZU51bWJlciI6MTUyfQ==',
    'zitokenrefresh': '%7B%22isRefreshInProgress%22%3Afalse%2C%22pendingCallsByAppUUID%22%3A%5B%22FslKqDiHq9OPh7dJhcL8U%22%5D%7D',
}
    headers = {
    'authority': 'app.zoominfo.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://app.zoominfo.com',
    'referer': 'https://app.zoominfo.com/master/dozi-lite/latest/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'session-token': '1',
    'user': '31697769',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-ziaccesstoken': 'eyJraWQiOiJMTjFWN2VNSHZtY251LXFPMDZ0aU93ZmZFZFdnY013UFpvenhOVGo0a1RzIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULms0blA1UFV6YkotdXRRQ3BqRzM5M0tkM0hrMGlnR2tLNmJtc0JyMmc3aXcub2FydXN5cmczSXlodG0wZUM2OTYiLCJpc3MiOiJodHRwczovL29rdGEtbG9naW4uem9vbWluZm8uY29tL29hdXRoMi9kZWZhdWx0IiwiYXVkIjoiYXBpOi8vZGVmYXVsdCIsInN1YiI6ImluZm9AY3Jhd2xlci5wcm8udm4iLCJpYXQiOjE2OTE3NjUzMDEsImV4cCI6MTY5MTg1MTcwMSwiY2lkIjoiMG9hOTlkc21ibkF4bGV2RjM2OTYiLCJ1aWQiOiIwMHU2d2N1NzN3ZHZTcUNObDY5NyIsInNjcCI6WyJvZmZsaW5lX2FjY2VzcyIsImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSJdLCJhdXRoX3RpbWUiOjE2OTE3NjUyOTgsImxhc3ROYW1lIjoiQ3Jhd2xlci5wcm8udm4iLCJ6aVNlc3Npb25UeXBlIjotMywiemlHcm91cElkIjowLCJ6aUNvbXBhbnlQcm9maWxlSWQiOiIiLCJ6aVBsYXRmb3JtcyI6WyJDT01NVU5JVFkiXSwiemlVc2VybmFtZSI6ImluZm9AY3Jhd2xlci5wcm8udm4iLCJmaXJzdE5hbWUiOiJJbmZvIiwiemlSb2xlcyI6IkJxUWdSc2c1Z0VFQXdCZ0F3R0VBQUFBQUFBQUFBQUFRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3IiwiemlVdWlkIjoiMGQ3MDhhZjktNzM0Mi00MmE3LTk3ODYtNzcxZjI2MzMyMWE5IiwiemlVc2VySWQiOjMxNjk3NzY5LCJ6aUluYWN0aXZpdHkiOjYwNDgwMCwiemlUZW5hbnRJZCI6MjA2MDU4MDEsImVtYWlsIjoiaW5mb0BjcmF3bGVyLnByby52biIsInNmQWNjb3VudElkIjoiMDAxRG8wMDAwMExlREpQSUEzIiwiemlNb25nb1VzZXJJZCI6IjMxNjk3NzY5In0.FROBX-WGxcCWf9U1UHnzojJ8evuorUWVD5jF35geVJyqfDbjm_qDparRvAbSFlWTvC1_mq4JegDynj1oiZAZy78h_xJmrRqFrOUY0zznqrAXKLHuqZw58DdA3FRLrTzoe3kAgzof9F4jphPWfPHEPrntYGgDXiXTzXnhD-b-eypwhoLwa0kQFWorcDklwiPnXI3e0Zp3mYdHRTmz2OhBQ6yYMddN0VYpSjukMQwMohqCXpvgecqhpQ2AWN_Rszg1D7Ref08HXQMZn1NyPPrs__2pchpSGP_qi0TiA6StMuFWRqgZCd8eT4wZdY_uXoO7j9NZisZF3U_WvV8vAZctrA',
    'x-ziid': '15zw7ab9lhSfEhgKVhb77ecPn6XV6YaKrf0bFHs2x4ZilkhAv-eQe9nttNWvCEeSfmxRs1Rb_1b63EIPEU-adw',
    'x-zisession': '15zw7ab9lhSfEhgKVhb77ecPn6XV6YaKrf0bFHs2x4ZilkhAv-eQe9nttNWvCEeSfmxRs1Rb_1Z2bbjYyUx5Bw3SGGWHjsOYr_UemRIcb1277KJ3enkLy6bersyAvwk0',
}
    json_data = {'page': 1,'companyPastOrPresent': '1','isCertified': 'include','sortBy': 'Relevance,company_id','sortOrder': 'desc,desc','excludeDefunctCompanies': True,'confidenceScoreMin': 85,'confidenceScoreMax': 99,'outputCurrencyCode': 'USD','inputCurrencyCode': 'USD','excludeNoCompany': 'true','returnOnlyBoardMembers': False,'excludeBoardMembers': True,'sourceId': 'ANURA','companyDesc': 'Tire OR Auto OR Repair OR Body','titleSeniority': 'C_EXECUTIVES,VP_EXECUTIVES,DIRECTOR,MANAGER','employeeSizeMax': '5000','employeeSizeMin': '50','rpp': 25,'doziIndustry': 'consumerservices.auto','departments': 'Human Resources,Operations','buyingCommittee': '{"personas":[],"applyToSearchCriteria":false}','contactRequirements': '','state': 'USA - All','feature': 'People Search - UI'}
    url='https://app.zoominfo.com/anura/zoominfo/hPeopleSearch'
    def start_requests(self):
        yield scrapy.Request(self.url,callback=self.parse,dont_filter=True,method="POST",headers=self.headers,cookies=self.cookies,body=json.dumps(self.json_data),meta={'page':1})
    def parse(self, response):
        page=response.meta['page']
        DATA=json.loads(response.text)
        if 'data' in DATA:
            Data=DATA['data']
        else:
            Data=[]
            print(response.text)
        i=0
        for row in Data:
            i+=1
            item={}
            #item['KEY_']=str(row['companyID'])+'_'+str(row['personID'])+'_'+key_MD5(row['title'])
            item['KEY_']=str(page)+'_'+str(i)
            item['company name']=row.get('companyName','')
            item['Total number of employees']=row.get('companyEmployees','')
            item['company URL']=row.get('website','')
            item['Name']=row['name']
            item['Title']=row['title']
            item['Office phone']=row.get('companyPhone')
            item['Cell phone']=row.get('phone','')
            item['Email address']=row.get('email','')
            if 'location' in row and len(row['location'])>0:
                item['Location']=', '.join(list(row['location'].values()))
            else:
                item['Location']=''
            if item['Cell phone']=='' and item['Email address']=='':
                yield(item)
            else:
                print(item)
                #json_data = {'contacts': [{'personId': row['personID']}],'creditSource': 'GROW'}
                #yield scrapy.Request('https://app.zoominfo.com/anura/userData/viewContacts',callback=self.parse_detail,dont_filter=True,method="POST",headers=self.headers,cookies=self.cookies,body=json.dumps(json_data),meta={'item':item})
        print('PAGE:',page)
        if len(Data)>=25:
            page+=1
            self.json_data['page']=page
            yield scrapy.Request(self.url,callback=self.parse,dont_filter=True,method="POST",headers=self.headers,cookies=self.cookies,body=json.dumps(self.json_data),meta={'page':page})
    def parse_detail(self,response):
        item=response.meta['item']
        Data=json.loads(response.text)['data']
        row=Data[0]
        item['Cell phone']=row.get('phone','')
        item['Email address']=row.get('email','')
        yield(item)