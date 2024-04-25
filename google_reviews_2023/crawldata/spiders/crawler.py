import scrapy,json,re,os,platform,time
from crawldata.functions import *
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire.utils import decode

class CrawlerSpider(scrapy.Spider):
    name = 'google_reviews'
    DATE_CRAWL=datetime.now().strftime('%Y-%m-%d')
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+DATE_CRAWL+'.log'}
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()+'/scrapy.cfg'
    else:
        URL='file:///' + os.getcwd()+'/scrapy.cfg'
    URLS=re.split('\r\n|\n', open('urls.txt','r',encoding='utf-8').read())
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    def start_requests(self):
        yield scrapy.Request(self.URL,callback=self.parse,dont_filter=True)
    def parse(self, response):
        for url in self.URLS:
            urls=(str(url).strip()).split('~')
            self.driver.get(urls[1])
            time.sleep(5)
            E=self.driver.find_element(By.XPATH, '//input[@id="searchboxinput"]')
            action = ActionChains(self.driver)
            action.move_to_element_with_offset(E, 0, -30)
            action.click()
            action.perform()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//button[@role="tab" and (contains(@aria-label,"Reviews"))]').click()
            time.sleep(5)
            SL=0
            REVIEWS=self.driver.find_elements(By.XPATH, '//div[@role="main"]//div[@data-review-id and (contains(@class,"fontBodyMedium"))]')
            DATA=[]
            while len(REVIEWS)>SL:
                print(SL,'/',len(REVIEWS))
                E=REVIEWS[SL]
                self.driver.execute_script("arguments[0].scrollIntoView();", E)
                time.sleep(1)
                REVIEWS=self.driver.find_elements(By.XPATH, '//div[@role="main"]//div[@data-review-id and (contains(@class,"fontBodyMedium"))]')                
                SL+=1
                for request in self.driver.requests:
                    if request.response and 'listentitiesreviews' in request.url:
                        ID=key_MD5(request.url)
                        if not ID in DATA:
                            DATA.append(ID)
                            body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
                            D=str(body).split('[')[0]
                            body=str(body).split(D)[1]
                            Data=json.loads(body)[2]
                            for row in Data:
                                item={}
                                item['_id']=row[10]
                                item['Company']=urls[0]
                                item['URL']=urls[1]
                                item['Review_name']=row[0][1]
                                item['Reviews']=row[12][1][1]
                                item['Star']=row[4]
                                item['Review_time']=datetime.fromtimestamp(row[27]/1000).strftime('%Y-%m-%d')
                                item['Review_text']=row[3]
                                item['Review_like']=row[16]
                                yield(item)

        self.driver.quit()
