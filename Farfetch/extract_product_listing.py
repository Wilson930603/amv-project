# Importing the required modules.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By as by
from time import sleep
from scrapy import Selector
import pandas as pd
from scrapy import Selector
from selenium.webdriver.chrome.service import Service
import threading
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
# importing module
import logging
from datetime import datetime
from random import randint
import pickle

def get_driver():
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-webgl")
    return webdriver.Chrome(ChromeDriverManager().install(),options=options)

driver = get_driver()
fd = pd.read_csv('main_category.csv')
links = [fd.iloc[i]['link'] for i in range(len(fd))]

data = {'links':[]}
for link in tqdm(links):
    driver.get(link)
    base_url = "https://www.farfetch.com"
    response = Selector(text=driver.page_source)
    subBrands = response.xpath("//main//ul/li/a/@href").extract()
    for listing in subBrands:
        data['link'].append(base_url+listing)

file_name = 'product_listing.csv'
if not os.path.exists(file_name):
    pd.DataFrame(data).to_csv(file_name,index=False)
else:
    pd.DataFrame(data).to_csv(file_name,index=False,header=False,mode='a')