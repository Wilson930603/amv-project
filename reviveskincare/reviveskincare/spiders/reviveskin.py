
import datetime
import scrapy
import json
import requests
from parsel import Selector
from datetime import datetime
class ReviveskincareSpider(scrapy.Spider):
    name = 'reviveskincare'
    allowed_domains = ['x']
    start_urls = ['https://reviveskincare.com/collections/best-sellers/products/moisturizing-renewal-day-cream-spf-30-broad-spectrum-uva-uvb-sunscreen-pa',
                'https://reviveskincare.com/collections/best-sellers/products/moisturizing-renewal-hydrogel-hydration-hyaluronic-acid-serum',
                'https://reviveskincare.com/collections/best-sellers/products/moisturizing-renewal-cream',
                'https://reviveskincare.com/collections/best-sellers/products/intensite-volumizing-serum-ultime-targeted-skin-filler',
                'https://reviveskincare.com/collections/best-sellers/products/peau-magnifique-serum-nightly-youth-renewal-activator',
                'https://reviveskincare.com/collections/best-sellers/products/perfectif-night-even-skin-tone-cream-retinol-dark-spot-corrector',
                'https://reviveskincare.com/collections/best-sellers/products/moisturizing-renewal-eye-cream',
                'https://reviveskincare.com/collections/best-sellers/products/eye-renewal-serum',
                'https://reviveskincare.com/collections/best-sellers/products/masque-des-yeux-instant-de-puffing-gel-eye-mask',
                'https://reviveskincare.com/collections/best-sellers/products/rescue-elixir',
                'https://reviveskincare.com/collections/best-sellers/products/intensite-creme-lustre-night-moisturizer',
                'https://reviveskincare.com/collections/best-sellers/products/fermitif-neck-renewal-cream',
                'https://reviveskincare.com/collections/best-sellers/products/sensitif-renewal-cream',
                'https://reviveskincare.com/collections/best-sellers/products/moisturizing-renewal-lotion-nightly-dual-acid-retexturizer',
                'https://reviveskincare.com/collections/best-sellers/products/soleil-superieur',
                'https://reviveskincare.com/collections/best-sellers/products/foaming-cleanser-enriched-hydrating-wash',
                'https://reviveskincare.com/collections/best-sellers/products/balancing-toner',
                'https://reviveskincare.com/collections/best-sellers/products/intensite-creme-lustre-day-moisturizer',
                'https://reviveskincare.com/collections/best-sellers/products/intensite-les-yeux'
                ]
    headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'pixel=7395d3a2-7c37-4416-466d-0978ce4f0d89',
    'Origin': 'https://reviveskincare.com',
    'Referer': 'https://reviveskincare.com/',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36:'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback = self.parse,)

    def parse(self,response):
        i = 0
        PID = json.loads(response.xpath("//script[@id = '__st']/text()").get().split('=')[-1].split(';')[0]).get('rid')
        Price = response.xpath("//span[@id = 'ProductPrice']/text()").get().replace('$', '').strip()
        Product = response.xpath("//h1[@class = 'product-single__title']/text()").get()
        url = f'https://staticw2.yotpo.com/batch/app_key/IhBjFUnmqTD8rDNiiK99i9jznSi5yAUCYsXpYE0f/domain_key/{PID}/widget/reviews'
        while True:
            i += 1
            payload = {'methods': '[{"method":"reviews","params":{"pid":'+str(PID)+',"order_metadata_fields":{},"widget_product_id":'+str(PID)+',"data_source":"default","page":'+str(i)+',"host-widget":"main_widget","is_mobile":false,"pictures_per_review":10}}]',
                    'app_key': ' IhBjFUnmqTD8rDNiiK99i9jznSi5yAUCYsXpYE0f',
                    'is_mobile': ' false',
                    'widget_version': ' 2022-12-18_11-24-50'}
            response = requests.request("POST", url, headers=self.headers, data=payload,)
            jo = json.loads(response.text)
            sel = Selector(text = jo[0]['result'])
            if sel.xpath("//div[contains(@class,'yotpo-review yotpo-regular-box')]") == []:
                break
            for path in sel.xpath("//div[contains(@class,'yotpo-review yotpo-regular-box')]"):
                
                Names = path.xpath(".//span[@class = 'y-label yotpo-user-name yotpo-font-bold pull-left']/text()").get()
                Date = path.xpath(".//span[contains(@aria-label,'review date')]/text()").get()
                Date = datetime.strptime(Date,"%m/%d/%y").strftime("%m/%d/%Y")
                Ages = path.xpath(".//span[contains(text(),'Age:')]/following-sibling::span/text()").get()
                Gender = path.xpath(".//span[contains(text(),'Gender:')]/following-sibling::span/text()").get()
                SkinConcerns = path.xpath(".//span[contains(text(),'Skin Concerns:')]/following-sibling::span/text()").get()
                SkinType = path.xpath(".//span[contains(text(),'Skin Type:')]/following-sibling::span/text()").get()
                Effectiveness = path.xpath(".//div[contains(text(),'Effectiveness')]/following-sibling::div/div/span[@class = 'sr-only']/text()").get()
                Quality = path.xpath(".//div[contains(text(),'Quality')]/following-sibling::div/div/span[@class = 'sr-only']/text()").get()
                if Quality is not None:
                    Quality = Quality.split('of')[0].strip()
                if Effectiveness is not None:
                    Effectiveness = Effectiveness.split('of')[0].strip()

                ReviewHeading = path.xpath(".//div[@role = 'heading']/text()").get()
                ReviewBody = path.xpath(".//div[@class= 'content-review']/text()").get()
                UpVotes = path.xpath(".//span[@data-type = 'up']/text()").get()
                DownVotes = path.xpath(".//span[@data-type = 'down']/text()").get()
                Stars = path.xpath(".//div[@class = 'yotpo-review-stars ']/span[@class = 'sr-only']/text()").get()
                if Stars is not None:
                    Stars =Stars.split('star')[0].strip()

                items = {}
                items['Product'] = Product
                items['Price'] = Price
                items['Name'] = Names
                items['Rating'] = Stars
                items['Age'] = Ages
                items['Gender'] = Gender
                items['SkinConcerns'] = SkinConcerns
                items['SkinType'] = SkinType
                items['Quality'] = Quality
                items['Effectiveness'] = Effectiveness
                items['Tile'] = ReviewHeading
                items['Review'] = ReviewBody
                items['# Helpfull'] = UpVotes
                items['# Unhelpfull'] = DownVotes
                items['Date'] = Date
                yield items



   
