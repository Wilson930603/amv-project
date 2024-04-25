from selenium import webdriver
from selenium.webdriver.common.by import By
import scrapy,time,re
from crawldata.functions import *
from scrapy.exporters import CsvItemExporter

file = open('./Data/twitchtracker.csv', 'wb')
exporter = CsvItemExporter(file, encoding='utf-8-sig')
exporter.start_exporting()

driver = webdriver.Firefox()
driver.maximize_window()

URL_LIST=re.split('\r\n|\n',open('twitchtracker_urls.txt','r',encoding='utf-8').read())
for URL in URL_LIST:
    URL_STR=str(URL).split('~')
    Game=URL_STR[0]
    url=URL_STR[1]
    driver.get(url)
    BLOCK=driver.find_element(By.XPATH,'//section[@id="sbm"]')
    driver.execute_script("arguments[0].scrollIntoView();", BLOCK)
    PAGES=driver.find_element(By.XPATH,'//ul[@class="pagination"]')
    pages=PAGES.find_elements(By.XPATH,'./li/a')
    time.sleep(3)
    pg=0
    while pg<len(pages):
        pg+=1
        DATASET=[]
        HTML="<html>"+BLOCK.get_attribute('innerHTML')+"</html>"
        response=scrapy.Selector(text=HTML)
        for i in range(3):
            TABLE='DataTables_Table_'+str(i)
            Data=response.xpath('//table[@id="'+TABLE+'"]/tbody/tr')
            for R in range(len(Data)):
                row=Data[R]
                td=row.xpath('./td').getall()
                for j in range(len(td)):
                    td[j]=cleanhtml(td[j])
                if i==0:
                    item={}
                    item['Game']=Game
                    item['Month']=td[0]
                    item['Average Concurrent Viewers']=td[1]
                    item['Peak Concurrent Viewers']=td[4]
                    DATASET.append(item)
                elif i==1:
                    DATASET[R]['Average Concurrent Streams']=td[1]
                    DATASET[R]['Peak Concurrent Streams']=td[4]
                else:
                    DATASET[R]['Hours Watched']=td[1]
        for row in DATASET:
            print(row)
            exporter.export_item(row)
        if pg<len(pages):
            PGS=driver.find_elements(By.XPATH,'//ul[@class="pagination"]')
            for PGs in PGS:
                ps=PGs.find_elements(By.XPATH,'./li/a')
                ps[pg].click()
                time.sleep(1)
            BLOCK=driver.find_element(By.XPATH,'//section[@id="sbm"]')
exporter.finish_exporting()
file.close()
driver.quit()