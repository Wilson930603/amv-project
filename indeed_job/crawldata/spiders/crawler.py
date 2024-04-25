import scrapy,json,cloudscraper,re,time,os
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'indeed_job'
    scraper = cloudscraper.create_scraper()
    url='file://D:\\FREELANCER\\indeed_job\\scrapy.cfg'
    domain='https://www.indeed.com'
    def start_requests(self):
        STATES=re.split('\r\n|\n', open('Staties.txt','r').read())
        KEYWORDS=re.split('\r\n|\n', open('Keywords.txt','r').read())
        for State in STATES:
            for Keyword in KEYWORDS:
                url='https://www.indeed.com/jobs?q='+Keyword+'&l='+State+'&start=0'
                # Get first page
                HTML=None
                while HTML is None:
                    try:
                        HTML=self.scraper.get(url)
                    except:
                        print('Wait 3 seconds !!!')
                        time.sleep(3)
                response=scrapy.Selector(text=HTML.text)
                Data=response.xpath('//a[contains(@id,"job_")]')
                Total=str(response.xpath('//div[@class="jobsearch-JobCountAndSortPane-jobCount"]/span[contains(text(),"job")]/text()').get()).split()[0]
                for row in Data:
                    id=row.xpath('./@data-jk').get()
                    link=self.domain + row.xpath('./@href').get()
                    yield scrapy.Request(self.url,callback=self.parse_content,meta={'State':State,'Keyword':Keyword,'id':id,'link':link,'Total':Total},dont_filter=True)
                next_page=response.xpath('//a[@data-testid="pagination-page-next"]/@href').get()
                if next_page:
                    link=self.domain+next_page
                    yield scrapy.Request(self.url,callback=self.parse_nextpage,meta={'State':State,'Keyword':Keyword,'Total':Total,'link':link},dont_filter=True)
    def parse_nextpage(self,response):
        State=response.meta['State']
        Keyword=response.meta['Keyword']
        link=response.meta['link']
        Total=response.meta['Total']
        HTML=None
        while HTML is None:
            try:
                HTML=self.scraper.get(link)
            except:
                print('Wait 3 seconds !!!')
                time.sleep(3)
        response=scrapy.Selector(text=HTML.text)
        Data=response.xpath('//a[contains(@id,"job_")]')
        Total=str(response.xpath('//div[@class="jobsearch-JobCountAndSortPane-jobCount"]/span[contains(text(),"job")]/text()').get()).split()[0]
        for row in Data:
            id=row.xpath('./@data-jk').get()
            link=self.domain + row.xpath('./@href').get()
            yield scrapy.Request(self.url,callback=self.parse_content,meta={'State':State,'Keyword':Keyword,'id':id,'link':link,'Total':Total},dont_filter=True)
        next_page=response.xpath('//a[@data-testid="pagination-page-next"]/@href').get()
        if next_page:
            link=self.domain+next_page
            yield scrapy.Request(self.url,callback=self.parse_nextpage,meta={'State':State,'Keyword':Keyword,'Total':Total,'link':link},dont_filter=True)
    def parse_content(self, response):
        id=response.meta['id']
        State=response.meta['State']
        Keyword=response.meta['Keyword']
        link=response.meta['link']
        Total=response.meta['Total']
        url='https://www.indeed.com/viewjob?viewtype=embedded&jk='+id+'&spa=1'
        Data=None
        while Data is None:
            HTML=self.scraper.get(url)
            try:
                Data=json.loads(HTML.text)['body']
            except:
                print('Wait 3 seconds !!!')
                time.sleep(3)
        HEAD=Data['jobInfoWrapperModel']['jobInfoModel']['jobInfoHeaderModel']
        CONTENT=Data['jobInfoWrapperModel']['jobInfoModel']['sanitizedJobDescription']
        item={}
        item['Search Keyword']=Keyword
        item['State']=State
        item['Job Posting Link']=link
        item['Job Title']=HEAD.get('jobTitle','')
        item['Total Jobs']=Total
        item['Company Name']=HEAD.get('companyName','')
        item['Location']=HEAD.get('formattedLocation','')
        item['Salary']=''
        if Data['salaryInfoModel']:
            item['Salary']=Data['salaryInfoModel'].get('salaryText','')
        item['Job Description']=cleanhtml(CONTENT.get('content',''))
        yield item


