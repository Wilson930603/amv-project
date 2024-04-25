from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from time import sleep
from selenium.webdriver.support.ui import Select
from scrapy import Selector
from random import randint
from selenium.common.exceptions import TimeoutException   
from datetime import datetime
import pandas as pd
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from random import randint
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


df = pd.read_csv('./inputData/brands.csv')
brands = [df.iloc[i]['Brand'] for i in range(len(df))]
urlNames = [df.iloc[i]['urlsName'] for i in range(len(df))]

def get_driver():
    options = webdriver.ChromeOptions()
    user_data_dir = r"E:\Mubashir\User Data"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    options.add_argument(f'user-data-dir={user_data_dir}')
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
driver.get('https://socialblade.com/login')

#Enter Username and password for social bald to access instagram data
username = ''
password = ''
driver.find_element(by.XPATH,'//input[contains(@name,"dashboard_email")]').send_keys(username)
sleep(.2)
driver.find_element(by.XPATH,'//input[contains(@name,"dashboard_pass")]').send_keys(password)
sleep(.2)
driver.find_element(by.XPATH,'//input[contains(@value,"LOGIN")]').click()

start_url_instagram = "https://socialblade.com/instagram/user/{brand}/monthly"
df = pd.read_csv('./inputData/chanels.csv')
brands = [df.iloc[i]['Brand'] for i in range(len(df))]
urlNames = [df.iloc[i]['urls'] for i in range(len(df))]

def save_csv(Brand,mediaUploads,followers,following,engagement,avgLikes,avgComments,followersOverTime,file_name='socialBlade_instagram.csv'):
    items = {
        'Brand':[],
        'Website':[],
        'mediaUploads':[],
        'followers':[],
        'following':[],
        'engagement':[],
        'avgLikes':[],
        'avgComments':[],
        'followersOverTime':[],
    }
    items['Brand'].append(Brand)
    items['Website'].append('Instagram')
    items['mediaUploads'].append(mediaUploads)
    items['followers'].append(followers)
    items['following'].append(following)
    items['engagement'].append(engagement)
    items['avgLikes'].append(avgLikes)
    items['avgComments'].append(avgComments)
    items['followersOverTime'].append(followersOverTime)
    if not os.path.exists(file_name):
        pd.DataFrame(items).to_csv(file_name,index=False)
    else:
        pd.DataFrame(items).to_csv(file_name,index=False,header=False,mode='a')

for itr,brand in enumerate(brands):
    if '/instagram/' not in urlNames[itr]:
        continue
    newUrl = urlNames[itr]
    driver.get(newUrl)
    response = Selector(text=driver.page_source)
    script = response.xpath('//script[contains(text(),"followers")]/text()').get()
    try:
        data = script.split('Highcharts.chart')
        instaFollowers = None
        for i in data:
            if 'graph-instagram-monthly-followers-container' in i:
                instaFollowers = i
        
        if instaFollowers:
            instaFollowers = instaFollowers.split('data: ')[-1].split('navigation')[0].strip()[:-3].strip()
        else:
            instaFollowers = 'NA'
            
    except:

        instaFollowers = 'NA'
    
    mediaUploads = response.xpath('//span[contains(text(),"Media Uploads")]/../span/text()').extract()
    if len(mediaUploads) == 0:
        mediaUploads = 'NA'
    elif len(mediaUploads) == 2:
        mediaUploads = mediaUploads[-1]

    followers = response.xpath('//span[contains(text(),"Followers")]/../span/text()').extract()
    if len(followers) == 0:
        followers = 'NA'
    elif len(followers) == 2:
        followers = followers[-1]
    
    following = response.xpath('//span[contains(text(),"Following")]/../span/text()').extract()
    if len(following) == 0:
        following = 'NA'
    elif len(following) == 2:
        following = following[-1]

    engagementRate = response.xpath('//span[contains(text(),"Engagement Rate")]/../span/text()').extract()
    if len(engagementRate) == 0:
        engagementRate = 'NA'
    elif len(engagementRate) == 2:
        engagementRate = engagementRate[-1].strip()

    avgLikes = response.xpath('//span[contains(text(),"AVG Likes")]/../span/text()').extract()
    if len(avgLikes) == 0:
        avgLikes = 'NA'
    elif len(avgLikes) == 2:
        avgLikes = avgLikes[-1]

    avgComments = response.xpath('//span[contains(text(),"AVG Comments")]/../span/text()').extract()
    if len(avgComments) == 0:
        avgComments = 'NA'
    elif len(avgComments) == 2:
        avgComments = avgComments[-1]
    
    save_csv(brand,mediaUploads,followers,following,engagementRate,avgLikes,avgComments,instaFollowers,file_name='socialBlade_instagram.csv')
    sleep(3)
    

driver.close()