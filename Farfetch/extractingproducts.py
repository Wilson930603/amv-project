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
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
# importing module
import logging
from datetime import datetime
from random import randint

# *|CURSOR_MARCADOR|*
THREAD_COUNT = 2
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

TYPE_RUN = 1
FILE_NAME = 'gude.csv'
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Setting up the logging module to log to a file and to the console.
##loging


class Farfetch:
    def __init__(self, date, url_city, number):
        # Remove all handlers associated with the root self.logger object.
        self.failedLink = []
        file_log = f"app_{date}_Thread_{number}.log"
        self.name = f"Thread_{number}"
        # logging.basicConfig(level=logging.INFO,filename=file_log, filemode='w',format='%(name)s - %(levelname)s - %(message)s')
        self.Successful_download = 0
        # self.logger = logging.getLogger(file_log)
        self.logger = setup_logger(self.name, file_log)
        self.today = datetime.now()
        self.today = datetime.strftime(self.today, "%Y-%m-%d")
        self.today = str(self.today)
        current = str(datetime.now())
        self.logger.info(f"Start - time => {current}")
        self.logger.info(f"Total Links to be scraped : {url_city}")
        self.total_url_city = url_city
        # Reading the proxy_25k.txt file and storing the contents in a list called proxyList.
        self.proxyList = []
        self.dead_proxy = []
        self.driver = ""


        self.downloaded_urls = []
        try:
            self.read_file1()
        except:
            self.downloaded_urls = []

    def saveProductList(self, link, file):
        items = {"link": [], "fileLink": []}
        items["link"].append(link)
        items["fileLink"].append(file)
        if not os.path.exists(f"./productUrls/listing_farfetch_{self.today}_{self.name}_final.csv"):
            pd.DataFrame(items).to_csv(
                f"./productUrls/listing_farfetch_{self.today}_{self.name}_final.csv", index=False
            )
        else:
            pd.DataFrame(items).to_csv(
                f"./productUrls/listing_farfetch_{self.today}_{self.name}_final.csv",
                index=False,
                header=False,
                mode="a",
            )

    def saveCsv(
        self,
        ProductUrl,
        MainCategory,
        Brand,
        ProductCategory,
        ProductSubCategory,
        ProductName,
        Price,
    ):
        items = {
            "ProductUrl": [],
            "MainCategory": [],
            "Brand": [],
            "ProductCategory": [],
            "ProductSubCategory": [],
            "ProductName": [],
            "Price": [],
        }
        items["ProductUrl"].append(ProductUrl)
        items["MainCategory"].append(MainCategory)
        items["Brand"].append(Brand)
        items["ProductCategory"].append(ProductCategory)
        items["ProductSubCategory"].append(ProductSubCategory)

        items["ProductName"].append(ProductName)
        items["Price"].append(Price)

        if not os.path.exists(f"./productData/Data_farfetch_{self.today}_{self.name}_final.csv"):
            pd.DataFrame(items).to_csv(
                f"./productData/Data_farfetch_{self.today}_{self.name}_final.csv", index=False
            )
        else:
            pd.DataFrame(items).to_csv(
                f"./productData/Data_farfetch_{self.today}_{self.name}_final.csv",
                index=False,
                header=False,
                mode="a",
            )

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48"
        )
        return webdriver.Chrome(service = Service('c://chromedriver.exe'),options=options)
        #return webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def read_file1(self):
        if TYPE_RUN == 0:
            df = pd.read_csv(f"./productUrls/Data_farfetch_{self.today}_{self.name}_final.csv")
            self.downloaded_urls = [df.iloc[num]["ProductUrl"] for num in tqdm(range(len(df)))]
        else:
            df = pd.read_csv(f"./productData/Data_farfetch_{self.today}_{self.name}_final.csv")
            self.downloaded_urls = [df.iloc[num]["ProductUrl"] for num in tqdm(range(len(df)))]

    def check_none(self, data):
        if data == None or data == "":
            return "N/A"
        return data

    def extract_productList(self, link, driver, ThreadCount):
        tryCount = 0
        while True:
            try:
                if tryCount == 5:
                    self.logger.error(
                        f"Thread Count: {ThreadCount} => Search query: {link}, Failed {tryCount} times, ignoring link"
                    )
                    return driver
                base_url = "https://www.farfetch.com"
                driver.get(link)
                while(True):
                    response = Selector(text=driver.page_source)
                    products = response.xpath(
                            '//ul[@data-testid="product-card-list"]//a[@data-component="ProductCardLink"]/@href'
                        ).extract()
                    
                    for product in products:
                        self.saveProductList(base_url + product, link)
                    try:
                        driver.find_element(by.XPATH,'//a[@data-testid="page-next"]').click()
                    except Exception:
                        break
                return driver
            except (Exception, WebDriverException, TimeoutException) as e:
                self.logger.error(
                    f"Thread Count: {ThreadCount} => Search query: {link}, Failed. Trying again : {e}"
                )
                tryCount += 1

    def extract_product(self, link, driver, ThreadCount):
        tryCount = 0
        while True:
            try:
                if tryCount == 5:
                    self.logger.error(
                        f"Thread Count: {ThreadCount} => Search query: {link}, Failed {tryCount} times, ignoring link"
                    )
                    return driver, False
                driver.get(link)
                response = Selector(text=driver.page_source)
                if response.xpath('//h1[text()="429 Too Many Requests"]'):
                    tryCount+=1
                    self.logger.error(
                        f"Thread Count: {ThreadCount} <Error 429> => Search query: {link}, Failed {tryCount} times"
                    )
                    continue
                brand = response.xpath("//h1/a/text()").get()
                productName = response.xpath(
                    '//p[@data-testid="product-short-description"]/text()'
                ).get()
                productUrl = link
                price = response.xpath(
                    '//p[@data-component="PriceLarge"]/text()|//p[@data-component="PriceFinalLarge"]/text()'
                ).get()
                mainCategory = response.xpath(
                    '//a[@data-type="department"]/text()'
                ).get()
                productCategory = response.xpath(
                    '//a[@data-type="category"]/text()'
                ).get()
                productSubCategory = response.xpath(
                    '//a[@data-type="subcategory"]/text()'
                ).get()
                self.saveCsv(
                    link,
                    self.check_none(mainCategory),
                    self.check_none(brand),
                    self.check_none(productCategory),
                    self.check_none(productSubCategory),
                    self.check_none(productName),
                    self.check_none(price),
                )
                return driver, True
            except (Exception, WebDriverException, TimeoutException) as e:
                self.logger.error(
                    f"Thread Count: {ThreadCount} => Search query: {link}, Failed. Trying again : {e}"
                )
                tryCount += 1

    def check_exsist(self, url):
        if url.strip() in self.downloaded_urls:
            return True
        else:
            return False

    def main_func_products(self, links, ThreadCount):
        failedUrls = 0
        driver = self.get_driver()
        for i in range(len(links)):
            if self.check_exsist(links[i]):
                self.Successful_download += 1
                self.logger.info(
                    f"Thread Count: {ThreadCount} => Search query: {links[i]}, Already Available moving to the next urls."
                )
                self.logger.info(
                    f"Thread Count: {ThreadCount} => Already Available downloaded/total {self.Successful_download}/{self.total_url_city}"
                )
                continue
            driver, check_link = self.extract_product(links[i], driver, ThreadCount)
            if check_link:
                self.logger.info(
                    f"Thread Count: {ThreadCount} => Search query: {links[i]}, Completed and scraped"
                )
                self.Successful_download += 1
                self.logger.info(
                    f"Thread Count: {ThreadCount} => downloaded/total {self.Successful_download}/{self.total_url_city}"
                )
            else:
                self.failedLink.append(links[i])
                failedUrls += 1
                self.logger.error(
                    f"Thread Count: {ThreadCount} => Search query: {links[i]}, Failed"
                )
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            self.logger.error(
                f"Thread Count: {ThreadCount} => Finished, close/quit exception: {e}"
            )

        self.logger.info(
            f"Thread Count: {ThreadCount} => Finished downloaded/total {self.Successful_download}/{self.total_url_city}"
            f"Thread Count: {ThreadCount} => Failed downloaded {failedUrls}"
        )
        if failedUrls > 0:
            for failed in self.failedLink:
                self.logger.error(f"Thread Count: {ThreadCount} => {failed}")
        handlers = self.logger.handlers[:]
        for handler in handlers:
            self.logger.removeHandler(handler)
            handler.close()

    def main_func_listing(self, links, ThreadCount):
        driver = self.get_driver()
        for i in range(len(links)):
            if self.check_exsist(links[i]):
                self.logger.info(
                    f"Thread Count: {ThreadCount} => Search query: {links[i]}, Already Available moving to the next urls."
                )
                self.Successful_download += 1
                self.logger.info(
                    f"Thread Count: {ThreadCount} downloaded/total {self.Successful_download}/{self.total_url_city} => Search query: {links[i]}, Already Available moving to the next urls."
                )
                continue
            driver = self.extract_productList(links[i], driver, ThreadCount)
            self.logger.info(
                f"Thread Count: {ThreadCount} => Search query: {links[i]}, Completed and scraped"
            )
            self.Successful_download += 1
            self.logger.info(
                f"Thread Count: {ThreadCount} => downloaded/total {self.Successful_download}/{self.total_url_city}"
            )
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            self.logger.error(
                f"Thread Count: {ThreadCount} => Finished, close/quit exception: {e}"
            )

        self.logger.info(
            f"Thread Count: {ThreadCount} => Finished downloaded/total {self.Successful_download}/{self.total_url_city}"
        )
        handlers = self.logger.handlers[:]
        for handler in handlers:
            self.logger.removeHandler(handler)
            handler.close()


import numpy as np

urls_city = []
today = datetime.now()
today = datetime.strftime(today, "%Y-%m-%d")
today = str(today)


def read_file():
    global urls_city
    filename = FILE_NAME
    df = pd.read_csv(filename)
    urls_city = [df.iloc[num]["link"] for num in tqdm(range(len(df)))]


read_file()
arr = np.array_split(urls_city, THREAD_COUNT)
objects = []

for i in range(THREAD_COUNT):
    objects.append(Farfetch(today, len(arr[i]), i))
threads = []
if TYPE_RUN == 0:
    print('Running in extracting product URLs')
    for i in range(THREAD_COUNT):
        t = threading.Thread(
            target=objects[i].main_func_listing,
            args=(
                arr[i],
                i,
            ),
        )
        threads.append(t)
else:
    for i in range(THREAD_COUNT):
        t = threading.Thread(
            target=objects[i].main_func_products,
            args=(
                arr[i],
                i,
            ),
        )
        threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()

output = open(f"app_{today}.log", "w")
data = ""
for i in range(THREAD_COUNT):
    file = open(f"app_{today}_Thread_{i}.log", "r")
    data = file.readlines()
    file.close()
    output.writelines(data)
output.close()
import os

for i in range(THREAD_COUNT):
    file = f"app_{today}_Thread_{i}.log"
    if os.path.exists(file):
        os.remove(file)

def merge_csv(files,prev_path,file_name):
    merged_data = pd.DataFrame()
    # Loop through each CSV file and merge its data with the existing data
    for file in files:
        print(productUrls_path+file)
        df = pd.read_csv(prev_path+file)
        merged_data = pd.concat([merged_data, df], ignore_index=True)
    merged_data.fillna('N/A',inplace=True)
    # Write the merged data to a new CSV file
    merged_data.to_csv(prev_path+file_name, index=False)

productUrls_path = 'productUrls/'
productUrls_files = os.listdir(productUrls_path)
merge_csv(productUrls_files,productUrls_path,f'listing_{today}.csv')

product_data_path = 'productData/'
product_data_files = os.listdir(product_data_path)
merge_csv(product_data_files,product_data_path,f'product_data_{today}.csv')

