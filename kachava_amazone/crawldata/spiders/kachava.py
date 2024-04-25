import scrapy,json,re
from crawldata.functions import *
from datetime import datetime
from urllib.parse import quote
class CrawlerSpider(scrapy.Spider):
    name = 'kachava'
    conn=None
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    LIST_URL=re.split('\r\n|\n', open('urls.txt').read())
    cookies = {
    'AMCV_7742037254C95E840A4C98A6^%^40AdobeOrg': '1585540135^%^7CMCIDTS^%^7C19447^%^7CMCMID^%^7C72333469891479947072269211402419859665^%^7CMCAAMLH-1679918792^%^7C3^%^7CMCAAMB-1680193960^%^7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y^%^7CMCOPTOUT-1680201521s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CMCSYNCSOP^%^7C411-19444^%^7CvVersion^%^7C4.4.0',
    'aws-target-visitor-id': '1675531286674-998665.38_0',
    'aws-target-data': '^%^7B^%^22support^%^22^%^3A^%^221^%^22^%^7D',
    'regStatus': 'registered',
    'aws-ubid-main': '387-2054355-0261632',
    'aws-account-alias': '637307937437',
    'remember-account': 'true',
    'aws-userInfo': '^%^7B^%^22arn^%^22^%^3A^%^22arn^%^3Aaws^%^3Aiam^%^3A^%^3A637307937437^%^3Auser^%^2Fbradford^%^22^%^2C^%^22alias^%^22^%^3A^%^22637307937437^%^22^%^2C^%^22username^%^22^%^3A^%^22bradford^%^22^%^2C^%^22keybase^%^22^%^3A^%^22vOLOSdbWDezGUVUrpdAMzgrjhZIF^%^2B9^%^2B1JBDulcMT5yI^%^5Cu003d^%^22^%^2C^%^22issuer^%^22^%^3A^%^22http^%^3A^%^2F^%^2Fsignin.aws.amazon.com^%^2Fsignin^%^22^%^2C^%^22signinType^%^22^%^3A^%^22PUBLIC^%^22^%^7D',
    'noflush_awsccs_sid': '6d42d3648ae3db48573444a3eecb161194b96980deae5aed0a9df8687e94c412',
    'session-id': '137-6234446-2738147',
    'session-id-time': '2082787201l',
    'csm-hit': 'tb:PTXFS9ASFJEQBZ6WJNVE+b-YV6BMFK12VB0CJVZNART^|1681185587149&t:1681185587149&adb:adblk_no',
    'ubid-main': '135-1554616-4456761',
    'ubid-acbus': '130-0581998-9148118',
    's_pers': '^%^20s_fid^%^3D2DE5C565C5EED9BA-364E9756235D82BB^%^7C1838176694066^%^3B^%^20s_dl^%^3D1^%^7C1680325694066^%^3B^%^20gpv_page^%^3DUS^%^253ASD^%^253ASOA-home^%^7C1680325694068^%^3B^%^20s_ev15^%^3D^%^255B^%^255B^%^2527AZFSSOA^%^2527^%^252C^%^25271680323894097^%^2527^%^255D^%^255D^%^7C1838176694097^%^3B',
    'sst-main': 'Sst1^|PQFZFQvZQsaXH3-mZGD_Fp3uCdDcvWGPYyQFitINt4Z4x7GJAH8QDPrUGQAl-LBZHJR9COtF8tPGChbQKLECdGnNCPBJpc6mBsaoCdv0rk60cBS5ai_9Cgr2jNE4dXoN36zsYWYtz-jGbidludkf4f21APoz2C7V7Hb9-xvPwLfW2JL6_3BMf9-X7972RtcSVpA9n9gcE1cN2_jJZ3TrlaF7fRlyZbql-x_ThOJgZiJE0RLBILJrLY9szwXol5h54f0FpIbOMGPgHA-puuWgVnDfYE66AkbLVXIGkTrbq1vK3Xk',
    'aws-signer-token_us-east-1': 'eyJrZXlWZXJzaW9uIjoidnV5djkuU2VXMFpNdnFxbUJlXy52bkdRbW03bUUyTjUiLCJ2YWx1ZSI6InJaRmg1OFdqQVZydnFmTDVTTjU0enhSd2tFeXdKVEs4WWR4SjNhMEZ0aGM9IiwidmVyc2lvbiI6MX0=',
    'x-amz-captcha-1': '1681152867140425',
    'x-amz-captcha-2': 'VvQAYL/CrZlkv9TZ7js/qg==',
    'aws-userInfo-signed': 'eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJhcC1zb3V0aGVhc3QtMiIsImFsZyI6IkVTMzg0Iiwia2lkIjoiMDZiN2EwMGUtMmI2My00NGNiLWIyMzEtOGFlOWFhMmEyOTllIn0.eyJzdWIiOiI2MzczMDc5Mzc0MzciLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoidk9MT1NkYldEZXpHVVZVcnBkQU16Z3JqaFpJRis5KzFKQkR1bGNNVDV5ST0iLCJhcm4iOiJhcm46YXdzOmlhbTo6NjM3MzA3OTM3NDM3OnVzZXJcL2JyYWRmb3JkIiwidXNlcm5hbWUiOiJicmFkZm9yZCJ9.Tv0ZSVSZ8jUg-HIBYA2ebNWvDmOYtbdIY28Kn7XRu23A0gGXWCAmlKoeu1Qppepyzvi9-9FaPWri2J_IGyO7FltBoyYRKyuX93XvwFGDnGLi7vAdJ2AOCK3pOxoTQVBY',
    'session-token': 'sZzwW5zZV/HFIpOQQjkOoSAN9Ti8EptM6vNRmkizkmAwng2bNemES1/bPL/hO8Rtk1wMr+vgUMMVGvALIRb5v5+9HiYQ0zfAOVGyu67sdbVXDSuZwx8P/klYgrplmqiLGOEXXiME7CFG1r8rC14dSs5uI/FQ2UYSaAUyRJ2c1+LH8SnZPqwWXnuvjmhXGyuyzLM+UzbicbwwbGawHjGyvqrzysSUFIeZg4828XODt88jJ+dcUnGNKJrAk6HlMJ5p',
    'lc-main': 'en_US',
    'x-main': 'rvVgBRobJUkV3rsz8h8CRQullFbfJacx33z0HJaggqjX2joZwa0oOE9TIZwj2Ahm',
    'at-main': 'Atza^|IwEBIHECwJ6ldZlmuNaXJSdK-8QZvx7rlivrGTfeqV8XTa_DjtQ7hV-UnF-W2LuGZTkht-3ytJd0OCa02nyw-1OS3a55LPm0nPWozPbQQU35tsY4kIb-8cf7VHFrBhpjkquvTTpxo3V0RJm3_7Q9_FCuI6pJRxXE8oxcoEqbzctoe-gNN_RGCztkSh--L2xiMI9ZS7xCZjzRlsD1HB7ovUF35zrZ',
    'sess-at-main': '91bNyIaoqi+4y8O/39I2Wyg9o8PPsD7AR3MJmf75mWI=',
    'i18n-prefs': 'USD',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # 'Cookie': 'AMCV_7742037254C95E840A4C98A6^%^40AdobeOrg=1585540135^%^7CMCIDTS^%^7C19447^%^7CMCMID^%^7C72333469891479947072269211402419859665^%^7CMCAAMLH-1679918792^%^7C3^%^7CMCAAMB-1680193960^%^7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y^%^7CMCOPTOUT-1680201521s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CMCSYNCSOP^%^7C411-19444^%^7CvVersion^%^7C4.4.0; aws-target-visitor-id=1675531286674-998665.38_0; aws-target-data=^%^7B^%^22support^%^22^%^3A^%^221^%^22^%^7D; regStatus=registered; aws-ubid-main=387-2054355-0261632; aws-account-alias=637307937437; remember-account=true; aws-userInfo=^%^7B^%^22arn^%^22^%^3A^%^22arn^%^3Aaws^%^3Aiam^%^3A^%^3A637307937437^%^3Auser^%^2Fbradford^%^22^%^2C^%^22alias^%^22^%^3A^%^22637307937437^%^22^%^2C^%^22username^%^22^%^3A^%^22bradford^%^22^%^2C^%^22keybase^%^22^%^3A^%^22vOLOSdbWDezGUVUrpdAMzgrjhZIF^%^2B9^%^2B1JBDulcMT5yI^%^5Cu003d^%^22^%^2C^%^22issuer^%^22^%^3A^%^22http^%^3A^%^2F^%^2Fsignin.aws.amazon.com^%^2Fsignin^%^22^%^2C^%^22signinType^%^22^%^3A^%^22PUBLIC^%^22^%^7D; noflush_awsccs_sid=6d42d3648ae3db48573444a3eecb161194b96980deae5aed0a9df8687e94c412; session-id=137-6234446-2738147; session-id-time=2082787201l; csm-hit=tb:PTXFS9ASFJEQBZ6WJNVE+b-YV6BMFK12VB0CJVZNART^|1681185587149&t:1681185587149&adb:adblk_no; ubid-main=135-1554616-4456761; ubid-acbus=130-0581998-9148118; s_pers=^%^20s_fid^%^3D2DE5C565C5EED9BA-364E9756235D82BB^%^7C1838176694066^%^3B^%^20s_dl^%^3D1^%^7C1680325694066^%^3B^%^20gpv_page^%^3DUS^%^253ASD^%^253ASOA-home^%^7C1680325694068^%^3B^%^20s_ev15^%^3D^%^255B^%^255B^%^2527AZFSSOA^%^2527^%^252C^%^25271680323894097^%^2527^%^255D^%^255D^%^7C1838176694097^%^3B; sst-main=Sst1^|PQFZFQvZQsaXH3-mZGD_Fp3uCdDcvWGPYyQFitINt4Z4x7GJAH8QDPrUGQAl-LBZHJR9COtF8tPGChbQKLECdGnNCPBJpc6mBsaoCdv0rk60cBS5ai_9Cgr2jNE4dXoN36zsYWYtz-jGbidludkf4f21APoz2C7V7Hb9-xvPwLfW2JL6_3BMf9-X7972RtcSVpA9n9gcE1cN2_jJZ3TrlaF7fRlyZbql-x_ThOJgZiJE0RLBILJrLY9szwXol5h54f0FpIbOMGPgHA-puuWgVnDfYE66AkbLVXIGkTrbq1vK3Xk; aws-signer-token_us-east-1=eyJrZXlWZXJzaW9uIjoidnV5djkuU2VXMFpNdnFxbUJlXy52bkdRbW03bUUyTjUiLCJ2YWx1ZSI6InJaRmg1OFdqQVZydnFmTDVTTjU0enhSd2tFeXdKVEs4WWR4SjNhMEZ0aGM9IiwidmVyc2lvbiI6MX0=; x-amz-captcha-1=1681152867140425; x-amz-captcha-2=VvQAYL/CrZlkv9TZ7js/qg==; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJhcC1zb3V0aGVhc3QtMiIsImFsZyI6IkVTMzg0Iiwia2lkIjoiMDZiN2EwMGUtMmI2My00NGNiLWIyMzEtOGFlOWFhMmEyOTllIn0.eyJzdWIiOiI2MzczMDc5Mzc0MzciLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoidk9MT1NkYldEZXpHVVZVcnBkQU16Z3JqaFpJRis5KzFKQkR1bGNNVDV5ST0iLCJhcm4iOiJhcm46YXdzOmlhbTo6NjM3MzA3OTM3NDM3OnVzZXJcL2JyYWRmb3JkIiwidXNlcm5hbWUiOiJicmFkZm9yZCJ9.Tv0ZSVSZ8jUg-HIBYA2ebNWvDmOYtbdIY28Kn7XRu23A0gGXWCAmlKoeu1Qppepyzvi9-9FaPWri2J_IGyO7FltBoyYRKyuX93XvwFGDnGLi7vAdJ2AOCK3pOxoTQVBY; session-token=sZzwW5zZV/HFIpOQQjkOoSAN9Ti8EptM6vNRmkizkmAwng2bNemES1/bPL/hO8Rtk1wMr+vgUMMVGvALIRb5v5+9HiYQ0zfAOVGyu67sdbVXDSuZwx8P/klYgrplmqiLGOEXXiME7CFG1r8rC14dSs5uI/FQ2UYSaAUyRJ2c1+LH8SnZPqwWXnuvjmhXGyuyzLM+UzbicbwwbGawHjGyvqrzysSUFIeZg4828XODt88jJ+dcUnGNKJrAk6HlMJ5p; lc-main=en_US; x-main=rvVgBRobJUkV3rsz8h8CRQullFbfJacx33z0HJaggqjX2joZwa0oOE9TIZwj2Ahm; at-main=Atza^|IwEBIHECwJ6ldZlmuNaXJSdK-8QZvx7rlivrGTfeqV8XTa_DjtQ7hV-UnF-W2LuGZTkht-3ytJd0OCa02nyw-1OS3a55LPm0nPWozPbQQU35tsY4kIb-8cf7VHFrBhpjkquvTTpxo3V0RJm3_7Q9_FCuI6pJRxXE8oxcoEqbzctoe-gNN_RGCztkSh--L2xiMI9ZS7xCZjzRlsD1HB7ovUF35zrZ; sess-at-main=91bNyIaoqi+4y8O/39I2Wyg9o8PPsD7AR3MJmf75mWI=; i18n-prefs=USD',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


    domain='https://www.amazon.com'
    def start_requests(self):
        for KEYWORD in self.LIST_URL:
            if not KEYWORD.startswith('#'):
                yield scrapy.Request('https://www.amazon.com/s?k='+KEYWORD+'&page=1',callback=self.parse,meta={'KEYWORD':KEYWORD},headers=self.headers,cookies=self.cookies,dont_filter=True)
    def parse(self, response):
        KEYWORD=response.meta['KEYWORD']
        if not '/ap/signin' in response.url:
            Data=response.xpath('//div[contains(@class,"s-main-slot")]//div[@data-component-type="s-search-result"]')
            for row in Data:
                item={}
                item['KEYWORD']=KEYWORD
                item['KEY_']=row.xpath('./@data-asin').get()
                item['Product_name']=row.xpath('.//h2//text()').get()
                item['Product_url']=self.domain+row.xpath('.//h2/a/@href').get()
                if str(KEYWORD).lower() in str(item['Product_name']).lower():
                    url='https://www.amazon.com/Product/dp/'+item['KEY_']
                    headers=self.headers
                    headers['referer']=url
                    yield scrapy.Request(url,callback=self.parse_product,headers=headers,cookies=self.cookies,meta={'item':item,'Level':0},dont_filter=True)
            next_page=response.xpath('//a[contains(@class,"s-pagination-next")]/@href').get()
            if next_page:
                url=self.domain+next_page
                yield scrapy.Request(url,callback=self.parse,meta={'KEYWORD':KEYWORD},headers=self.headers)
        else:
            yield scrapy.Request('https://www.amazon.com/s?k='+KEYWORD+'&page=1',callback=self.parse,meta={'KEYWORD':KEYWORD},headers=self.headers,cookies=self.cookies,dont_filter=True)
    def parse_product(self,response):
        item=response.meta['item']
        Level=response.meta['Level']
        if not '/ap/signin' in response.url:
            CATES=response.xpath('//div[@data-feature-name="wayfinding-breadcrumbs"]//li//text()').getall()
            CATE=[]
            for Cat in CATES:
                Cat=str(Cat).strip()
                if Cat!='':
                    CATE.append(Cat)
            if len(CATE)>0 or Level>=5:
                item['Category']=' '.join(CATE)
                Data=response.xpath('//table[contains(@class,"a-spacing-micro")]//tr')
                for row in Data:
                    TITLE=row.xpath('.//span[contains(@class,"a-text-bold")]/text()').get()
                    VAL=row.xpath('.//span[contains(@class,"po-break-word")]/text()').get()
                    if TITLE:
                        TITLE=str(TITLE).strip()
                        if TITLE!='' and not TITLE in item:
                            item[Get_Key_String(TITLE)]=str(VAL).strip()
                Data=response.xpath('//div[@id="detailBullets_feature_div"]//li/span')
                for row in Data:
                    TITLE=row.xpath('./span[@class]/text()').get()
                    VAL=row.xpath('./span[not(@class)]/text()').get()
                    if TITLE:
                        TITLE=re.split('\r\n|\n', TITLE)[0]
                        TITLE=str(TITLE).strip()
                        if TITLE!='' and not TITLE in item:
                            item[Get_Key_String(TITLE)]=str(VAL).strip()
                Data=response.xpath('//table[contains(@id,"productDetails")]//tr')
                for row in Data:
                    TITLE=row.xpath('./th/text()').get()
                    VAL=row.xpath('./td/text()').get()
                    if TITLE:
                        TITLE=str(TITLE).strip()
                        if TITLE!='' and not TITLE in item:
                            item[Get_Key_String(TITLE)]=str(VAL).strip()
                Product={}
                Product['SHEET']=self.name
                Product['KEY_']=item['KEY_']
                Product['Brand']=item['KEYWORD']
                Product['ASIN']=item['KEY_']
                if not item['Product_name'] is None and len(str(item['Product_name']))>1:
                    Product['Title']=item['Product_name']
                else:
                    Product['Title']=response.xpath('//h1/span[@id="productTitle"]/text()').get()
                Product['Category']=item['Category']
                Product['Manufacturer']=item.get('Manufacturer','')
                Product['UPC']=item.get('UPC','')
                Product['Item_model_number']=item.get('Item_model_number','')
                Product['Product_Dimensions']=''
                if 'Product_Dimensions' in item:
                    Product['Product_Dimensions']=item['Product_Dimensions']
                elif 'Package_Dimensions' in item:
                    Product['Product_Dimensions']=item['Package_Dimensions']
                Product['Is_Discontinued_By_Manufacturer']=item.get('Is_Discontinued_By_Manufacturer','')
                REVIEWS=response.xpath('//div[@data-hook="review"]')
                if len(REVIEWS)>0:
                    url='https://www.amazon.com/product-reviews/'+Product['ASIN']+'/ref=cm_cr_dp_d_show_all_btm?reviewerType=all_reviews&pageNumber=1'
                    yield scrapy.Request(url,callback=self.parse_reviews,meta={'Product':Product,'page':1},headers=self.headers,cookies=self.cookies,dont_filter=True)
                else:
                    Product['Retailer_Name']=''
                    Product['Title']=''
                    Product['Review_Star']=''
                    Product['Is_Verified']=''
                    Product['Review_Date']=''
                    Product['Has_Response']=''
                    Product['Review_Text']=''
                    Product['Review_URL']=''
                    yield(Product)
            elif Level<5:
                Level+=1
                print('\n ----------------')
                print('Re-Crawl',Level,response.url)
                url='https://www.amazon.com/Product/dp/'+item['KEY_']
                headers=self.headers
                headers['referer']=url
                yield scrapy.Request(url,callback=self.parse_product,headers=headers,cookies=self.cookies,meta={'item':item,'Level':Level},dont_filter=True)
            else:
                print('\a')
                print('\n ==========================')
                print(response.url)
        else:
            url='https://www.amazon.com/Product/dp/'+item['KEY_']
            headers=self.headers
            headers['referer']=url
            yield scrapy.Request(url,callback=self.parse_product,headers=headers,cookies=self.cookies,meta={'item':item,'Level':0},dont_filter=True)

    def parse_reviews(self,response):
        Product=response.meta['Product']
        page=response.meta['page']
        if not '/ap/signin' in response.url:
            Data=response.xpath('//div[@data-hook="review"]')
            for row in Data:
                item={}
                item.update(Product)
                item['Retailer_Name']=row.xpath('.//span[@class="a-profile-name"]/text()').get()
                item['Review_Title']=row.xpath('.//a[@data-hook="review-title"]/span/text()').get()
                item['Review_Star']=''
                Star=row.xpath('.//i[@data-hook="review-star-rating"]//text()').get()
                if Star:
                    item['Review_Star']=str(Star).split()[0]
                item['Is_Verified']=row.xpath('.//span[@data-hook="avp-badge"]/text()').get()
                item['Review_Date']=''
                RvDate=row.xpath('.//span[@data-hook="review-date"]/text()').get()
                if RvDate and ' on ' in RvDate:
                    item['Review_Date']=str(RvDate).split(' on ')[1]
                item['Has_Response']=''
                item['Review_Text']=cleanhtml(row.xpath('.//span[@data-hook="review-body"]').get())
                try:
                    item['Review_URL']=self.domain + row.xpath('.//a[@data-hook="review-title"]/@href').get()
                except:
                    item['Review_URL']=''
                yield(item)
            next_page=response.xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').get()
            print('\n *****************')
            print(next_page)
            if len(Data)>0:
                page+=1
                url='https://www.amazon.com/product-reviews/'+Product['ASIN']+'/ref=cm_cr_dp_d_show_all_btm?reviewerType=all_reviews&pageNumber='+str(page)
                yield scrapy.Request(url,callback=self.parse_reviews,meta={'Product':Product,'page':page},headers=self.headers,cookies=self.cookies,dont_filter=True)
        else:
            url='https://www.amazon.com/product-reviews/'+Product['ASIN']+'/ref=cm_cr_dp_d_show_all_btm?reviewerType=all_reviews&pageNumber='+str(page)
            yield scrapy.Request(url,callback=self.parse_reviews,meta={'Product':Product,'page':page},headers=self.headers,cookies=self.cookies,dont_filter=True)

        

        
