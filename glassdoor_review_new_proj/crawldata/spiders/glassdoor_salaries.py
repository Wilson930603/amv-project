import scrapy,re,json,os,requests,time
from urllib.parse import quote
from crawldata.functions import *
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from crawldata.settings import GLASSDOOR_USER,GLASSDOOR_PASSWORD

class CrawlerSpider(scrapy.Spider):
    name = 'glassdoor_salaries'
    start_urls=['http://httpbin.org/ip']
    f=open('urls.txt','r')
    LIST=re.split('\r\n|\n',f.read())
    f.close()
    cookies = {'gdId': '1d139927-b06f-4e33-b277-816254222ba6','trs': 'direct:direct:direct:2023-01-31+06%3A47%3A37.32:undefined:undefined','rl_session': 'RudderEncrypt%3AU2FsdGVkX1%2FKP2aNTtkAja59qXnKuBlMpdA7ZgAJiYa5Vuv3j3p4cXs5zyhSxuOkbxXY0FDIVOf2sziJy3WWRN9vY3FS%2BY%2BaFvcIHlbMoiCWMYTItmoQYS0OPWLI4kTKyUMlt2%2BwbftEoBKO%2BcFsbw%3D%3D','rl_user_id': 'RudderEncrypt%3AU2FsdGVkX19lEUD1pykU0rVwgcfAW5DJB8j8yMyddjc%3D','rl_trait': 'RudderEncrypt%3AU2FsdGVkX1%2BglpSG0tLoScB0w0I3ydEMQMQif4nv7D%2Bp%2F630WU1XXgpxMqZJSmSpQMbiladvf%2FSQZerP5twGKPHwAtsfsayGouZtAFGrkzW5huiNdAg3lQW43V2K4GBhtai%2FsF8ID7sU4Bl%2FNgTxinSOQI4qxRnICEdvPT45suzrwBirR0Te9KRTLiOxHTidpk5vGotLd2IhE7qsMZczQziGaw3Ey6BM4JU0rsh%2B%2FOjFB76g9k2RNBNzaeQG8vqfuPrfW0JoYiNRrSJFqsXYXyIUu%2BcnNW%2BnHnAjkOhXsXRFNRLThHUMEgdo0Q00P1vT','rl_group_id': 'RudderEncrypt%3AU2FsdGVkX1%2B69GdiVhvwvPv73b05YXHmgmfyDVqV3DA%3D','rl_group_trait': 'RudderEncrypt%3AU2FsdGVkX19nBFvHMZFLGIqYYCg%2BohQNbHjOmt4gXJs%3D','rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX18yJOqlpYejKCPYbn0JmDPKJ3Ji2bAwYAbi383IL7Ai%2F8wTURMWdOrIp5QMzNEzpoJ3iJD1kz6J4w%3D%3D','rl_page_init_referrer': 'RudderEncrypt%3AU2FsdGVkX1%2FRux4CYvMqH8ot2SaZj6NDTqY1OTQC23kvOgZJXXR%2F3TOK9%2Fp1M8t7','rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX1%2BdCx%2B5xPoiX8rHCpuawXUJtlZ46HBAINlzqS6CZNQM%2BM8CYUI0nC8X','G_ENABLED_IDPS': 'google','_ga': 'GA1.2.802249789.1675176495','OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Apr+15+2023+13%3A20%3A20+GMT%2B0700+(Indochina+Time)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=ccff4c88-b8ce-4470-8cb6-7a38b3f505f7&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false','_optionalConsent': 'true','_gcl_au': '1.1.897742432.1675176496','__pdst': '38d99cdc7efc4212b832d6abbd92ed07','_rdt_uuid': '1675176495924.a96eb5f7-1b5c-437e-a2e9-dfb9e454cfd3','_pin_unauth': 'dWlkPU4ySXhOREUxWVRVdE1EUmhNQzAwWkdFMExUZzVOelF0WVRreVlXSTVOMkUxTURVMA','_fbp': 'fb.1.1675176498460.562419655','_tt_enable_cookie': '1','_ttp': 'gngzJplB5s40nF_HwYZYVXmMNi8','ki_t': '1675176499473%3B1681532001801%3B1681539621799%3B16%3B138','ki_r': '','ki_u': '8ffe4fdb-17f7-e4c1-a800-930e','uc': '8013A8318C98C517A1E3210FFD1F05F398C9D2152F0180DC768A742F3472FB8F427D6A68FB38F2B1B28726BCFCF3A5954B227C87A60D51481D1C99ABCCBA75AD66D19FE28C0B9437C4766BD65F74E0B46F6E94CF18AD31214A49501A582048A16FE6B0F83C6B85B3C9FFCD329729BBAA9F99A0D3FE413F66C05C4B1C4BD73D458FA62D117D89E5FA78073142BB7E0B2B','ki_s': '218147%3A1.0.0.0.2%3B221866%3A21.0.0.0.2','indeedCtk': '1gp7rvs2ch4dl801','known_by_marketo_email': 'info@crawler.pro.vn','_gd_visitor': '3a1e607b-1d88-446b-88e7-e4585ac55e73','_mkto_trk': 'id:899-LOT-464&token:_mch-glassdoor.com-1679633154216-23294','_uetvid': 'c1987f40c9fe11ed8ea805849bfabb45','drift_aid': '1fe507db-7676-43af-b490-abd7a8c25935','driftt_aid': '1fe507db-7676-43af-b490-abd7a8c25935','at': 'J1PxDTQTg31DqKBaqA-G4VS425v2-8-IOejwoNWoRd0405uzUbmSIvXVwka1L7If1E27jKy1URm9iwzidyvPFt-lSQJL5pL9bnDPMPv_3OOtYDR3kunEXUX-8NiVY8B8gZh4JK-fzANYX8dftvcXbQLr_rE4eA2gHAvwf-MbGbilMWBjM8CaMti6puJrHxMja9OANsqNp6U-mr3zf508ad-dT41G73j66fxdAyBmpQZQjpMvGVZqP_2A57UIi0d9U-lZVwXs_kTeyDmRXXhoxobE4ancXd3Ufo80Cky5W-Z7GKMn8LsWc1n-USJbsH-GredKXvcTE7YrUzu2H8OcWopQjcLPFb5RMfDxy5p_5L4euF-i05n1kxWnGKIZYAJCxBRqPW1sbjldwt4V6Y-ZGLgONX0OBEJhmRW0OZE-A-mVaJrwyf7HHFsq6ybWhjj6RoPZnqgf43k-33BxBOc0WoOV6j8e0ke5y1sv5fWEfVy2aAncRGhxmMfehEN1TBomTHNCeCzsGc174ppOLyVx8KI5yFjcZsXtJ1_RtL9QoRKlmx6Xe75Z0KS-jVQgcZbQ7M5YTEDhUKat1Bg8T4fmUS-Nuq98qPv6VLFLyQ17WilkcAyEqfN6DxYCgIkERXUmQEHJyzJcwrXwIq44eXbASeA0KTmuALnOWX87a4cCOFwNzU0NxwThDX4XMeenMn8skrEDkeKjpDtat2H3Mi7h_GcC_xOajpNpvgGZ4LRRD43RNhVdGfHecEtYp5kmggMbG7fFdxwmFn8YQp--2a9CREYiXAc4ElAuIe2U_B7Zt59woAnFG2xLh__TnvOjOE2s76jWG4E9-5zG9j8mkFPNC5ka3n5sAZuo3UaIejoF6UoC3ZWhefBQp4rN4UYPMA','AWSALB': '72J0yRhxeviIJWzxQFn9/me1ms+VxZ2gOhlHJEldvmy2RT/7kYDT2lnW6/lYerUDRRs2ZsTUm9AgbLsf2mcV5Rt5LLcZx76aKfS09FrKH8CHUgRbd/8g1Qil9ZCx','AWSALBCORS': '72J0yRhxeviIJWzxQFn9/me1ms+VxZ2gOhlHJEldvmy2RT/7kYDT2lnW6/lYerUDRRs2ZsTUm9AgbLsf2mcV5Rt5LLcZx76aKfS09FrKH8CHUgRbd/8g1Qil9ZCx','_gid': 'GA1.2.920075613.1681264916','ln_or': 'eyIzNTY1OTY0IjoiZCJ9','JSESSIONID': 'DD547B07692DD41BF7C0F3980FE6AF7E','GSESSIONID': '1d139927-b06f-4e33-b277-816254222ba6+1681531994660','cass': '1','gdsid': '1681531994660:1681540463705:841D17BFA75BF3DB67B2C3D205BF4FE5','_cfuvid': 'flSbj7HIKshe3gY1NvlcPfuryTtPPGx5mIdMaB.rM8w-1681531996069-0-604800000','fpvc': '32','__gads': 'ID=fc2190f36114309e:T=1681532993:S=ALNI_MaIgolnpy_cYP0DSsUtuYK_Mbw6iw','__gpi': 'UID=00000bf4a6ef36fd:T=1681532993:RT=1681532993:S=ALNI_MZyecLhKGIQoSqW5oHl7Vn9MYRrdw','__cf_bm': '2asNo0_n3vvCryTKsq0KHR1tykN9kKKHPWh44XKeSFI-1681540463-0-AQp45J0cJ3USZ8wcDMbc4EEiiBAs5V61G1uQrkc4bxIu8iclFgt5NkPgCb5dWoDGDzJ0brD+fmFPmzt43Xf3Qxg=','asst': '1681537847.0','rsSessionId': '1681537851278','_dc_gtm_UA-2595786-1': '1'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0','Accept': '*/*','Accept-Language': 'en-GB,en;q=0.5','Content-Type': 'application/json','Referer': 'https://www.glassdoor.com/','gd-csrf-token': '1mchwTtccZn11kHs7ei4-w:D0kGBTSARQWeyT7mDA7PVPvsrnWSjLLhKacIcdlw5ifoTO0HoyPUr_iHvqora6Ns8cTjc3qmUtgzZ8LX7lXg3g:oPDRHhpT9VIgM42fHlyceypiHq3Y_963pihxa1utgmE','x-gd-dos2-experiments-json': '{"content_indeed":{"treatment":"apply_t1","experiment":"PROD_test","params":{"apply":"true"}}}','apollographql-client-name': 'salaries','apollographql-client-version': '9.14.3','Origin': 'https://www.glassdoor.com','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','Connection': 'keep-alive','Alt-Used': 'www.glassdoor.com',}
    if os.path.exists('headers_sa.json'):
        f=open('headers_sa.json','r')
        headers_str=json.loads(f.read())
        f.close()
        for k,v in headers_str.items():
            if k in headers:
                headers[k]=v
    if os.path.exists('cookies_sa.json'):
        f=open('cookies_sa.json','r')
        cookies_str=json.loads(f.read())
        f.close()
        for k,v in cookies_str.items():
            if k in cookies:
                cookies[k]=v
    START=0 # 9384 -> 750
    LIMIT=1
    if os.path.exists('CRAWLED_SA.txt'):
        START=int(open('CRAWLED_SA.txt').read())
    FUNC={}
    if os.path.exists('FUNC.json'):
        FUNC=json.loads(open('FUNC.json','r',encoding='utf-8').read())
    WRITE=False
    def get_cookies(self):
        CHK=False
        while CHK==False:
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
            #driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
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
            driver.get('https://www.glassdoor.com/Salary/Amazon-Salaries-E6036.htm')
            time.sleep(3)
            if 'lib__EIFilterModuleStyles__clearAll' in driver.page_source:
                driver.find_element_by_xpath('//a[contains(@class,"lib__EIFilterModuleStyles__clearAll")]').click()
                time.sleep(8)
            TOKEN=str(driver.page_source).split('"gdToken":"')
            TOKEN=str(TOKEN[len(TOKEN)-1]).split('"')[0]
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
                f=open('headers_sa.json','w')
                f.write(json.dumps(self.headers))
                f.close()
                f=open('cookies_sa.json','w')
                f.write(json.dumps(self.cookies))
                f.close()
                CHK=True
                driver.close()
                return True
            except:
                print('Can not get reponse, please try to re-run !!!')
                driver.close()
    def parse(self,response):
        ID=6036
        json_data = [{'operationName': 'EiSalariesGraphQuery','variables': {'cityId': None,'countryId': None,'domain': 'glassdoor.com','employerId': ID,'getLocations': True,'goc': 0,'jobTitle': '','locale': 'en-US','metroId': None,'pageNum': 1,'pageSize': 20,'sortType': 'COUNT','stateId': None,'payPeriod': None,'viewAsPayPeriodId': 'ANNUAL','useUgcSearch2ForSalaries': 'false','enableSalaryEstimates': False,'enableV3Estimates': True,},'query': 'query EiSalariesGraphQuery($employerId: Int!, $cityId: Int, $metroId: Int, $goc: Int, $stateId: Int, $countryId: Int, $jobTitle: String!, $pageNum: Int!, $sortType: SalariesSortOrderEnum, $employmentStatuses: [SalariesEmploymentStatusEnum], $domain: String, $locale: String, $gdId: String, $ip: String, $userId: Int, $payPeriod: PayPeriodEnum, $viewAsPayPeriodId: PayPeriodEnum, $useUgcSearch2ForSalaries: String, $enableSalaryEstimates: Boolean, $enableV3Estimates: Boolean) {\n  employmentStatusEnums(context: {domain: $domain}) {\n    values\n    __typename\n  }\n  salariesByEmployer(\n    goc: {sgocId: $goc}\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    page: {num: $pageNum, size: 20}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n    payPeriod: $payPeriod\n    employmentStatuses: $employmentStatuses\n    sort: $sortType\n    viewAsPayPeriodId: $viewAsPayPeriodId\n    enableSalaryEstimates: $enableSalaryEstimates\n    enableV3Estimates: $enableV3Estimates\n  ) {\n    salaryCount\n    filteredSalaryCount\n    pages\n    mostRecent\n    jobTitleCount\n    filteredJobTitleCount\n    seoTexts {\n      salarySeoDescriptionText\n      salarySeoDescriptionTitle\n      salarySeoDescriptionBody\n      __typename\n    }\n    lashedJobTitle {\n      text\n      __typename\n    }\n    queryLocation {\n      id\n      type\n      name\n      shortName\n      __typename\n    }\n    queryEmployer {\n      shortName\n      __typename\n    }\n    results {\n      salaryEstimatesFromJobListings\n      currency {\n        code\n        __typename\n      }\n      employer {\n        shortName\n        squareLogoUrl\n        id\n        counts {\n          globalJobCount {\n            jobCount\n            __typename\n          }\n          __typename\n        }\n        links {\n          jobsUrl\n          __typename\n        }\n        __typename\n      }\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      obscuring\n      payPeriod\n      count\n      employerTotalCount\n      employmentStatus\n      minBasePay\n      medianBasePay\n      maxBasePay\n      totalCompMin\n      totalCompMax\n      totalCompMedian\n      totalAdditionalCashPayMin\n      totalAdditionalCashPayMax\n      totalAdditionalCashPayMedian\n      links {\n        employerSalariesByCompanyLogoUrl\n        employerSalariesAllLocationsInfositeUrl\n        employerSalariesInfositeUrl\n        __typename\n      }\n      totalCompPercentiles {\n        ident\n        value\n        __typename\n      }\n      totalPayInsights {\n        isHigh\n        percentage\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  salaryLocations(\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n  ) {\n    countries {\n      id\n      identString\n      name\n      salaryCount\n      currency {\n        symbol\n        __typename\n      }\n      states {\n        id\n        identString\n        name\n        salaryCount\n        metros {\n          id\n          identString\n          name\n          salaryCount\n          cities {\n            id\n            identString\n            name\n            salaryCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',},]
        response = requests.post('https://www.glassdoor.com/graph', headers=self.headers,cookies=self.cookies, json=json_data)
        try:
            DATA=json.loads(response.text)
            print('Cookies is OK')
        except:
            self.get_cookies()
        #for i in range(len(self.LIST)):
        for i in range(self.START,self.START+self.LIMIT):
            LS=self.LIST[i]
            if '~' in LS:
                LS=str(LS).split('~')[1]
            STR=re.split('_E|-EI|_IE|-E', str(LS))
            STR=STR[len(STR)-1]
            ID=int(Get_Number(re.split('\.|\_', str(STR))[0]))
            url='https://www.glassdoor.com/Salary/'+(str(LS).split('/')[-1]).replace('-Reviews-', '-Salaries-')
            yield scrapy.Request(self.start_urls[0],callback=self.parse_function,meta={'URL':url,'ID':ID},dont_filter=True)
    def parse_function(self,response):
        URL=response.meta['URL']
        ID=response.meta['ID']
        self.headers['referer']=URL
        RES=requests.get(URL,headers=self.headers,cookies=self.cookies)
        response=scrapy.Selector(text=RES.text)
        Data=response.xpath('//div[@data-test="ContentFiltersJobFunctionDropdownContent"]//li')
        for row in Data:
            FID=str(row.xpath('./@id').get()).replace('option_', '')
            FNAME=str(row.xpath('.//span[contains(@class,"dropdownOptionLabel")]/text()').get()).strip()
            print(FID,FNAME)
            json_data = [{'operationName': 'EiSalariesGraphQuery','variables': {'cityId': None,'countryId': None,'domain': 'glassdoor.com','employerId': ID,'gdId': '1d139927-b06f-4e33-b277-816254222ba6','getLocations': True,'goc': int(FID),'jobTitle': '','locale': 'en-US','metroId': None,'pageNum': 1,'pageSize': 20,'sortType': 'COUNT','stateId': None,'userId': 201817205,'payPeriod': None,'viewAsPayPeriodId': 'ANNUAL','useUgcSearch2ForSalaries': 'false','enableSalaryEstimates': False,'enableV3Estimates': True,},'query': 'query EiSalariesGraphQuery($employerId: Int!, $cityId: Int, $metroId: Int, $goc: Int, $stateId: Int, $countryId: Int, $jobTitle: String!, $pageNum: Int!, $sortType: SalariesSortOrderEnum, $employmentStatuses: [SalariesEmploymentStatusEnum], $domain: String, $locale: String, $gdId: String, $ip: String, $userId: Int, $payPeriod: PayPeriodEnum, $viewAsPayPeriodId: PayPeriodEnum, $useUgcSearch2ForSalaries: String, $enableSalaryEstimates: Boolean, $enableV3Estimates: Boolean) {\n  employmentStatusEnums(context: {domain: $domain}) {\n    values\n    __typename\n  }\n  salariesByEmployer(\n    goc: {sgocId: $goc}\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    page: {num: $pageNum, size: 20}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n    payPeriod: $payPeriod\n    employmentStatuses: $employmentStatuses\n    sort: $sortType\n    viewAsPayPeriodId: $viewAsPayPeriodId\n    enableSalaryEstimates: $enableSalaryEstimates\n    enableV3Estimates: $enableV3Estimates\n  ) {\n    salaryCount\n    filteredSalaryCount\n    pages\n    mostRecent\n    jobTitleCount\n    filteredJobTitleCount\n    seoTexts {\n      salarySeoDescriptionText\n      salarySeoDescriptionTitle\n      salarySeoDescriptionBody\n      __typename\n    }\n    lashedJobTitle {\n      text\n      __typename\n    }\n    queryLocation {\n      id\n      type\n      name\n      shortName\n      __typename\n    }\n    queryEmployer {\n      shortName\n      __typename\n    }\n    results {\n      salaryEstimatesFromJobListings\n      currency {\n        code\n        __typename\n      }\n      employer {\n        shortName\n        squareLogoUrl\n        id\n        counts {\n          globalJobCount {\n            jobCount\n            __typename\n          }\n          __typename\n        }\n        links {\n          jobsUrl\n          __typename\n        }\n        __typename\n      }\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      obscuring\n      payPeriod\n      count\n      employerTotalCount\n      employmentStatus\n      minBasePay\n      medianBasePay\n      maxBasePay\n      totalCompMin\n      totalCompMax\n      totalCompMedian\n      totalAdditionalCashPayMin\n      totalAdditionalCashPayMax\n      totalAdditionalCashPayMedian\n      links {\n        employerSalariesByCompanyLogoUrl\n        employerSalariesAllLocationsInfositeUrl\n        employerSalariesInfositeUrl\n        __typename\n      }\n      totalCompPercentiles {\n        ident\n        value\n        __typename\n      }\n      totalPayInsights {\n        isHigh\n        percentage\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  salaryLocations(\n    employer: {id: $employerId}\n    jobTitle: {text: $jobTitle}\n    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n    context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: "useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n  ) {\n    countries {\n      id\n      identString\n      name\n      salaryCount\n      currency {\n        symbol\n        __typename\n      }\n      states {\n        id\n        identString\n        name\n        salaryCount\n        metros {\n          id\n          identString\n          name\n          salaryCount\n          cities {\n            id\n            identString\n            name\n            salaryCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',},]
            yield scrapy.Request(self.start_urls[0],callback=self.parse_content,meta={'json_data':json_data,'FID':FID,'FNAME':FNAME},dont_filter=True)
    def parse_content(self,response):
        json_data=response.meta['json_data']
        FID=response.meta['FID']
        FNAME=response.meta['FNAME']
        response = requests.post('https://www.glassdoor.com/graph', headers=self.headers,cookies=self.cookies, json=json_data)
        if response.status_code<400 :
            if self.WRITE==False:
                open('CRAWLED_SA.txt','w').write(str(self.START+self.LIMIT))
                self.WRITE=True
            DATA=json.loads(response.text)
            Data=DATA[0]['data']['salariesByEmployer']
            if not Data is None and 'results' in Data and not Data['results'] is None:
                for row in Data['results']:
                    item={}
                    item['Company']=Data['queryEmployer']['shortName']
                    item['function name']=FNAME
                    item['Job Title']=row['jobTitle']['text']
                    item['Salaries Submitted']=row['count']
                    item['Total Pay']=int(row['totalCompMedian'])
                    item['Base Pay']=int(row['medianBasePay'])
                    item['Additional Pay']=int(row['totalAdditionalCashPayMedian'])
                    item['Lower Pay Range']=0
                    item['Higher Pay Range']=0
                    for rs in row['totalCompPercentiles']:
                        if rs['ident']=='P25':
                            item['Lower Pay Range']=int(rs['value'])
                        if rs['ident']=='P75':
                            item['Higher Pay Range']=int(rs['value'])
                    item['KEY_']=str(FID)+'_'+key_MD5(row['links']['employerSalariesAllLocationsInfositeUrl'])
                    #item['KEY_']=key_MD5(item['Company'])+'_'+str(json_data[0]['variables']['pageNum'])+'_'+str(i)
                    yield(item)
                print(len(Data['results']),'=>',json_data[0]['variables']['pageNum'],'/',DATA[0]['data']['salariesByEmployer']['pages'])
                if json_data[0]['variables']['pageNum']<DATA[0]['data']['salariesByEmployer']['pages']:
                    json_data[0]['variables']['pageNum']+=1
                    print('NEXT PAGE:',json_data[0]['variables']['pageNum'])
                    self.headers['referer']=LS
                    yield scrapy.Request(self.start_urls[0],callback=self.parse_content,meta={'json_data':json_data,'FID':FID,'FNAME':FNAME},dont_filter=True)
