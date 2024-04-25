import time, csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from scrapy import Selector
options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
serv = Service("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=options)
urls={"UK":"https://www.portakabin.com/gb-en/our-visitor-centres/?SearchTerm=w1u4de&Latitude=54.272337500000006&Longitude=-3.1932690000000004&SortOrder=Proximity&IncludeCaseStudies=false&Marker=","France":"https://www.portakabin.com/fr/nos-agences/?SearchTerm=70123&Latitude=46.7110495&Longitude=1.5457210000000003&SortOrder=Proximity&IncludeCaseStudies=false&Marker=","Belgium":"https://www.portakabin.com/be-fr/nos-agences-locales/?SearchTerm=7906&Latitude=50.505362500000004&Longitude=4.4742485&SortOrder=Proximity&IncludeCaseStudies=false&Marker=","Germany":"https://www.portakabin.com/de/standorte/?SearchTerm=603060&Latitude=51.0844235&Longitude=10.4628365&SortOrder=Proximity&IncludeCaseStudies=false&Marker=","Ireland":"https://www.portakabin.com/ie-en/our-visitor-centres/?SearchTerm=&Latitude=53.2773855&Longitude=-8.0040535&SortOrder=Proximity&IncludeCaseStudies=false&Marker=","Netherlands":"https://www.portakabin.com/nl/onze-vestigingen/?SearchTerm=1098%20sj&Latitude=52.1548335&Longitude=5.278934&SortOrder=Proximity&IncludeCaseStudies=false&Marker=","Luxembourg":"https://www.portakabin.com/lu-de/unsere-besucherzentren/?SearchTerm=&Latitude=49.593488000000015&Longitude=6.225209&SortOrder=Proximity&IncludeCaseStudies=false&Marker="}
with open('akabin.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Country', 'Type', 'Address'])
for k, v in urls.items():
    driver.get(v)
    time.sleep(3)
    content = driver.page_source.encode('utf-8')
    sel = Selector(text=str(content.decode('utf-8')))
    type=sel.xpath('//li[contains(@class, "map-list__list-item")]//p[@class="location-card__type"]/text()').getall()
    address=sel.xpath('//li[contains(@class, "map-list__list-item")]//p[@class="location-card__address"]/text()').getall()
    lis = sel.xpath('//li[contains(@class, "map-list__list-item")]//button/text()').getall()
    for index, value in enumerate(lis):
        typevalue=type[index]
        addressvalue=address[index]
        with open('akabin.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([value, k, typevalue, addressvalue])
    time.sleep(3)
driver.close()