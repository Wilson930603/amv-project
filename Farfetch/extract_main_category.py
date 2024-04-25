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

driver.get('https://www.farfetch.com/sitemap/')
response = Selector(text=driver.page_source)
base_url = "https://www.farfetch.com"
links = [base_url+x for x in response.xpath('//p[contains(text(),"Categories by brand")]/../ul/li/a/@href').extract()]

data = {'link':links}

file_name = 'main_category.csv'
if not os.path.exists(file_name):
    pd.DataFrame(data).to_csv(file_name,index=False)
else:
    pd.DataFrame(data).to_csv(file_name,index=False,header=False,mode='a')