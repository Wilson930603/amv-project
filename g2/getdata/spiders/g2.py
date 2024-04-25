# -*- coding: utf-8 -*-
import scrapy,re,requests
class RunSpider(scrapy.Spider):
    name = 'g2'
    start_urls=['https://www.google.com/']
    # Get from google chrome
    cookies = {
    'cf_clearance': '2CK8vR1e0WPaE.GHdb_0jCFR2gDw.vx7cj2l7HpNWQ8-1688610563-0-250',
    'osano_consentmanager_uuid': 'feaa72f3-69a5-4e38-993b-799b6d767674',
    'osano_consentmanager': 'y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==',
    '_sp_id.6c8b': 'dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.2.1688610601.1686710063.ce6267c6-005e-4599-8202-295ad3c602c1.f96c8798-f8fb-46c6-84bc-2834ac11307f.2ccbba2a-facd-45e2-863b-ebc6a0d84961.1688610583659.4',
    '_ga_MFZ5NDXZ5F': 'GS1.1.1688610583.2.0.1688610583.60.0.0',
    '_ga': 'GA1.2.1170638361.1686710004',
    'sp': 'f7c087c9-ba10-46ee-b441-2ae005dea18d',
    '_delighted_web': '{^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}}}',
    '__cf_bm': '45e2AhqbZcQexK3cbb7Vf_k0sXjjqRPziETcZTRir7M-1688610583-0-AeyWGMkfwOmlYTpKo011E8AqVSQUi8av+AjphhJP/9GMJ6V6gLtNm49/zyNwYW5klagi8BcYfrmygANhXvZXeNqnCzMySfhRHzTvKnPQUETD',
    'cf_chl_2': 'f25156126dac2a8',
    'cf_chl_rc_i': '1',
    'AWSALB': '5XleJUNRB+kZUv47JQxmNmi/f3Rn3kWoxr5b2yF4UxvhXxu4AlbvHLiepSOVykUWThJx7TZxez883uiA5Fh/lyF74/9+B7veW/IuMcomigMLybCoSrD6olCKkjcD',
    'AWSALBCORS': '5XleJUNRB+kZUv47JQxmNmi/f3Rn3kWoxr5b2yF4UxvhXxu4AlbvHLiepSOVykUWThJx7TZxez883uiA5Fh/lyF74/9+B7veW/IuMcomigMLybCoSrD6olCKkjcD',
    'events_distinct_id': '8959f2ca-b00a-4c81-bc36-a2d602dbfe73',
    'amplitude_session': '1688610581915',
    '_g2_session_id': 'ad1e31f3661c02c12d7c3c924b851b01',
    '_sp_ses.6c8b': '*',
    '_gid': 'GA1.2.2049621159.1688610585',
    '_gat': '1',
    '_gat_t1': '1',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # 'Cookie': 'cf_clearance=2CK8vR1e0WPaE.GHdb_0jCFR2gDw.vx7cj2l7HpNWQ8-1688610563-0-250; osano_consentmanager_uuid=feaa72f3-69a5-4e38-993b-799b6d767674; osano_consentmanager=y5Ca2R3gGd_MxtoHVKwyp8hB_r3CPdVZbui3ARg9E1tgI9AXr5fsJwXZ0H84cAU1hVFhU6JQUjyYLW0UKraXyru094VXvPFIgjknePMd6lvtDajAUabDJlNJVxexywnfnPRKvcLSqn-fdA4kyrqYdh15IBBntbDXLVu2K6F2r2D3CHR0quZghDx2lKdKJHPuCpss8JC-tpJKD96yAn46NUjoKD-h10hCOPljcwkjPOcfjpcw6tXFd1r2TKIrxfAE8cf6gCGmYI2ehEXOPfh_eF55DXo-7t7fFIIFIA==; _sp_id.6c8b=dd3153a6-ad5d-4a2a-adad-3327618ec1a3.1686710004.2.1688610601.1686710063.ce6267c6-005e-4599-8202-295ad3c602c1.f96c8798-f8fb-46c6-84bc-2834ac11307f.2ccbba2a-facd-45e2-863b-ebc6a0d84961.1688610583659.4; _ga_MFZ5NDXZ5F=GS1.1.1688610583.2.0.1688610583.60.0.0; _ga=GA1.2.1170638361.1686710004; sp=f7c087c9-ba10-46ee-b441-2ae005dea18d; _delighted_web={^%^22h7nzI49oCCJbJbS4^%^22:{^%^22_delighted_fst^%^22:{^%^22t^%^22:^%^221686710024640^%^22}}}; __cf_bm=45e2AhqbZcQexK3cbb7Vf_k0sXjjqRPziETcZTRir7M-1688610583-0-AeyWGMkfwOmlYTpKo011E8AqVSQUi8av+AjphhJP/9GMJ6V6gLtNm49/zyNwYW5klagi8BcYfrmygANhXvZXeNqnCzMySfhRHzTvKnPQUETD; cf_chl_2=f25156126dac2a8; cf_chl_rc_i=1; AWSALB=5XleJUNRB+kZUv47JQxmNmi/f3Rn3kWoxr5b2yF4UxvhXxu4AlbvHLiepSOVykUWThJx7TZxez883uiA5Fh/lyF74/9+B7veW/IuMcomigMLybCoSrD6olCKkjcD; AWSALBCORS=5XleJUNRB+kZUv47JQxmNmi/f3Rn3kWoxr5b2yF4UxvhXxu4AlbvHLiepSOVykUWThJx7TZxez883uiA5Fh/lyF74/9+B7veW/IuMcomigMLybCoSrD6olCKkjcD; events_distinct_id=8959f2ca-b00a-4c81-bc36-a2d602dbfe73; amplitude_session=1688610581915; _g2_session_id=ad1e31f3661c02c12d7c3c924b851b01; _sp_ses.6c8b=*; _gid=GA1.2.2049621159.1688610585; _gat=1; _gat_t1=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

    def parse(self,response):
        f=open('urls.txt','r')
        LIST=re.split("\r\n|\n",f.read())
        f.close()
        for URL in LIST:
            RUN=True
            Page=1
            if not str(URL).startswith('#'):
                if '~' in URL:
                    urls=str(URL).split('~')
                    Product=urls[0]
                    url_crawl=urls[1]
                else:
                    url_crawl=URL
                    Product=''
                while RUN:
                    url=str(url_crawl).split('#')[0]+'?page='+str(Page)
                    print('\n ------------')
                    print(url)
                    self.headers['referer']=url
                    res=requests.get(url,headers=self.headers,cookies=self.cookies)
                    response=scrapy.Selector(text=res.text)
                    if Page==1:
                        ITEM={}
                        ITEM['SHEET']='Websites'
                        ITEM['Websites']=url
                        try:
                            ITEM['G2 # Reviews']=self.Get_Number(str(response.xpath('//li[@class="list--piped__li"]/a/text()').get()).split()[0]) #header
                        except:
                            ITEM['G2 # Reviews']=self.Get_Number(response.xpath('//div[contains(@class,"filter-summary")]/div/strong/text()').get())
                        yield(ITEM)
                    Data=response.xpath('//div[@id="reviews"]//div[contains(@class,"paper paper--white paper--box mb-2 position-relative border-bottom")]')
                    for row in Data:
                        item={}
                        item['SHEET']='Reviews'
                        if Product=='':
                            item['Product']=response.xpath('//div[@itemprop="name"]/a/text()').get()
                        else:    
                            item['Product']=Product
                        item['Name']=row.xpath('.//span[@itemprop="author"]//text()').get()
                        item['Title']=''
                        item['Company']=''
                        item['Size']=''
                        DT=row.xpath('.//div[@class="c-midnight-80 line-height-h6 fw-regular"]/div')
                        if len(DT)>0:
                            item['Size']=self.cleanhtml(DT[len(DT)-1].xpath('.').get())
                        if len(DT)>1:
                            item['Title']=self.cleanhtml(DT[0].xpath('.').get())
                        if len(DT)>2:
                            item['Company']=self.cleanhtml(DT[1].xpath('.').get())
                        Star=row.xpath('.//div[contains(@class,"stars large xlarge--medium-down")]/@class').get()
                        Star=str(Star).split('stars-')[1]
                        item['Stars']=round(int(Star)/2,1)
                        item['Date']=row.xpath('.//time/@datetime').get()
                        item['Review Title']=str(row.xpath('.//h3[@itemprop="name"]/text()').get()).strip()
                        DT=row.xpath('.//div[@itemprop="reviewBody" and not(@data-poison-text)]/div')
                        for rs in DT:
                            TXT=self.cleanhtml(str(rs.xpath('./div').get()).replace('</p>','</p>\n'))
                            item[str(rs.xpath('./h5/text()').get()).strip()]=TXT
                        item['URL From Review Title']=row.xpath('.//a[@class="pjax"]/@href').get()
                        BUTTON=row.xpath('.//div[@class="tags--teal"]/div')
                        VER=[]
                        for rs in BUTTON:
                            txt=str(rs.xpath('.//text()').get()).strip()
                            VER.append(txt)
                        item['Verified buttons']='; '.join(VER)
                        yield(item)
                    next_page=response.xpath('//li/a[contains(text(),"Next")]')
                    if next_page:
                        Page+=1
                    else:
                        RUN=False
    def Get_Number(self,xau):
        KQ=re.sub(r"([^0-9.])","", str(xau).strip())
        return KQ
    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    def kill_space(self,xau):
        xau=str(xau).replace('\t','').replace('\r','').replace('\n',', ')
        xau=(' '.join(xau.split())).strip()
        return xau
        