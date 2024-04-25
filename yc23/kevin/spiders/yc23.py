import scrapy,json,csv,os, requests
from os import path
class CrawlerSpider(scrapy.Spider):
    name = 'yc23'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.ycombinator.com/',
        'content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.ycombinator.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }

    data = '{"requests":[{"indexName":"YCCompany_production","params":"facetFilters=%5B%5B%22batch%3AW23%22%5D%5D&facets=%5B%22top_company%22%2C%22top_company_by_revenue%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22highlight_black%22%2C%22highlight_latinx%22%2C%22highlight_women%22%2C%22batch%22%2C%22industries%22%2C%22subindustry%22%2C%22regions%22%2C%22tags_highlighted%22%2C%22tags%22%2C%22status%22%2C%22app_video_public%22%2C%22demo_day_video_public%22%2C%22app_answers%22%2C%22question_answers%22%5D&hitsPerPage=1000&maxValuesPerFacet=1000&page=0&query=&tagFilters="},{"indexName":"YCCompany_production","params":"analytics=false&clickAnalytics=false&facets=batch&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="}]}'
    products=[]
    def start_requests(self):
        url='https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.11.3)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=Zjk5ZmFjMzg2NmQxNTA0NGM5OGNiNWY4MzQ0NDUyNTg0MDZjMzdmMWY1NTU2YzZkZGVmYjg1ZGZjMGJlYjhkN3Jlc3RyaWN0SW5kaWNlcz1ZQ0NvbXBhbnlfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVEJmFuYWx5dGljc1RhZ3M9JTVCJTIyeWNkYyUyMiU1RA%3D%3D'
        if path.exists("yc23.csv"):
            os.remove("yc23.csv")
        with open('yc23.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["url", "tags", "name", "website", "short_description", "description", "year_founded","team_size", "location", "linkedin"]
            writer.writerow(field)
        yield scrapy.Request(url,callback=self.get_listing, method='POST', headers=self.headers,cookies='', body = self.data,dont_filter=True)
    def get_listing(self,response):
        Data=json.loads(response.text)
        url=""
        tags=""
        website=""
        name=""
        short_description=""
        description=""
        year_founded=""
        team_size=""
        location=""
        linkedin=""
        i=0
        for item in Data['results'][0]['hits']:
            url="https://www.ycombinator.com/companies/"+item['slug']
            # url="https://www.ycombinator.com/companies/vaero"
            tags=""
            for tag in item['tags']:
                tags+=tag+"\n"
            tags="W23"+"\n"+"ACTIVE"+"\n"+tags.upper()
            website=item['website']
            name=item['name']
            short_description=item['one_liner']
            description=item['long_description']            
            htmldetail = requests.get(url)
            id=htmldetail.text.split('<div id="CompaniesShowPage-react-component-')[1].split('">')[0]
            script=htmldetail.text.split('<script type="application/json" class="js-react-on-rails-component" data-component-name="CompaniesShowPage" data-dom-id="CompaniesShowPage-react-component-'+id+'">')[1].split('</script>')[0]
            Data=json.loads(script)
            year_founded=Data['company']['year_founded']
            team_size=item['team_size']
            location=Data['company']['location']
            linkedin=Data['company']['linkedin_url']
            with open('yc23.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([url, tags, name, website, short_description, description, year_founded, team_size, location, linkedin])