import datetime
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
from parsel import Selector
import time
driver_path = ChromeDriverManager().install()
formurl = []
START_URL = 'https://forums.oracle.com/ords/apexds/domain/dev-community/category/infrastructure-software?tags=oracle-linux'
def getdriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = Chrome(
        executable_path=driver_path,
        options=chrome_options)
    return driver
def getQuestionUrls(driver):
    driver.get(START_URL)
    urls= []
    nextpage = 'Not None'
    while nextpage!=None:
        try:
            nextpage = WebDriverWait(driver,20).until(EC.presence_of_element_located((by.XPATH,'//a[@title="Next"]')))
        except Exception:
            nextpage = None
        response = Selector(text=driver.page_source)
        for forum in response.xpath("//ul[@data-region-id = 'questions_rpt']/li"):
            forumurl = forum.xpath("./div/div/div/div/a/@href").get()
            urls.append(forumurl)
        if nextpage != None:
            nextpage.click()
            time.sleep(3)
    return urls

driver = getdriver()
formurl = getQuestionUrls(driver)
driver.close()
retryurl = []
item = {'URL':[],'User':[]}
driver = getdriver()
for url in formurl:
    print(url)
    print(formurl.index(url))
    print("--------------------------")
    time.sleep(randint(5,10))
    driver.get(url)
    try:
        wait =WebDriverWait(driver,20).until(EC.presence_of_element_located((by.XPATH,"//span[@class = 'ds-User-name']/a")))
    except Exception:
        retryurl.append(url)
    response = Selector(driver.page_source)
    user = response.xpath("//span[@class = 'ds-User-name']/a/text()").extract()
    userurl = response.xpath("//span[@class = 'ds-User-name']/a/@href").extract()
    
    for i in range(0,len(user)):        
        item['User'].append(user[i])
        item['URL'].append(userurl[i])
        
driver.close()
driver = getdriver()
for url in retryurl:
    print(url)
    print(retryurl.index(url))
    print("--------------------------")
    time.sleep(randint(5,10))
    driver.get(url)
    try:
        wait =WebDriverWait(driver,20).until(EC.presence_of_element_located((by.XPATH,"//span[@class = 'ds-User-name']/a")))
    except Exception:
        pass
    response = Selector(driver.page_source)
    user = response.xpath("//span[@class = 'ds-User-name']/a/text()").extract()
    userurl = response.xpath("//span[@class = 'ds-User-name']/a/@href").extract()
    
    for i in range(0,len(user)):        
        item['User'].append(user[i])
        item['URL'].append(userurl[i])
        
driver.close()

import pandas as pd
df = pd.DataFrame(item)
df.to_csv("oraclelinux_{}.csv".format(str(datetime.datetime.now().date()).replace('-','')),index=False)