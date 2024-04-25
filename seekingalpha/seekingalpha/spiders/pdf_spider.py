import json
from urllib.parse import urljoin
import scrapy
import pandas as pd


class Seekingalpha_Spider(scrapy.Spider):
    name = 'seekingalpha'
    download_delay = 2.5
    headers = {
    'authority': 'seekingalpha.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'session_id=f3f0da44-ba37-4956-8e07-697ac4286b69; _sasource=; machine_cookie=0941646005974; LAST_VISITED_PAGE=%7B%22pathname%22%3A%22https%3A%2F%2Fseekingalpha.com%2Ffiling%2F7088153%22%2C%22pageKey%22%3A%22fcf9d6b2-9cfd-4a81-8534-8226603f4a2a%22%7D; _gcl_au=1.1.1075990552.1693470960; _uetsid=69bd349047d911ee934951d211718067; _uetvid=69bd5f7047d911eea5cdd170e7a39430; _ga=GA1.1.1404479456.1693470960; sailthru_content=2ebb5e39fdcfcbb5f03494b072c6fcb9; sailthru_visitor=bb0a70a0-0701-4735-a2b1-b947ec4b7d71; _hjSessionUser_65666=eyJpZCI6IjQxZTg4MjViLTAxMmMtNTQ1Yy1hM2JlLWJjZTUyNzJmZTBiMCIsImNyZWF0ZWQiOjE2OTM0NzA5NjA5MDgsImV4aXN0aW5nIjpmYWxzZX0=; _hjHasCachedUserAttributes=true; pxcts=6ae8c7d4-47d9-11ee-9a06-544644546667; _pxvid=6ae8b596-47d9-11ee-9a06-db8f1a4f6117; _pcid=%7B%22browserId%22%3A%22llyww74x11osqyfq%22%7D; _pcus=eyJ1c2VyU2VnbWVudHMiOm51bGx9; __tbc=%7Bkpex%7DA4-swaoEWdP5ffGxfNqnms1KrMVRX_T5hwa8KcjU4YkwA75AfFmA_eSFgY7p3f_X; __pat=-14400000; __pvi=eyJpZCI6InYtMjAyMy0wOC0zMS0xMy0zNi0xNS0wMzctYjJwVGM1U3hubFBGampMNC1hMTJmYTlkMjc2ODRhMTU1NDFlOGQ0OTJmYmUxOWM0NCIsImRvbWFpbiI6Ii5zZWVraW5nYWxwaGEuY29tIiwidGltZSI6MTY5MzQ3MDk3NTY1NH0%3D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXQF8g; xbc=%7Bkpex%7DEUWGdkhVeihjFpsFpji5cMGOTC5M93XQv5RXQJvfAHUqs0Pm1IZMg4VztNgGEIJxLb5Uo2tx5mTd_mb2zVwonisUz6UbllyhI5XoiU7TqlV_3M2SUdCGiwoW5UxJ6THx3hkW6sF7enw0X3QG8jkjyeNGxCCwWobMlgCIgrttN_YzMVRxb3x9wuu__A6RoX0h; _ga_KGRFF2R2C5=GS1.1.1693470960.1.0.1693470983.37.0.0; g_state={"i_p":1693478201328,"i_l":1}; _px2=eyJ1IjoiNmFhYWZjNTAtNDdkOS0xMWVlLTlkZTQtNDMzM2Y4NjVhZWI3IiwidiI6IjZhZThiNTk2LTQ3ZDktMTFlZS05YTA2LWRiOGYxYTRmNjExNyIsInQiOjE1Mjk5NzEyMDAwMDAsImgiOiI4MjAwZmEwNTE3ZmY1ZDVjNDQ3OWYyMjFmZWExMGJiZGZlNTYxODEyNjhiZDgwY2M5NjY2OTVmYjQ5OTg3ZWFjIn0=; _px=zD2Gc4xiJIy/QQoL+kq/44QRpkrrbrH3Pu/g2imsUP2Wg0PDr6Pd4zUfYuZ7whz8dRrY0WtEErkhLC0P7WlHEA==:1000:2eHYO4EEmYUpBqjtlI5GGXYvG+nQBVBFJviVG2PBQuq4uMTXMlHqE60qqFC1uMtF6iHAlEk7vIbPM35FK0MglPBWiZE93HQ1RWyF59NWWqOA9WJ+KRvZg/S+TOWNhIsR1Fq4v2aDmJaOef/Ws5/k8XVyumpXIbscCaaGDKnPvXG2eNiIIGMGchFCCYZf7FgJhTwwKWYXb1+/Wjsc53bX3KSgke27i9AxPHB+xzEZbZVdYhXr5wpIXr2NO2dBzz2K4VVckWdHJGshkiwUT9SSwg==',
    'if-none-match': 'W/"b6ce200a151eebaf051e26830d4eb2d5"',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
    handle_httpstatus_list = [403]
    concurrent_requests = 8
    counter = 0
    def start_requests(self):
        df = pd.read_excel("./seekingalpha_instructions.xlsx",sheet_name='URLs').fillna('N/A')
        for num in range(len(df)):
            row  = df.iloc[num]
            id = row['10k_url'].split('filing/')[-1].split('?')[0]
            ticker = row['ticker']
            if id != 'N/A':
                link = f'https://seekingalpha.com/api/v3/filings/{id}?include=ticker'
                yield scrapy.Request(link,callback = self.getPDF,headers=self.headers,meta={'ticker':ticker})
            

    def getPDF(self, response):
        meta =response.meta
        ticker = meta.get('ticker')

        jo = json.loads(response.body)
        
        data = jo['data']['attributes']['content']
        link = urljoin('https://seekingalpha.com',jo['data']['attributes']['pdf_path'])
        yield scrapy.Request(link,callback = self.parse,dont_filter=True,headers=self.headers,meta={'ticker':ticker,'data':data})


    def parse(self,response):
        meta =response.meta
        ticker = meta.get('ticker')   
        self.counter += 1
        if response.status != 200:
            with open(f"url.txt", 'a') as f:
                f.write(response.url)
            
        else:
            with open(f"./Downloads/{ticker}.pdf", 'wb') as f:
                f.write(response.body)
            
