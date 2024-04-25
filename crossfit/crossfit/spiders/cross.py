import os
import scrapy
import pandas as pd


class CrossSpider(scrapy.Spider):
    name = 'cross'
    start_urls = ['https://map.crossfit.com/getAllAffiliates.php']
    include_headers_line = True
    if os.path.exists('data.csv'):
        data = open('data.csv', 'r').readline()
        if data:
            include_headers_line = False
    custom_settings = {
        "FEEDS": {
            "data.csv": {
                "format": "csv",
                "item_export_kwargs": {
                    "include_headers_line": include_headers_line
                }
            }
        },
    }

    def parse(self, response):
        try:
            df = pd.read_csv('data.csv')
            data = df.to_dict('records')
            old_rows = []
            for row in data:
                old_rows.append(str(row['ID']))
        except:
            old_rows = []
        data = response.json()
        for item in data:
            lat, lon, cross_id = item[0], item[1], item[3]
            if str(cross_id) in old_rows:
                continue
            yield scrapy.Request(
                url=f"https://map.crossfit.com/getAffiliateInfo.php?aid={cross_id}",
                callback=self.parse_crossfit,
                meta={"id": cross_id, "lat": lat, "lon": lon}
            )

    def parse_crossfit(self, response):
        data = response.json()
        meta = response.meta
        yield {
            "ID": meta['id'],
            "Name": data['name'],
            "Website": data['website'],
            "Address": data['address'],
            "City": data['city'],
            "State": data['state'],
            "Zip": data['zip'],
            "Country": data['country'],
            "Phone": data['phone'],
            "Latitute": meta['lat'],
            "Longitude": meta['lon'],
        }
