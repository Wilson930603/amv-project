import scrapy,re,json,os,requests,time
from crawldata.functions import *
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from crawldata.settings import GLASSDOOR_USER,GLASSDOOR_PASSWORD
class CrawlerSpider(scrapy.Spider):
    name = 'glassdoor_reviews'
    start_urls=['http://httpbin.org/ip']
    IDS=[]
    RUN=None
    CRAWLED=[]
    cookies = {'gdId': 'dd21d13b-9a0b-420f-ad00-bbcac501d232','trs': 'direct:direct:direct:2022-08-15+04%3A46%3A07.271:undefined:undefined','optimizelyEndUserId': 'oeu1660563969690r0.7528168008341631','_ga_RC95PMVB3H': 'GS1.1.1666401410.49.0.1666401410.60.0.0','_ga': 'GA1.2.1080828764.1660563971','_ga_RJF0GNZNXE': 'GS1.1.1666401410.51.0.1666401410.60.0.0','OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Dec+07+2022+18%3A03%3A26+GMT%2B0700+(Indochina+Time)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=f1ad896b-5a74-40bf-b187-e93ddbd007d7&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false','_optionalConsent': 'true','_rdt_uuid': '1660563972243.160606b6-98a1-49fe-8ced-348708592023','__pdst': '9c410293da4144e68c92c3df6ce4424f','_tt_enable_cookie': '1','_ttp': 'c96ca690-5f2e-4d4a-8f16-4ab4aa78fb6e','amp_a46b8b': '1CHCuLtYIF6ZXpHC9uAEf-.MjAxODE3MjA1..1gdi6fm1t.1gdi6jk3s.48.3k.7s','_pin_unauth': 'dWlkPU9HSTBZV1UxWXprdFpHUmxOQzAwTVdNeUxUbG1Nall0TXprMU5UaGlZVGxqTVRZdw','_fbp': 'fb.1.1660563975071.1661300353','__gads': 'ID=78680b1cbbbf5967-226ff9b598d50003:T=1660563974:S=ALNI_MbPSh55ZGjjYPCO-vf5fGNb1xl9mA','__gpi': 'UID=000008a27b184216:T=1660563974:RT=1670404214:S=ALNI_MaPxVrkjwXAfryySrPqq-p8middxA','ki_t': '1660563977884%3B1670411002300%3B1670411010090%3B42%3B587','ki_r': '','G_ENABLED_IDPS': 'google','ki_u': '39b3f4e3-5233-baf0-60d8-377c','ki_s': '200550%3A0.0.0.0.0%3B213982%3A0.0.0.0.0%3B213985%3A0.0.0.0.0%3B218147%3A1.0.0.0.2%3B220996%3A5.0.0.0.2%3B221866%3A8.0.0.1.2','uc': '8013A8318C98C517A1E3210FFD1F05F398C9D2152F0180DC768A742F3472FB8F427D6A68FB38F2B1B28726BCFCF3A5954B227C87A60D51481D1C99ABCCBA75AD66D19FE28C0B9437C4766BD65F74E0B46F6E94CF18AD31214A49501A582048A16FE6B0F83C6B85B3C9FFCD329729BBAA9F99A0D3FE413F66C05C4B1C4BD73D458FA62D117D89E5FA78073142BB7E0B2B','indeedCtk': '1gf52i3r8klue801','__ssid': '0a8acb351d281c10c620a288c56363a','amp_bfd0a9': 'Agxe0RnZH4zv2FhCIK-exg.MjAxODE3MjA1..1gjm4250l.1gjm42bv3.hf.k.i3','g_state': '{"i_p":1668045731155,"i_l":2}','_mkto_trk': 'id:899-LOT-464&token:_mch-glassdoor.com-1665544065924-80651','_clck': 'jkevrs|1|f5n|0','_gd_visitor': '6e3ef52c-f45a-4320-8d17-bb614fa84616','drift_aid': 'f5932956-b73b-4db3-959a-fd4f32954817','driftt_aid': 'f5932956-b73b-4db3-959a-fd4f32954817','_uetvid': '0a87869049db11edafbc774fa84becf9','known_by_marketo_email': 'info@crawler.pro.vn','cf_clearance': '1w7nyXwpo5saifk5sd4VlUaE4p.FMtyJvAUNgGzHxg4-1666089495-0-150','rl_session': 'RudderEncrypt%3AU2FsdGVkX1%2BiI3a1U56Hjd92bDrZ%2FaYug0k4WiaNoxYJy1uqIus%2FzjRWq6pPwKj65JFFxOGnVv73UlkjzHFX%2BGtVxnka3QTBa0VT1mx59jcLP55mgsD2SUMRGIpS1GICgEzyKJGbH8RcK40Q0fyJ2A%3D%3D','rl_user_id': 'RudderEncrypt%3AU2FsdGVkX1%2FDQW2qzkudHG%2FFc8j%2FsAxiR7he6N9lAQs%3D','rl_trait': 'RudderEncrypt%3AU2FsdGVkX1%2Bm8BTSwrfSUo%2BXrbJ40nAe231d2ERyb8SFQRw0KKPnxG%2BjafrN3eeTwaq94Y0MjOn6GFz%2B3%2FK%2FDNh6psBPj8O6qTEkvSxDVqy1ym5%2FpZ35xTsS%2FVZLI5NJEZClL1PYPo552fLn%2B9eNksArBbHdKAwzl5dbNeemTrKkt1BYjTUueVrmCTSW%2Bxvk5JVYRff4BHsUrDypQKIY%2FQ%3D%3D','rl_group_id': 'RudderEncrypt%3AU2FsdGVkX1%2BhY36SSI3M36emklyi%2Bf9J7ziFPPY0pgQ%3D','rl_group_trait': 'RudderEncrypt%3AU2FsdGVkX19Q1AVZaZM%2FHbPifRElqic6g7W7hCSZJ2k%3D','rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX19McQ761E85ILqO2VvHozSgGkt1i3hhYSXghan3S9HqpM72D5ymGWgx3LVteL3YOnocED0XJgTbhA%3D%3D','rl_page_init_referrer': 'RudderEncrypt%3AU2FsdGVkX19nB6CLLPK31ucf0vWsT32CnDMkVRAXLUw%3D','rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX19tUqwmVfuix2Q92U3E6WYX7qhZhrzXvl0%3D','AWSALB': '6AWaB5svm+BJAUh4m2j1Xa1QFvRpzeUu0Yi2ZSkRZj5NlMQOt7tCa1ogCEMGmlz8SxQ0KF1ULw88LS7SNCfqbLcnZXCrZmjci0wbtaLNxF0NgHGbUs2AvWWeIFOCTfs5j2YT7XGDpia3rnwFqItzcYaG3qTM03lsgyUBySbUVovqZBGXBE1dWN7+M2i4PA==','AWSALBCORS': '6AWaB5svm+BJAUh4m2j1Xa1QFvRpzeUu0Yi2ZSkRZj5NlMQOt7tCa1ogCEMGmlz8SxQ0KF1ULw88LS7SNCfqbLcnZXCrZmjci0wbtaLNxF0NgHGbUs2AvWWeIFOCTfs5j2YT7XGDpia3rnwFqItzcYaG3qTM03lsgyUBySbUVovqZBGXBE1dWN7+M2i4PA==','at': 'H2SPyIo_ZSRhAdMXgNiOyLZIUvGyrNJmABaciXCz5CAStB7jVLRn0-x5P-MoHQxRu9b0GSTLdJlrRx10Ar6yXvC2ytfT8lePdePfEYqDXOxRR8yaO_SWUpiAOef-YSVpZeXzDjqjum40OfQuDpwR49jSgsUswdczRH24Ujr1hkSN1XUMY4sfHKiDElEh3FHKpdNDnJDB07CCa7bGL14E_RKLxgbOUIBcDuGIUfUkGqGQLLvjFnuMQiulI0J1OlP_jhy5yLysU1mZBlU-vuPLKUlBoBxjpSiB41JHVMLBzV0eBN18YJW-Bx-4V-Xhs5UEe6al9Ee5JN5-kmXNd__g5vuoYua95VGpOhc-N0tRMdc5-lKXq64Sz_ITy2ZNNiVfwhS-Lvhv7BRQTilF2Oy-AVXzi6y5SvPh9pBf1zJOdMHoy16RPnT24kkPvLpKQLtYAHgq_ujGnm74Li0ApBvLNOIvxMZsG3kGzGXXPdUcGVR2pTmZ4P2xbBE69vVW2mPxWBeydsm6fj49eskzdLsfswmwDueo60l9h8aOUcJPhSH5VBLyMB8hH2ir5E_4h8AxS3M1Z0Dy3wW4vDKil9ogAOuPwe_meZuSiSXQiLZJPMO92Na6mwDn7qqCJ3QzTLjVXGXHSBnKILIZYH8jlknhMQdVdpvA_XBdfSZwf4GmrDYu9gVAuI9Vedy803NkvgSJSrCaSL68nsRJUV-_U6o-Bs-KtVq5OaVe0kzZHfzkgp-5PXo7BKGjtSVPRp3LueHZIJeTWrW_mFX55cGY_cu3ghgV24CztI1LhTOuYafMA8pZcdIYKEDl-bYtayTfgyyqxDjvGoze8VEKp-ZTSyBgb6VwPtzeEugvMYrfvQQO-DaNLJvQr1w43sRzzcq9oQ','_gcl_au': '1.1.1794617645.1668565669','JSESSIONID': '033B31895D8B470054B4623DEFF23AA7','GSESSIONID': 'dd21d13b-9a0b-420f-ad00-bbcac501d232+1670404209982','cass': '1','gdsid': '1670404209982:1670410992165:7E779A528FA134706A3647F053A1F686','JSESSIONID_PC_APP': 'BADE3E6929D46E8BAEF3CDA1AA406523','_gid': 'GA1.2.837180361.1670404214','SameSite': 'None','asst': '1670410992.0','bs': 'SHcvTfrtd6rmHB-KPl24Dw:GAggQjNU4XGTEwG6Dw1EQcDNUdnmhlJMBsjvvlnrOg7SE4eXtVz3-bGl-0qbRV9oeNhVrm6OUrq_FlL1RsMpWBGWTPI460dDfWrDmfIUlxg:AMvh2-BUEWUCPGhMgZyXSbROD22InLLaaZmdSsLIN50','__cf_bm': 'aiWPiUwF1H.OPBlTMo.E8u7Fk8_o0XH9DUvfYp3cA0E-1670410992-0-ATzXtqv57uUIPwCGXdDoSdxcPGHOZn63rfF3shwKuwU1uayKDj7eJuW6pJXE8MzBeI73XeAoIAOIgwiF52PLmrE=','_dc_gtm_UA-2595786-1': '1','ln_or': 'd',}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0','Accept': '*/*','Accept-Language': 'en-GB,en;q=0.5','Content-Type': 'application/json','Referer': 'https://www.glassdoor.com/','gd-csrf-token': 'NwoSFYzuJe5aVlDYnY3tXQ:LLGAvfhFDBN-us8tHkGpi8PpIVzgysr-x6u1SWVzh6FZiNeVsBWUHjFF9jtw4HfAZirPOrxV3gOR87piiBnOtg:0ZwqoF1c1Jh77-mY7DbKs6kUNGRW8Vq5SHUgRV8genU','x-gd-dos2-experiments-json': '{"content_indeed":{"treatment":"apply_t1","experiment":"PROD_test","params":{"apply":"true"}},"content_reviews_sort":{"treatment":"newRankScore2","experiment":"CXP-1964_PROD_test_08162021","params":{"reviewLengthMultiplier":"1","reviewLengthLimit":"300","reviewLengthConstant":"100","recencyFunctionMultiplier":"-25","recencyFunctionExponentiator":"0.5","recencyFunctionLimit":"1000","recencyFunctionConstant":"-1000","ratingModifierMultiplier":"3"}}}','apollographql-client-name': 'reviews','apollographql-client-version': '7.13.3','Origin': 'https://www.glassdoor.com','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','Connection': 'keep-alive','Alt-Used': 'www.glassdoor.com',}
    if os.path.exists('headers.json'):
        f=open('headers.json','r')
        headers_str=json.loads(f.read())
        f.close()
        for k,v in headers_str.items():
            if k in headers:
                headers[k]=v
    if os.path.exists('cookies.json'):
        f=open('cookies.json','r')
        cookies_str=json.loads(f.read())
        f.close()
        for k,v in cookies_str.items():
            if k in cookies:
                cookies[k]=v
    START=0
    LIMIT=1
    if os.path.exists('CRAWLED.txt'):
        START=int(open('CRAWLED.txt').read())
    WRITE=False
    def __init__(self, RUN=None, **kwargs):
        if not RUN is None:
            self.RUN=int(RUN)
        super().__init__(**kwargs)
    def get_cookies(self):
        CHK=False
        while CHK==False:
            #options = webdriver.FirefoxOptions()
            #options.add_argument("--headless")
            #driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            driver.maximize_window()
            driver.get('https://www.glassdoor.com/employers/')
            time.sleep(3)
            driver.find_element_by_xpath('//a[@aria-label="Sign In"]').click()
            time.sleep(2)
            driver.find_element_by_xpath('//input[@id="userEmail"]').send_keys(GLASSDOOR_USER)
            driver.find_element_by_xpath('//input[@id="userPassword"]').send_keys(GLASSDOOR_PASSWORD)
            time.sleep(2)
            driver.find_element_by_xpath('//button[contains(@class,"minWidthBtn")]').click()
            time.sleep(3)
            driver.get('https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm')
            time.sleep(20)
            if 'lib__EIFilterModuleStyles__clearAll' in driver.page_source:
                driver.find_element_by_xpath('//a[contains(@class,"lib__EIFilterModuleStyles__clearAll")]').click()
                time.sleep(8)
            TOKEN=str(driver.page_source).split('"gdToken":"')
            TOKEN=str(TOKEN[len(TOKEN)-1]).split('"')[0]
            print('TOKEN:',TOKEN)
            self.headers['gd-csrf-token']=TOKEN
            COOKIES=driver.get_cookies()
            for row in COOKIES:
                if row['name'] in self.cookies:
                    self.cookies[row['name']]=row['value']
            ID=6036
            json_data = [{'operationName': 'EiSalariesGraphQuery','variables': {'cityId': None,'countryId': None,'domain': 'glassdoor.com','employerId': ID,'getLocations': True,'goc': 0,'jobTitle': '','locale': 'en-US','metroId': None,'pageNum': 1,'pageSize': 20,'sortType': 'COUNT','stateId': None,'payPeriod': None,'viewAsPayPeriodId': 'ANNUAL','useUgcSearch2ForSalaries': 'false','enableSalaryEstimates': False,'enableV3Estimates': True,},'query': 'query EiSalariesGraphQuery($employerId: Int!, $cityId: Int, $metroId: Int, $goc: Int, $stateId: Int, $countryId: Int, $jobTitle: String!, $pageNum: Int!, $sortType: SalariesSortOrderEnum, $employmentStatuses: [SalariesEmploymentStatusEnum], $domain: String, $locale: String, $gdId: String, $ip: String, $userId: Int, $payPeriod: PayPeriodEnum, $viewAsPayPeriodId: PayPeriodEnum, $useUgcSearch2ForSalaries: String, $enableSalaryEstimates: Boolean, $enableV3Estimates: Boolean) {\n  employmentStatusEnums(context: {domain: $domain}) {\n    values\n    __typename\n  }\n  salariesByEmployer(\n    goc: {sgocId: $goc}\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    page: {num: $pageNum, size: 20}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n    payPeriod: $payPeriod\n    employmentStatuses: $employmentStatuses\n    sort: $sortType\n    viewAsPayPeriodId: $viewAsPayPeriodId\n    enableSalaryEstimates: $enableSalaryEstimates\n    enableV3Estimates: $enableV3Estimates\n  ) {\n    salaryCount\n    filteredSalaryCount\n    pages\n    mostRecent\n    jobTitleCount\n    filteredJobTitleCount\n    seoTexts {\n      salarySeoDescriptionText\n      salarySeoDescriptionTitle\n      salarySeoDescriptionBody\n      __typename\n    }\n    lashedJobTitle {\n      text\n      __typename\n    }\n    queryLocation {\n      id\n      type\n      name\n      shortName\n      __typename\n    }\n    queryEmployer {\n      shortName\n      __typename\n    }\n    results {\n      salaryEstimatesFromJobListings\n      currency {\n        code\n        __typename\n      }\n      employer {\n        shortName\n        squareLogoUrl\n        id\n        counts {\n          globalJobCount {\n            jobCount\n            __typename\n          }\n          __typename\n        }\n        links {\n          jobsUrl\n          __typename\n        }\n        __typename\n      }\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      obscuring\n      payPeriod\n      count\n      employerTotalCount\n      employmentStatus\n      minBasePay\n      medianBasePay\n      maxBasePay\n      totalCompMin\n      totalCompMax\n      totalCompMedian\n      totalAdditionalCashPayMin\n      totalAdditionalCashPayMax\n      totalAdditionalCashPayMedian\n      links {\n        employerSalariesByCompanyLogoUrl\n        employerSalariesAllLocationsInfositeUrl\n        employerSalariesInfositeUrl\n        __typename\n      }\n      totalCompPercentiles {\n        ident\n        value\n        __typename\n      }\n      totalPayInsights {\n        isHigh\n        percentage\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  salaryLocations(\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n  ) {\n    countries {\n      id\n      identString\n      name\n      salaryCount\n      currency {\n        symbol\n        __typename\n      }\n      states {\n        id\n        identString\n        name\n        salaryCount\n        metros {\n          id\n          identString\n          name\n          salaryCount\n          cities {\n            id\n            identString\n            name\n            salaryCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',},]
            response = requests.post('https://www.glassdoor.com/graph', headers=self.headers,cookies=self.cookies, json=json_data)
            try:
                DATA=json.loads(response.text)
                print('Cookies is OK')
                f=open('headers.json','w')
                f.write(json.dumps(self.headers))
                f.close()
                f=open('cookies.json','w')
                f.write(json.dumps(self.cookies))
                f.close()
                CHK=True
                driver.close()
                return True
            except:
                print('Can not get reponse, please try to re-run !!!')
                driver.close()
    def parse(self,response):
        f=open('urls.txt','r')
        LIST=re.split('\r\n|\n',f.read())
        f.close()
        ID=6036
        json_data = [{'operationName': 'EiSalariesGraphQuery','variables': {'cityId': None,'countryId': None,'domain': 'glassdoor.com','employerId': ID,'getLocations': True,'goc': 0,'jobTitle': '','locale': 'en-US','metroId': None,'pageNum': 1,'pageSize': 20,'sortType': 'COUNT','stateId': None,'payPeriod': None,'viewAsPayPeriodId': 'ANNUAL','useUgcSearch2ForSalaries': 'false','enableSalaryEstimates': False,'enableV3Estimates': True,},'query': 'query EiSalariesGraphQuery($employerId: Int!, $cityId: Int, $metroId: Int, $goc: Int, $stateId: Int, $countryId: Int, $jobTitle: String!, $pageNum: Int!, $sortType: SalariesSortOrderEnum, $employmentStatuses: [SalariesEmploymentStatusEnum], $domain: String, $locale: String, $gdId: String, $ip: String, $userId: Int, $payPeriod: PayPeriodEnum, $viewAsPayPeriodId: PayPeriodEnum, $useUgcSearch2ForSalaries: String, $enableSalaryEstimates: Boolean, $enableV3Estimates: Boolean) {\n  employmentStatusEnums(context: {domain: $domain}) {\n    values\n    __typename\n  }\n  salariesByEmployer(\n    goc: {sgocId: $goc}\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    page: {num: $pageNum, size: 20}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n    payPeriod: $payPeriod\n    employmentStatuses: $employmentStatuses\n    sort: $sortType\n    viewAsPayPeriodId: $viewAsPayPeriodId\n    enableSalaryEstimates: $enableSalaryEstimates\n    enableV3Estimates: $enableV3Estimates\n  ) {\n    salaryCount\n    filteredSalaryCount\n    pages\n    mostRecent\n    jobTitleCount\n    filteredJobTitleCount\n    seoTexts {\n      salarySeoDescriptionText\n      salarySeoDescriptionTitle\n      salarySeoDescriptionBody\n      __typename\n    }\n    lashedJobTitle {\n      text\n      __typename\n    }\n    queryLocation {\n      id\n      type\n      name\n      shortName\n      __typename\n    }\n    queryEmployer {\n      shortName\n      __typename\n    }\n    results {\n      salaryEstimatesFromJobListings\n      currency {\n        code\n        __typename\n      }\n      employer {\n        shortName\n        squareLogoUrl\n        id\n        counts {\n          globalJobCount {\n            jobCount\n            __typename\n          }\n          __typename\n        }\n        links {\n          jobsUrl\n          __typename\n        }\n        __typename\n      }\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      obscuring\n      payPeriod\n      count\n      employerTotalCount\n      employmentStatus\n      minBasePay\n      medianBasePay\n      maxBasePay\n      totalCompMin\n      totalCompMax\n      totalCompMedian\n      totalAdditionalCashPayMin\n      totalAdditionalCashPayMax\n      totalAdditionalCashPayMedian\n      links {\n        employerSalariesByCompanyLogoUrl\n        employerSalariesAllLocationsInfositeUrl\n        employerSalariesInfositeUrl\n        __typename\n      }\n      totalCompPercentiles {\n        ident\n        value\n        __typename\n      }\n      totalPayInsights {\n        isHigh\n        percentage\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  salaryLocations(\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n  ) {\n    countries {\n      id\n      identString\n      name\n      salaryCount\n      currency {\n        symbol\n        __typename\n      }\n      states {\n        id\n        identString\n        name\n        salaryCount\n        metros {\n          id\n          identString\n          name\n          salaryCount\n          cities {\n            id\n            identString\n            name\n            salaryCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',},]
        response = requests.post('https://www.glassdoor.com/graph', headers=self.headers,cookies=self.cookies, json=json_data)
        try:
            DATA=json.loads(response.text)
            print('Cookies is OK')
        except:
            self.get_cookies()
        #for i in range(len(LIST)):
        for i in range(self.START,self.START+self.LIMIT):
            LS=LIST[i]
            CHK=False
            if not self.RUN is None:
                if self.RUN==i:
                    CHK=True
                    print(self.RUN,' ==> ', LS)
            else:
                CHK=True
                print(LS)
            CHK=True
            if not str(LS).startswith('#') and CHK==True:
                if '~' in LS:
                    LS=str(LS).split('~')
                    STR=re.split('_E|-EI|_IE|-E', str(LS[1]))
                else:
                    STR=re.split('_E|-EI|_IE|-E', str(LS))
                STR=STR[len(STR)-1]
                ID=int(Get_Number(re.split('\.|\_', str(STR))[0]))
                print(ID)
                json_data = [{'operationName': 'EIReviewsPageGraphQuery','variables': {'onlyCurrentEmployees': False,'employerId': ID,'jobTitle': None,'location': {'countryId': None,'stateId': None,'metroId': None,'cityId': None,},'employmentStatuses': [],'goc': None,'highlight': None,'page': 1,'sort': 'RELEVANCE','fetchHighlights': True,'applyDefaultCriteria': False,'worldwideFilter': False,'language': 'por','divisionId': None,'preferredTldId': 0,'isRowProfileEnabled': None,'dynamicProfileId': 117106,'isLoggedIn': True,},'query': 'query EIReviewsPageGraphQuery($onlyCurrentEmployees: Boolean, $employerId: Int!, $jobTitle: JobTitleIdent, $location: LocationIdent, $employmentStatuses: [EmploymentStatusEnum], $goc: GOCIdent, $highlight: HighlightTerm, $page: Int!, $sort: ReviewsSortOrderEnum, $fetchHighlights: Boolean!, $applyDefaultCriteria: Boolean, $worldwideFilter: Boolean, $language: String, $divisionId: DivisionIdent, $preferredTldId: Int, $isRowProfileEnabled: Boolean, $dynamicProfileId: Int, $isLoggedIn: Boolean!) {\n  employerDivisionReviews(employer: {id: $employerId}) {\n    employer {\n      links {\n        reviewsUrl\n        __typename\n      }\n      __typename\n    }\n    employerRatings {\n      overallRating\n      __typename\n    }\n    employerReviews {\n      divisionLink\n      ratingOverall\n      pros\n      __typename\n    }\n    divisions {\n      id\n      name\n      ratings {\n        overallRating\n        __typename\n      }\n      reviews {\n        divisionLink\n        featured\n        pros\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  employerReviews(\n    onlyCurrentEmployees: $onlyCurrentEmployees\n    employer: {id: $employerId}\n    jobTitle: $jobTitle\n    location: $location\n    goc: $goc\n    employmentStatuses: $employmentStatuses\n    highlight: $highlight\n    sort: $sort\n    page: {num: $page, size: 10}\n    applyDefaultCriteria: $applyDefaultCriteria\n    worldwideFilter: $worldwideFilter\n    language: $language\n    division: $divisionId\n    preferredTldId: $preferredTldId\n    isRowProfileEnabled: $isRowProfileEnabled\n    dynamicProfileId: $dynamicProfileId\n  ) {\n    filteredReviewsCountByLang {\n      count\n      isoLanguage\n      __typename\n    }\n    employer {\n      activeStatus\n      bestPlacesToWork {\n        id\n        isCurrent\n        timePeriod\n        __typename\n      }\n      bestProfile {\n        id\n        __typename\n      }\n      ceo {\n        id\n        name\n        __typename\n      }\n      counts {\n        benefitCount\n        globalJobCount {\n          jobCount\n          __typename\n        }\n        interviewCount\n        jobCount\n        photoCount\n        pollCount\n        reviewCount\n        salaryCount\n        __typename\n      }\n      coverPhoto {\n        hiResUrl\n        __typename\n      }\n      divisions {\n        employerId\n        __typename\n      }\n      employerManagedContent {\n        featuredVideoLink\n        isContentPaidForTld\n        videoModule {\n          vimeoVideos\n          youTubeVideos\n          youTubeChannel\n          videoChannelPosition\n          __typename\n        }\n        __typename\n      }\n      id\n      isOpenCompany: requirementsComplete\n      largeLogoUrl: squareLogoUrl(size: LARGE)\n      links {\n        benefitsUrl\n        faqUrl\n        interviewUrl\n        jobsUrl\n        locationsUrl\n        orgStructureUrl\n        overviewUrl\n        photosUrl\n        pollsUrl\n        reviewsUrl\n        salariesUrl\n        __typename\n      }\n      officeAddresses {\n        id\n        __typename\n      }\n      parent {\n        employerId\n        employer {\n          shortName\n          links {\n            overviewUrl\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      regularLogoUrl: squareLogoUrl(size: REGULAR)\n      relatedEmployers {\n        employerId\n        __typename\n      }\n      shortName\n      squareLogoUrl\n      subsidiaries {\n        employerId\n        __typename\n      }\n      website\n      primaryIndustry {\n        industryId\n        sectorId\n        __typename\n      }\n      __typename\n    }\n    queryLocation {\n      id\n      type\n      shortName\n      longName\n      __typename\n    }\n    queryJobTitle {\n      id\n      text\n      __typename\n    }\n    currentPage\n    numberOfPages\n    lastReviewDateTime\n    allReviewsCount\n    ratedReviewsCount\n    filteredReviewsCount\n    ratings {\n      overallRating\n      reviewCount\n      ceoRating\n      recommendToFriendRating\n      cultureAndValuesRating\n      diversityAndInclusionRating\n      careerOpportunitiesRating\n      workLifeBalanceRating\n      seniorManagementRating\n      compensationAndBenefitsRating\n      businessOutlookRating\n      ceoRatingsCount\n      ratedCeo {\n        id\n        name\n        title\n        regularPhoto: photoUrl(size: REGULAR)\n        largePhoto: photoUrl(size: LARGE)\n        currentBestCeoAward {\n          displayName\n          timePeriod\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    reviews {\n      isLegal\n      reviewId\n      reviewDateTime\n      ratingOverall\n      ratingCeo\n      ratingBusinessOutlook\n      ratingWorkLifeBalance\n      ratingCultureAndValues\n      ratingDiversityAndInclusion\n      ratingSeniorLeadership\n      ratingRecommendToFriend\n      ratingCareerOpportunities\n      ratingCompensationAndBenefits\n      employer {\n        id\n        shortName\n        regularLogoUrl: squareLogoUrl(size: REGULAR)\n        largeLogoUrl: squareLogoUrl(size: LARGE)\n        __typename\n      }\n      isCurrentJob\n      lengthOfEmployment\n      employmentStatus\n      jobEndingYear\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      location {\n        id\n        type\n        name\n        __typename\n      }\n      originalLanguageId\n      pros\n      prosOriginal\n      cons\n      consOriginal\n      summary\n      summaryOriginal\n      advice\n      adviceOriginal\n      isLanguageMismatch\n      countHelpful\n      countNotHelpful\n      employerResponses {\n        id\n        response\n        userJobTitle\n        responseDateTime(format: ISO)\n        countHelpful\n        countNotHelpful\n        responseOriginal\n        languageId\n        originalLanguageId\n        translationMethod\n        __typename\n      }\n      featured\n      isCovid19\n      divisionName\n      divisionLink\n      links {\n        reviewDetailUrl\n        __typename\n      }\n      topLevelDomainId\n      languageId\n      translationMethod\n      __typename\n    }\n    __typename\n  }\n  pageViewSummary {\n    totalCount\n    __typename\n  }\n  reviewHighlights(employer: {id: $employerId}, language: $language) @include(if: $fetchHighlights) {\n    pros {\n      id\n      reviewCount\n      topPhrase\n      keyword\n      links {\n        highlightPhraseUrl\n        __typename\n      }\n      __typename\n    }\n    cons {\n      id\n      reviewCount\n      topPhrase\n      keyword\n      links {\n        highlightPhraseUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  reviewLocations(employer: {id: $employerId}) {\n    countries {\n      type\n      id\n      identString\n      name\n      containsEmployerHQ\n      states {\n        type\n        id\n        identString\n        name\n        containsEmployerHQ\n        metros {\n          type\n          id\n          identString\n          name\n          containsEmployerHQ\n          cities(onlyIfOther: true) {\n            type\n            id\n            identString\n            name\n            containsEmployerHQ\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  faqQuestionsByEmployer(employerId: $employerId) {\n    totalQuestions\n    __typename\n  }\n  getCompanyFollowsForUser @include(if: $isLoggedIn) {\n    employer {\n      id\n      __typename\n    }\n    follow\n    __typename\n  }\n}\n',},]
                yield scrapy.Request(self.start_urls[0],callback=self.parse_content,meta={'json_data':json_data},dont_filter=True)
    def parse_content(self,response):
        json_data=response.meta['json_data']
        response = requests.post('https://www.glassdoor.com/graph', headers=self.headers,cookies=self.cookies, json=json_data)
        if response.status_code<400 :
            if self.WRITE==False:
                open('CRAWLED.txt','w').write(str(self.START+self.LIMIT))
                self.WRITE=True
            DATA=json.loads(response.text)
            Data=DATA[0]['data']['employerReviews']
            for row in Data['reviews']:
                item={}
                item['Company']=Data['employer']['shortName']
                item['Date']=str(row['reviewDateTime']).split('T')[0]
                item['Title']=row['summary']
                item['URL']=self.start_urls[0]+row['links']['reviewDetailUrl']
                try:
                    item['Contact_Name']=row['jobTitle']['text']
                except:
                    item['Contact_Name']=''
                item['Rating']=row['ratingOverall']
                if row['isCurrentJob']==True:
                    item['Description']='Current Employee'
                    if row['lengthOfEmployment']>0:
                        item['Description']+=', more than '+str(row['lengthOfEmployment'])+' year'
                else:
                    item['Description']='Former  Employee'
                    if row['lengthOfEmployment']>0:
                        item['Description']+=', more than '+str(row['lengthOfEmployment']-1)+' year'
                item['Pros']=row['pros']
                item['Cons']=row['cons']
                item['Advice to Management']=row['advice']
                item['Recommend']=(str(row['ratingRecommendToFriend']).lower()).replace('none', 'no reponse')
                item['CEO Approval']=(str(row['ratingCeo']).lower()).replace('none', 'no reponse')
                item['Business Outlook']=(str(row['ratingBusinessOutlook']).lower()).replace('none', 'no reponse')
                try:
                    item['Location']=row['location']['name']
                except:
                    item['Location']=''
                item['Work/Life Balance']=row['ratingWorkLifeBalance']
                item['Culture & Values']=row['ratingCultureAndValues']
                item['Diversity & Inclusion']=row['ratingDiversityAndInclusion']
                item['Career Opportunities']=row['ratingCareerOpportunities']
                item['Compensation and Benefits']=row['ratingCompensationAndBenefits']
                item['Senior Management']=row['ratingSeniorLeadership']
                item['KEY_']=str(row['reviewId'])
                yield(item)
            if DATA[0]['data']['employerReviews']['currentPage']<DATA[0]['data']['employerReviews']['numberOfPages']:
                print('NEXT PAGE:',DATA[0]['data']['employerReviews']['currentPage']+1)
                json_data[0]['variables']['page']=DATA[0]['data']['employerReviews']['currentPage']+1
                yield scrapy.Request(self.start_urls[0],callback=self.parse_content,meta={'json_data':json_data},dont_filter=True)
