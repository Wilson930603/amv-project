import scrapy,json,re,os,platform,time,random,sys
from functions import *
from datetime import datetime
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def pass_captcha(url):
    RUN=True
    while RUN:
        e=driver.find_element(By.XPATH,'//div[@class="initial-slider"]')
        PO=e.location
        action = ActionChains(driver)
        action.click_and_hold(e)
        time.sleep(1)
        action.move_by_offset(PO['x']+50, PO['y'])
        time.sleep(1)
        action.release()
        action.perform()
        time.sleep(2)
        e=driver.find_element(By.XPATH,'//div[contains(@class,"robot-page_buttonContinue__")]')
        e.click()
        time.sleep(5)
        e=driver.find_element(By.XPATH,'//a[@id="header-menu-preços"]').click()
        time.sleep(2)
        e=driver.find_element(By.XPATH,'//a[@id="header-menu-preços"]/..//a[@id="header-menu-debêntures"]').click()
        time.sleep(5)
        if 'item-title-0' in driver.page_source:
            E=driver.find_element(By.XPATH,'//a[contains(@id,"item-title-0")]')
            E.click()
            time.sleep(5)
        driver.get(url)
        time.sleep(5)
        if not 'Seu acesso foi negado' in driver.page_source:
            RUN=False

try:
    driver = webdriver.Chrome()
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
URLS=re.split('\r\n|\n',open('urls.txt').read())
START=0
# if os.path.exists('CRAWLED.txt'):
#     No=open('CRAWLED.txt').read()
#     if str(No).isdigit():
#         START=int(No)+1
# open('CRAWLED.txt','w').write(str(START))
# START=START*100
# END=START+100
# print(START,END)
RUN=True
while RUN:
    if START<len(URLS):
        CODE=str(URLS[START]).split('/')[4]
        print(CODE)
        DATA=[]
        file_name='./jsondata/'+CODE+'.json'
        CHK=False
        if not os.path.exists(file_name):
            CHK=True
        #else:
        #    fs=os.stat(file_name)
        #    s=int(fs.st_size / 1024)
        #    if s<=1:
        #        CHK=True
        if CHK==True:
            url=URLS[START]+'?page=1&size=100'
            print(url)
            driver.get(url)
            time.sleep(3)
            if 'Seu acesso foi negado' in driver.page_source:
                print('PASS CAPTCHA')
                pass_captcha(url)
                time.sleep(2)
            if 'pagination-next-button' in driver.page_source:
                PAGE=True
                while PAGE:
                    e=driver.find_element(By.XPATH,'//a[@id="pagination-next-button"]')
                    CLASS=e.get_attribute('class')
                    if not '--disabled' in CLASS:
                        driver.execute_script("arguments[0].scrollIntoView();", e)
                        driver.execute_script("window.scrollTo(0, window.scrollY -200)")
                        e.click()
                        time.sleep(2)
                    else:
                        PAGE=False
            HIS=[]
            for request in driver.requests:
                if request.response:
                    if 'https://data.anbima.com.br/web-bff/v1/debentures/'+CODE+'/precos/pu-historico' in request.url and request.response.status_code==200 and not request.url in HIS:
                        HIS.append(request.url)
                        print('\n ---------------')
                        print(request.url)
                        body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                        Data=json.loads(body.decode('utf-8'))
                        if 'content' in Data and len(Data['content'])>0:
                            DATA+=Data['content']

            open(file_name,'w',encoding='utf-8').write(json.dumps(DATA))
        START+=1
    else:
        RUN=False
driver.quit()