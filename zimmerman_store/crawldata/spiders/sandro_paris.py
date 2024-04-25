import scrapy,json


class SandroParisSpider(scrapy.Spider):
    name = "sandro-paris"
    #allowed_domains = ["sandro-paris.com"]
    headers = {"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)"}
    cookies = {'sid:BiS4rgHJLV_GKgEszb12vF_DBECBKQcXHYw','dwanonymous_89769ebaac72b2eaaf64270f595dcd31:abdLzEQavUwCpHsbMZXG5vRbRE','__cq_dnt:1','dw_dnt:1','showGeolocationPopin:true','dwsid:4Z-SEVTVDt5nTF-epvRcoLh4Lv_UNSSWvOpj_wHa_JbaO-Y43LxrOaG1XL0qkI9f4omC0Pt3gFT66jhK3E0Mcw==; mt.v:2.1456189792.1681203854852','_gcl_au:1.1.1650999368.1681203856','sandronewsletterpopin:true','RES_TRACKINGID:751143088313282','ResonanceSegment:1','RES_SESSIONID:964581545823351','_ga_EYPVY28JC1:GS1.1.1681203855.1.1.1681205139.60.0.0','_ga:GA1.1.870845197.1681203856','m_ses:20230411160416','m_cnt:1','_gid:GA1.2.96510252.1681203857','_tt_enable_cookie:1','_ttp:st504PA4HnExGfbVvbYzO6SO1bE'}
    start_urls = ["https://us.sandro-paris.com/on/demandware.store/Sites-Sandro-US-Site/en_US/Stores-GetStores?adlgid=1"]

    def parse(self, response):
        Data=json.loads(response.text)
        for row in Data:
            Item = {}
            Item['Country'] = row['properties']['country']
            Item['Title'] = row['properties']['title']
            Item['Address'] = row['properties']['address']
            yield(Item)
        pass
