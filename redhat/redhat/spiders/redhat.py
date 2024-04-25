from scrapy import Request, Selector,Spider
from ..items import RedhatItem
from random import randint

class Spider_REDHAT(Spider):
    name = 'redhat'
    base_url = 'https://access.redhat.com'
    start_urls = ["https://access.redhat.com/discussions?keyword=&name=&product=25&tags=All&field_internal_tags_tid=All"]
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

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       
        'upgrade-insecure-requests': '1',
        'user-agent': user_agents[randint(0,len(user_agents)-1)],
    }

    def start_requests(self):
        
        for url in self.start_urls:
            yield Request(url,callback=self.form_page,headers=self.headers)
    
    def form_page(self,response):

        question_links = [self.base_url+x for x in response.xpath('//h3[@class="field-content"]/a/@href').extract()]

        for question in question_links:

            yield Request(question,callback=self.information,headers=self.headers)
        
        next_page = response.xpath('//a[@title ="Go to next page"]/@href').get()
        if next_page:
            yield Request(self.base_url+next_page,callback=self.form_page,headers=self.headers)
    def information(self,response):
        item = RedhatItem()
        main_question = response.xpath('//a[@class="username"]')
        item['URL'] = self.base_url+main_question.xpath('./@href').get(default='NA')
        item['User'] = main_question.xpath('./text()').get(default='NA')
        yield item
        user_responses = response.xpath('//a[@class="user-name"]')
        for user in user_responses:
            item = RedhatItem()
            item['URL'] = self.base_url+user.xpath('./@href').get(default='NA')
            item['User'] = user.xpath('./text()').get(default='NA')
            yield item

        