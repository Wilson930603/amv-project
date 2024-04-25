from random import randint
from requests.exceptions import ProxyError
import pandas as pd
proxyList = []
with open("proxy.txt") as file:
    for line in file:
        line = line.strip() #or some other preprocessing
        proxyList.append(line) 
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/100.0.100.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/604.1 Edg/100.0.100.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edge/18.19042',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/65.0.3467.48',
    'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
]   
file_path = 'links_users.csv'
question_pages = 8020
user_pages = 37423
import requests
import threading
from scrapy import Selector
import os
mutex = threading.Lock()
start_url = ['https://askubuntu.com/questions?tab=newest&page={page}', 'https://askubuntu.com/users?page={page}&tab=reputation&filter=all']
def getLinks(links):
    global mutex
    base_url = 'https://askubuntu.com'
    while True:
        PROXY= proxyList[randint(0,len(proxyList)-1)]
        try:
            proxies = { 
            "http"  : PROXY, 
            "https" : PROXY, 
            "ftp"   : PROXY
            }
            headers = {
                'user-agent': user_agents[randint(0,len(user_agents)-1)],
            }
            result = requests.request('GET',links,proxies=proxies,headers=headers)
            # result = requests.request('GET',links,headers=headers)
            if result.status_code !=200:
                continue
            response = Selector(text=result.text)
            break    
        except ProxyError as ex:
            print(f'{ex}- trying again')
    data = response.xpath('//div[contains(@id,"user-browser")]//div[contains(@class,"grid--item user-info")]')
    
    print(len(data))
    mutex.acquire()
    items = {'links': []}
    for user in data:
        user_link = user.xpath('.//div[contains(@class,"user-gravatar48")]//a/@href').get()
        items['links'].append(base_url+user_link)
    if not os.path.exists(file_path):
        pd.DataFrame(items).to_csv(file_path,index=False)
    else:
        pd.DataFrame(items).to_csv(file_path,index=False,header=False,mode='a')
    mutex.release()

threads = []
thread_count = 200
t_count = 0
for i in range(1,user_pages+1):
    seach_url = start_url[1].format(page=str(i))
    t = threading.Thread(target=getLinks, args=(seach_url,))
    threads.append(t)
    t_count+=1
    if t_count==thread_count:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        threads = []
        t_count = 0
    print(f'Number: {i}: {seach_url}')
    #break
if t_count!=0:
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads = []
    t_count = 0
