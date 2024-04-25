from random import randint
from requests.exceptions import ProxyError
import pandas as pd
from datetime import datetime

proxyList = []
def check_none(data):
        """
        If the data is None or an empty string, return 'N/A', otherwise return the data
        
        :param data: The data to be checked
        :return: the data if it is not None or empty.
        """
        if data == None or data == '':
            return 'N/A'
        return data 
with open("proxy.txt") as file:
    for line in file:
        line = line.strip() #or some other preprocessing
        proxyList.append(line) 
desc = []
def read_file():
    global desc, topics
    df = pd.read_csv('links_users.csv',encoding = "ISO-8859-1")
    desc = [df.iloc[num]['links'] for num in range(len(df))]
read_file()
file_path = 'Users_data.csv'
import requests
import threading
from scrapy import Selector
import os
mutex = threading.Lock()
def getLinks(links,topics=None):
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
            result = requests.request('GET',links,proxies=proxies,timeout=10)
            if result.status_code == 404:
                return
            if result.status_code !=200:
                print(f'{result.status_code}')
                continue
            response = Selector(text=result.text)
            break    
        except ProxyError as ex:
            print(f'{ex}- trying again')
        except Exception as ex:
            print(f'{ex}: Trying again')
    mutex.acquire()
    na = 'N/A'
    try:
        memberFor = response.xpath('//div[contains(@class,"flex--item")]//ul//li//span/@title').get()
            
        timestamp = datetime.strptime(memberFor, '%Y-%m-%d %H:%M:%S%z')
        now = datetime.now(timestamp.tzinfo)

        delta = now - timestamp

        years = delta.days // 365
        months = delta.days % 365 // 30
    except:
        memberFor = na
    item = {'URL':[],'Years':[],'Months':[]}

    item['URL'].append(result.url)
    item['Years'].append(check_none(years))
    item['Months'].append(check_none(months))

    print(item)
    if not os.path.exists(file_path):
        pd.DataFrame(item).to_csv(file_path,index=False)
    else:
        pd.DataFrame(item).to_csv(file_path,index=False,header=False,mode='a')
    mutex.release()

threads = []
thread_count = 1000
t_count = 0

for count,i in enumerate(desc):
    print(f'Number: {count}: {i}')
    t = threading.Thread(target=getLinks, args=(i,))
    threads.append(t)
    t_count+=1
    if t_count==thread_count:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        threads = []
        t_count = 0
    
    #break
if t_count!=0:
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads = []
    t_count = 0
