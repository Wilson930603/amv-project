import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector
from time import sleep
url = "https://platform.cloud.coveo.com/rest/search/v2?sitecoreItemUri=sitecore%3A%2F%2Fweb%2F%7BF6D9D698-B725-4B75-82F2-10DF263FB1A4%7D%3Flang%3Den%26amp%3Bver%3D1&siteName=RSAC-PROD-CD"

payload = "actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222023-03-29T15%3A37%3A25.726Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222023-03-29T15%3A13%3A12.763Z%5C%22%22%7D%5D&referrer=&analytics=%7B%22clientId%22%3A%22a7274737-d616-7ec0-f2b4-a58a1affa690%22%2C%22documentLocation%22%3A%22https%3A%2F%2Fwww.rsaconference.com%2Fmarketplace%2Fsearch%23numberOfResults%3D100%22%2C%22documentReferrer%22%3A%22%22%2C%22pageId%22%3A%22%22%7D&visitorId=a7274737-d616-7ec0-f2b4-a58a1affa690&isGuestUser=false&aq=((%40z95xtemplate%3D%3D9C786508EB8847B2AE85C8E08369B8A4%20((%40z95xpath%3D68F6938DF535413995A50E925A036DCF%20%40z95xid%3C%3E68F6938DF535413995A50E925A036DCF)%20%40showz32xinz32xmarketplace%3D%3DTrue))%20NOT%20%40z95xtemplate%3D%3D(ADB6CA4F03EF4F47B9AC9CE2BA53FF97%2CFE5DD82648C6436DB87A7C4210C7413B))&cq=(%40z95xlanguage%3D%3Den)%20(%40z95xlatestversion%3D%3D1)%20(%40source%3D%3D%22Coveo_web_index%20-%20NEW-PROD%22)&searchHub=Marketplace%20Search%20Hub&locale=en&pipeline=Marketplace%20Query%20Pipeline&maximumAge=900000&wildcards=true&firstResult={page_offset}&numberOfResults=100&excerptLength=200&enableDidYouMean=true&sortCriteria=relevancy&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40marketplaceez120xhibitorcategory%22%2C%22maximumNumberOfValues%22%3A500%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40marketplaceez120xhibitorsubcategory%22%2C%22maximumNumberOfValues%22%3A500%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40industrytopictopics%22%2C%22maximumNumberOfValues%22%3A500%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40industrytopicsubtopics%22%2C%22maximumNumberOfValues%22%3A500%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40ez120xhibitornamefirstletter%22%2C%22maximumNumberOfValues%22%3A31%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&facetOptions=%7B%7D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FKarachi&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"
headers = {
  'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ2OCI6dHJ1ZSwib3JnYW5pemF0aW9uIjoicnNhY3Byb2Q4bXlseTRraiIsInVzZXJJZHMiOlt7InByb3ZpZGVyIjoiRW1haWwgU2VjdXJpdHkgUHJvdmlkZXIiLCJuYW1lIjoiYW5vbnltb3VzIiwidHlwZSI6IlVzZXIifV0sInJvbGVzIjpbInF1ZXJ5RXhlY3V0b3IiXSwiZXhwIjoxNjgwMTkwNjM3LCJpYXQiOjE2ODAxMDQyMzd9.N_AjWeyR8fHnDAkI4zASxBShtbIU5o80W0A9cpqfeAk',
  'Content-Type': 'text/plain'
}
offset = 0
titles= []
for itr in range(5):
    response = requests.request("POST", url, headers=headers, data=payload.format(page_offset=str(offset)))
    data_json = json.loads(response.text)
    for data in data_json["results"]:
        titles.append(data.get("title"))
    offset+=100
def get_driver():
    options = webdriver.ChromeOptions()
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
print(len(titles))
driver = get_driver()
main_search_link ="https://www.rsaconference.com/marketplace/search/"
import csv

def write_to_csv(Name, URL, website, linkedIn, tags, Description, file_path):
    # Define the column names
    fieldnames = ['Name', 'URL', 'Website', 'LinkedIn', 'Tags', 'Description']

    # Open the csv file in append mode and write the header row if the file is empty
    with open(file_path, mode='a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(fieldnames)

        # Write the row to the csv file
        writer.writerow([Name, URL, website, linkedIn, tags, Description])
file_name = "rsa_dataset_29032023.csv"
from tqdm import tqdm
for title in tqdm(titles):
    page_link = main_search_link+title
    driver.get(page_link)
    response = Selector(text=driver.page_source)
    Name = response.xpath('//div[@id="content"]//h5/text()').get(default='NA')
    URL = driver.current_url
    website = response.xpath('//a[contains(text(),"website")]/@href').get(default='NA')
    linkedIn = response.xpath('//a[contains(text(),"LinkedIn")]/@href').get(default='NA')
    tags = ', '.join([x.strip() for x in response.xpath('//span[@class="btn-tag"]/text()').extract()])
    Description = response.xpath('//div[@class="container-fluid panel panel-callout-short"]//p/text()').get(default='NA').strip()
    write_to_csv(Name,URL,website,linkedIn,tags,Description,file_name)
    driver.close()
    driver = get_driver()
