from scrapy import Request, Selector,Spider

import pandas as pd
import json
from datetime import datetime
import os
try:
    from ..items import SocialbladeItem_facebook
    from ..items import SocialbladeItem_youtube
except:
    from items import SocialbladeItem_facebook
    from items import SocialbladeItem_youtube
from random import randint
class Spider_socialBlade(Spider):
    name = 'socialBlade'
    start_url_facebook = "https://socialblade.com/facebook/page/{brand}/monthly"
    start_url_youtube = "https://socialblade.com/youtube/user/{brand}/monthly"
    start_url_base_youtube = "https://socialblade.com/youtube/"
    download_delay = 1.5
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

    headers_main = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://www.google.com/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agents[randint(0,len(user_agents)-1)],
        'Cookie': 'audience=new-user;'
    }
    def __init__(self):
        df = pd.read_csv('./inputData/chanels.csv')
        self.brands = [df.iloc[i]['Brand'] for i in range(len(df))]
        self.urlNames = [df.iloc[i]['urls'] for i in range(len(df))]
    def check_none(self,data):
        """
        If the data is None or an empty string, return 'N/A', otherwise return the data
        
        :param data: The data to be checked
        :return: the data if it is not None or empty.
        """
        if data == None or data == '':
            return 'N/A'
        return data
    def start_requests(self):

        for itr,brand in enumerate(self.brands):
            newUrl = self.urlNames[itr]
            if '/facebook/' in self.urlNames[itr]:
                yield Request(newUrl,callback=self.parse_facebook,dont_filter=True,headers=self.headers_main, meta={'brand':brand})
            elif '/youtube/' in self.urlNames[itr]:
                yield Request(newUrl,callback=self.parse_youtube,dont_filter=True,headers=self.headers_main, meta={'brand':brand})
            #     break
    def parse_youtube(self,response):
        brand = response.meta.get('brand')

        uploads = response.xpath('//span[contains(@id,"youtube-stats-header-uploads")]/text()').get()
        subCount = response.xpath('//span[contains(@id,"youtube-stats-header-subs")]/text()').get()
        videoViews = response.xpath('//span[contains(@id,"youtube-stats-header-views")]/text()').get()
        country = response.xpath('//span[contains(@id,"youtube-stats-header-country")]/text()').get()
        channelType = response.xpath('//span[contains(@id,"youtube-stats-header-channeltype")]/text()').get()
        dateCreated = response.xpath('//span[contains(text(),"User Created")]/../span//text()').extract()
        script = response.xpath('//script[contains(text(),"subscribers")]/text()').get()
        if len(dateCreated)==2:
            dateCreated = dateCreated[-1]

        try:
            data = script.split('Highcharts.chart')
            mothlyVideo = None
            mothlySubs = None
            for i in data:
                if 'graph-youtube-monthly-vidviews-container' in i:
                    mothlyVideo = i
            
            

            for i in data:
                if 'graph-youtube-monthly-subscribers-container' in i:
                    mothlySubs = i
            
            if mothlyVideo:
                mothlyVideo = mothlyVideo.split('data: ')[-1].split('navigation')[0].strip()[:-3].strip()
            if mothlySubs:
                mothlySubs = mothlySubs.split('data: ')[-1].split('navigation')[0].strip()[:-3].strip()
        except:

            mothlyVideo = None
            mothlySubs = None
        items = SocialbladeItem_youtube()
        items['Brand'] = self.check_none(brand)
        items['Website'] = 'Youtube'
        items['Uploads'] = self.check_none(uploads)
        items['Subcribers'] = self.check_none(subCount)
        items['VideoViews'] = self.check_none(videoViews)
        items['country'] = self.check_none(country)
        items['ChannelType'] = self.check_none(channelType)
        items['UserCreated'] = self.check_none(dateCreated)
        items['subscriberOverTime'] = self.check_none(mothlySubs)
        items['videoOverTime'] = self.check_none(mothlyVideo)
        #items['url'] = response.url
        yield items
    
    def parse_facebook(self,response):
        brand = response.meta.get('brand')

        pageLikes = response.xpath('//p[contains(text(),"page likes")]/text()').get()
        if pageLikes:
            pageLikes = pageLikes.strip().split()[0]
        
        pageTalking = response.xpath('//p[contains(text(),"talking about this")]/text()').get()
        if pageTalking:
            pageTalking = pageTalking.strip().split()[0]
        script = response.xpath('//script[contains(text(),"likes")]/text()').get()

        try:
            data = script.split('Highcharts.chart')
            mothlyLikes = None
            mothlyTalks = None
            for i in data:
                if 'graph-facebook-monthly-likes-container' in i:
                    mothlyLikes = i
            
            

            for i in data:
                if 'graph-facebook-monthly-uploads-container' in i:
                    mothlyTalks = i
            
            if mothlyLikes:
                mothlyLikes = mothlyLikes.split('data: ')[-1].split('navigation')[0].strip()[:-3].strip()
            if mothlyTalks:
                mothlyTalks = mothlyTalks.split('data: ')[-1].split('navigation')[0].strip()[:-3].strip()
        except:

            mothlyLikes = None
            mothlyTalks = None
        items = SocialbladeItem_facebook()
        items['Brand'] = self.check_none(brand)
        items['Website'] = 'Facebook'
        items['Page_likes'] = self.check_none(pageLikes)
        items['Talking_about'] = self.check_none(pageTalking)
        items['TotalLikes_monthly'] = self.check_none(mothlyLikes)
        items['TotalTalking_monthly'] = self.check_none(mothlyTalks)

        yield items