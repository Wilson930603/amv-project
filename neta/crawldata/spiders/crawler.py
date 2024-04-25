import scrapy,json,re
from crawldata.functions import *
from datetime import datetime

class CrawlerSpider(scrapy.Spider):
    name = 'neta'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-GB,en;q=0.5','Content-Type': 'application/x-www-form-urlencoded','Origin': 'https://neta.netaworld.org','Connection': 'keep-alive','Referer': 'https://neta.netaworld.org/netassa/censsacustlkup.query_page','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'same-origin','Sec-Fetch-User': '?1'}
    url='https://neta.netaworld.org/netassa/censsacustlkup.result_page'
    def start_requests(self):
        url='https://neta.netaworld.org/netassa/censsacustlkup.query_page'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        STATES=response.xpath('//select[@name="p_state_cd"]/option/@value').getall()
        for State in STATES:
            if not '%' in State:
                data = {'p_cust_id': '','p_debug_fl': '','p_subclass_cd': '','p_first_nm': '','p_last_nm': '','p_company_nm': '','p_city_nm': '','p_state_cd': State,'p_postal_cd': '','p_distance': '%null%','p_country_cd': 'USA','p_email': '','p_keyword': '','p_configured_parm1_ty': '','p_configured_parm1': '','p_configured_parm2_ty': '','p_configured_parm2': '','p_configured_parm3_ty': '','p_configured_parm3': '','p_configured_parm4_ty': '','p_configured_parm4': '','p_configured_parm5_ty': '','p_configured_parm5': '','p_configured_parm6_ty': '','p_configured_parm6': '','p_configured_parm7_ty': '','p_configured_parm7': '','p_configured_parm8_ty': '','p_configured_parm8': '','p_configured_parm9_ty': '','p_configured_parm9': '','p_configured_parm10_ty': '','p_configured_parm10': '','p_recs_per_page': '50','p_partial_match_fl': 'Y','p_match_on': 'ALL','SubmitButton': 'Query'}
                yield scrapy.FormRequest(self.url,callback=self.parse_data,formdata=data,headers=self.headers,meta={'State':State})
    def parse_data(self,response):
        State=response.meta['State']
        Data=response.xpath('//table[@class="aaCenssacustlkupCustTbl"]')
        for Table in Data:
            datarow=Table.xpath('.//tr')
            item={}
            for row in datarow:
                TITLE=row.xpath('./td[1]/text()').get()
                VALUE=row.xpath('./td[2]//text()').getall()
                VALUES=[]
                for rs in VALUE:
                    rs=str(rs).strip()
                    if rs!='':
                        VALUES.append(rs)
                if 'Company Name' in TITLE:
                    item['Company Name']=VALUES[0]
                if 'Address' in TITLE:
                    item['Address']=', '.join(VALUES)
                if 'Phone' in TITLE:
                    for rs in VALUES:
                        TYPES=(str(rs).split('(')[-1])
                        TYPE=str(TYPES).title().replace(' ','_').replace('(','').replace(')','')
                        if 'Phone' in TYPE:
                            i=1
                            while TYPE+'_'+str(i) in item:
                                i+=1
                            item[TYPE+'_'+str(i)]=(str(rs).split('('+TYPES)[0]).strip()
                        else:
                            item[TYPE]=(str(rs).split('('+TYPES)[0]).strip()
                if 'Email' in TITLE or 'Website' in TITLE:
                    EMIALS=[]
                    WEBSITES=[]
                    for rs in VALUES:
                        if '@' in rs:
                            EMIALS.append(rs)
                        if 'http' in rs or 'www' in rs:
                            WEBSITES.append(rs)
                    item['Email']=', '.join(EMIALS)
                    item['Website']=', '.join(WEBSITES)
            item['KEY_']=key_MD5(str(item))
            yield(item)