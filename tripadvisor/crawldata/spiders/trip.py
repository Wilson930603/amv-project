import os
import json
import scrapy
import pandas as pd
import urllib.parse
from base64 import b64decode


class TripSpider(scrapy.Spider):
    name = 'trip'
    allowed_domains = ['tripadvisor.com']
    start_urls = ['http://tripadvisor.com/']

    headers = {
        'authority': 'www.tripadvisor.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.tripadvisor.com',
        'referer': 'https://www.tripadvisor.com/',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.134", "Google Chrome";v="114.0.5735.134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-by': 'a8c483bbfbba9bc2e06372387800f268c94ec8833b6b39a45e8407fe3f59d652',
    }
    headers_get = {
        'authority': 'www.tripadvisor.com',
        'accept': 'text/html, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'Application/json; charset=utf-8',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.135", "Google Chrome";v="114.0.5735.135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-puid': 'e60721bd-3759-4eb7-8b09-138b207fe922',
        'x-requested-with': 'XMLHttpRequest',
    }
    include_headers_line = True
    if os.path.exists('output.csv'):
        data = open('output.csv', 'r').readline()
        if data:
            include_headers_line = False
    custom_settings = {
        'CONCURRENT_REQUESTS': 99999999,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 99999999,
        'CONCURRENT_REQUESTS_PER_IP': 99999999,
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
        'ROTATING_PROXY_LIST_PATH': 'proxy_25000.txt',
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 10,
        "FEEDS": {
            "output.csv": {
                "format": "csv",
                "item_export_kwargs": {
                    "include_headers_line": include_headers_line
                }
            }
        },
    }

    def start_requests(self):
        try:
            df = pd.read_csv('output.csv')
            data = df.to_dict('records')
            old_rows = []
            for row in data:
                full_search = f"{row['STR Number']} {row['Hotel Name']} {row['Address 1']} {row['City']} {row['State']}"
                old_rows.append(full_search)
        except:
            old_rows = []

        df = pd.read_excel('hotels.xlsx', sheet_name='Hotel List New')
        data = df.to_dict('records')
        for row in data:
            full_search = f"{row['STR Number']} {row['Hotel Name']} {row['Address 1']} {row['City']} {row['State']}"
            if full_search in old_rows:
                continue
            full_search = row['Hotel Name']
            full_search = urllib.parse.quote(full_search)
            url = f'https://www.tripadvisor.com/Search?q={full_search}&searchSessionId=000aa630fec31e6c.ssid&sid=FBA9C60346CFE618ADA00A21B8EF54A71688463613822&blockRedirect=true&ssrc=m&isSingleSearch=true&locationRejected=true&firstEntry=false'
            yield scrapy.Request(
                url=url,
                headers=self.headers_get,
                callback=self.parse,
                meta={'row': row, 'page': 1, 'full_search': full_search},
                dont_filter=True
            )

    def parse(self, response):
        found = False
        locations = response.xpath('//div[@class="location-meta-block"]/div[@class="address"]')
        for location in locations:
            address = location.xpath('./div[@class="address-text"]/text()').get()
            if not address:
                continue
            if response.meta['row']['Address 1'] in address:
                url = location.xpath('./@onclick').get().split("this, '")[1].split("'")[0]
                url = f'https://www.tripadvisor.com{url}'
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                    callback=self.parse_hotel,
                    meta={'row': response.meta['row']},
                    dont_filter=True
                )
                found = True
                break
        if not found:
            page = response.meta['page']
            if page < 3:
                url = f'https://www.tripadvisor.com/Search?q={response.meta["full_search"]}&searchSessionId=000aa630fec31e6c.ssid&sid=FBA9C60346CFE618ADA00A21B8EF54A71688463613822&blockRedirect=true&ssrc=m&isSingleSearch=true&locationRejected=true&firstEntry=false'
                url += f'&o={page * 30}&rf={page}'
                yield scrapy.Request(
                    url=url,
                    headers=self.headers_get,
                    callback=self.parse,
                    meta={'row': response.meta['row'], 'page': page + 1, 'full_search': response.meta['full_search']},
                    dont_filter=True
                )
            else:
                row = response.meta['row']
                data = {
                    'STR Number': row['STR Number'],
                    'Hotel Name': row['Hotel Name'],
                    'Address 1': row['Address 1'],
                    'City': row['City'],
                    'State': row['State'],
                    'URL': '',
                    'Hotel Name Found': '',
                    'Hotel Website URL': '',
                    'Hotel Phone Number': '',
                    'Avg Rating': '',
                    '# Total Reviews': '',
                    'Hotel Local Ranking': '',
                    'Rating - Location': '',
                    'Rating - Cleanliness': '',
                    'Rating - Service': '',
                    'Rating - Value': '',
                    'GreenLeaders GreenPartner': '',
                    'Traveler\'s Choice': '',
                    'Property Amenities': '',
                    'Room Features': '',
                    'Room Types': '',
                    'Hotel Class': '',
                    'Hotel Style': '',
                    'Location Rating 1': '',
                    'Location Rating 1 Text': '',
                    'Location Rating 1 Detail': '',
                    'Location Rating 2': '',
                    'Location Rating 2 Text': '',
                    'Location Rating 2 Detail': '',
                    'Location Rating 3': '',
                    'Location Rating 3 Text': '',
                    'Location Rating 3 Detail': '',
                    '# 5 Star Ratings': '',
                    '# 4 Star Ratings': '',
                    '# 3 Star Ratings': '',
                    '# 2 Star Ratings': '',
                    '# 1 Star Ratings': '',
                    '# QAs': '',
                    '# Room Types': '',
                    'Popular Mentions': ''
                }
                yield data
    
    def parse_hotel(self, response):
        row = response.meta['row']
        hotel_name = response.xpath('//h1[@id="HEADING"]/text()').get()
        website_url = response.xpath('//div[@data-blcontact="URL_HOTEL ADDITIONAL"]/a/@data-encoded-url').get()
        if website_url:
            website_url = b64decode(website_url).decode()
            website_url = website_url.split('/', 1)[1]
            website_url = f'https://www.tripadvisor.com/{website_url}'
        phone_number = response.xpath('//div[contains(@data-blcontact, "PHONE")]/a/@href').get()
        if phone_number:
            phone_number = phone_number.replace('tel:', '')
        location_rating = None
        cleanliness_rating = None
        service_rating = None
        value_rating = None
        green_partner = 'FALSE'
        traveler_choice = 'FALSE'
        property_amenities = []
        room_features = []
        room_types = []
        hotel_class = None
        hotel_style = None
        avg_rating = None
        total_reviews = None
        local_ranking = None

        about_data = response.xpath('//div[@id="ABOUT_TAB"]/div[contains(@class, "ui_columns")]')
        if about_data:
            about_data = about_data[0]
            left_data = about_data.xpath('./div[1]')[0]
            right_data = about_data.xpath('./div[2]')[0]
            review_data = left_data.xpath('./div[1]')[0]
            avg_rating = review_data.xpath('./span/text()').get()
            total_reviews = review_data.xpath('./a/span[2]/text()').get()
            local_ranking = left_data.xpath('./span/text()').get()
            sub_ratings = left_data.xpath('./div[2]/div')
            for sub_rating in sub_ratings:
                spans = sub_rating.xpath('./span/text()').getall()
                if spans[0] == 'Location':
                    location_rating = spans[1]
                elif spans[0] == 'Cleanliness':
                    cleanliness_rating = spans[1]
                elif spans[0] == 'Service':
                    service_rating = spans[1]
                elif spans[0] == 'Value':
                    value_rating = spans[1]
            green_choice = left_data.xpath('./div[3]//text()').get()
            if green_choice == 'GreenLeaders GreenPartner':
                green_partner = 'TRUE'
            elif green_choice == 'Travelers\' Choice':
                traveler_choice = 'TRUE'
            amenities = right_data.xpath('div[1]/@data-ssrev-handlers').get()
            if amenities:
                amenities = json.loads(amenities)['load'][3].get('amenities')
                if amenities:
                    for e in ['highlightedAmenities', 'nonHighlightedAmenities']:
                        for amenity in amenities[e]['propertyAmenities']:
                            if amenity['amenityNameLocalized']:
                                property_amenities.append(amenity['amenityNameLocalized'])
                        for amenity in amenities[e]['roomFeatures']:
                            if amenity['amenityNameLocalized']:
                                room_features.append(amenity['amenityNameLocalized'])
                        for amenity in amenities[e]['roomTypes']:
                            if amenity['amenityNameLocalized']:
                                room_types.append(amenity['amenityNameLocalized'])
            hotel_class = right_data.xpath('./div[3]/div[1]/div[2]/span/svg/@aria-label').get()
            if hotel_class:
                hotel_class = hotel_class.split(' of ')[0]
            hotel_style = right_data.xpath('./div[3]/div[1]/div/text()').getall()[1:]
            hotel_style = '\n'.join(hotel_style)

        property_amenities = list(set(property_amenities))
        property_amenities = '\n'.join(property_amenities)
        room_features = list(set(room_features))
        room_features = '\n'.join(room_features)
        room_types = list(set(room_types))
        room_types = '\n'.join(room_types)
        locations = response.xpath('//div[@id="LOCATION"]/div[@class="ui_columns "]')
        location_data = [{
            'Rating': None,
            'Text': None,
            'Detail': None,
        } for _ in range(3)]
        if len(locations) == 2:
            location = locations[0].xpath('./div')
            for i, loc in enumerate(location):
                rating = loc.xpath('./span[1]/text()').get()
                text_details = loc.xpath('./span[2]//text()').getall()
                text = text_details[0]
                detail = ''.join(text_details[1:])
                location_data[i]['Rating'] = rating
                location_data[i]['Text'] = text
                location_data[i]['Detail'] = detail
        
        ratings = response.xpath('//div[@id="hrReviewFilters"]/div[1]/div[1]/ul/li/span[2]/text()').getall()

        qas = response.xpath('//div[@id="REVIEWS"]/div//span[@data-test-target="CC_TAB_Questions_LABEL"]/span/span/text()').get()
        room_tips = response.xpath('//div[@id="REVIEWS"]/div//span[@data-test-target="CC_TAB_RoomTips_LABEL"]/span/span/text()').get()
        popular_mentions = response.xpath('//div[@id="hrReviewFilters"]/div[2]//button/text()').getall()[1:]
        popular_mentions = '\n'.join(popular_mentions)

        data = {
            'STR Number': row['STR Number'],
            'Hotel Name': row['Hotel Name'],
            'Address 1': row['Address 1'],
            'City': row['City'],
            'State': row['State'],
            'URL': response.url,
            'Hotel Name Found': hotel_name,
            'Hotel Website URL': website_url,
            'Hotel Phone Number': phone_number,
            'Avg Rating': avg_rating,
            '# Total Reviews': total_reviews,
            'Hotel Local Ranking': local_ranking,
            'Rating - Location': location_rating,
            'Rating - Cleanliness': cleanliness_rating,
            'Rating - Service': service_rating,
            'Rating - Value': value_rating,
            'GreenLeaders GreenPartner': green_partner,
            'Traveler\'s Choice': traveler_choice,
            'Property Amenities': property_amenities,
            'Room Features': room_features,
            'Room Types': room_types,
            'Hotel Class': hotel_class,
            'Hotel Style': hotel_style,
            'Location Rating 1': location_data[0]['Rating'],
            'Location Rating 1 Text': location_data[0]['Text'],
            'Location Rating 1 Detail': location_data[0]['Detail'],
            'Location Rating 2': location_data[1]['Rating'],
            'Location Rating 2 Text': location_data[1]['Text'],
            'Location Rating 2 Detail': location_data[1]['Detail'],
            'Location Rating 3': location_data[2]['Rating'],
            'Location Rating 3 Text': location_data[2]['Text'],
            'Location Rating 3 Detail': location_data[2]['Detail'],
            '# 5 Star Ratings': ratings[0] if len(ratings) > 0 else 0,
            '# 4 Star Ratings': ratings[1] if len(ratings) > 0 else 0,
            '# 3 Star Ratings': ratings[2] if len(ratings) > 0 else 0,
            '# 2 Star Ratings': ratings[3] if len(ratings) > 0 else 0,
            '# 1 Star Ratings': ratings[4] if len(ratings) > 0 else 0,
            '# QAs': qas,
            '# Room Types': room_tips,
            'Popular Mentions': popular_mentions
        }
        yield data
