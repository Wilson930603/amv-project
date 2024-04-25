import scrapy
import json
from datetime import datetime
class Capterra_Spider(scrapy.Spider):
    name = "capterra"
    download_delay = 1.5
    base_url = "https://www.capterra.com/"
    api_url = "https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId={product_id}&from={offset}&size=25"
    product_url = "https://www.capterra.com/p/189398/QuickBooks-Online/reviews/"
    cookies = {
        '_pxhd': 'XXeml-l4em8Qn/nWVIGY5BCI5/IAL0RnmkzPHLB9tn-TQiEb8lysrbK6aQ4ahU140kUOIDAuIcLpk4Z0byOBhg==:a3zH1UFLXFFUIYRFzdksMOugPoxlhSMgswIgYaBREwJxOyeif1FXf6g9GsnImW8qN5Ato-qYEXoSryv3sBEwLIs6rU2yTJDe9JLvM/Yimb0=',
        '_pxvid': 'c759d328-2bc3-11ee-8eb2-5277e4eb55b8',
        'experimentSessionId': '0bbb26c1-e219-4160-b9f4-6613046659eb',
        '_gid': 'GA1.2.1582685885.1690383053',
        '_gcl_au': '1.1.101160339.1690383054',
        '_rdt_uuid': '1690383054885.fb01f15b-9910-4593-89f3-e42ef1173f88',
        'AMCV_04D07E1C5E4DDABB0A495ED1%40AdobeOrg': '-637568504%7CMCIDTS%7C19565%7CMCMID%7C61227119494459938270664742230499704681%7CMCAAMLH-1690987855%7C3%7CMCAAMB-1690987855%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1690390255s%7CNONE%7CvVersion%7C5.1.1',
        'seerid': '4ec55292-a4bb-4848-8401-a77c5798a221',
        'ELOQUA': 'GUID=73955716F2F147F686E68601C8D45669',
        'SignUpShowingProductToSaveExperiment': 'dbe52a30-2bc3-11ee-9e00-2f63a88762a7',
        'pxcts': '76a8a6d3-2c96-11ee-8dec-46544474454f',
        '_px3': '25994f7485eca5f7d2bbbeb3a67e8da93603477e1dd32738caafab9f1e8f314b:Am6flWF+U581LLXPUPn+1r7FZkF6BJ8XcoRgxpzcKG43+EFYz69fs44MIzfSS0Ka69GMK3i/qxFmUbUW9epU6w==:1000:fgCEGCMsVeqlOwBsVqM6zV0J0eJwvcHKRfpwiP6gOiEX3MhgaMoGSSWRhmCL1HSUeegBPfEJpo6ZdTKD7JgTn9IW8UdkFJw76QTgYWLqS55QB7nrHJWb0a3dBDdyfaeSFSuTcP6qAXLqck8/pgkkHhUVfwcd2OsVFdzRqfnMZO6BhasdAEB8VnYuAESXRaIjGqL3CqcHRuTDSq5ZYDfbpA==',
        '_pxde': '5fe56e1c4d60986dea2d0fd990612f3340d25069850a58d30ed9f4a6d293c91a:eyJ0aW1lc3RhbXAiOjE2OTA0NzM1MzQwNDYsImZfa2IiOjAsImlwY19pZCI6W119',
        'rt_var': 'prd',
        '_gat_UA-126190-1': '1',
        'device': 'Desktop',
        'country_code': 'PK',
        '_capterra2_session': 'dc3d0c8119385772fe94e46ef427e376',
        '_ga': 'GA1.2.1682997008.1690383053',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Jul+27+2023+20%3A59%3A03+GMT%2B0500+(Pakistan+Standard+Time)&version=202301.2.0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.capterra.com%2Fp%2F189398%2FQuickBooks-Online%2Freviews%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1',
        'seerses': 'e',
        'ln_or': 'eyIyNjk3MCI6ImQifQ%3D%3D',
        '_uetsid': 'd2b820302bc311ee8d52393341c15f03',
        '_uetvid': 'd2b83ec02bc311ee89bf5b4d39e299f4',
        '_gat': '1',
        'fs_lua': '1.1690473543908',
        'fs_uid': '#18VAT4#e5abc983-e6f9-49fd-ac3c-3e41583f4d13:34433cfd-d336-4b5e-a1cb-841469b9361f:1690473543908::1#/1721919054',
        '_ga_T9V61700R6': 'GS1.1.1690473542.5.0.1690473548.54.0.0',
        '_ga_M5DGBDHG2R': 'GS1.1.1690473542.3.1.1690473560.42.0.0',
    }

    headers = {
        'authority': 'www.capterra.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'cookie': '_pxhd=XXeml-l4em8Qn/nWVIGY5BCI5/IAL0RnmkzPHLB9tn-TQiEb8lysrbK6aQ4ahU140kUOIDAuIcLpk4Z0byOBhg==:a3zH1UFLXFFUIYRFzdksMOugPoxlhSMgswIgYaBREwJxOyeif1FXf6g9GsnImW8qN5Ato-qYEXoSryv3sBEwLIs6rU2yTJDe9JLvM/Yimb0=; _pxvid=c759d328-2bc3-11ee-8eb2-5277e4eb55b8; pxcts=c9311bba-2bc3-11ee-b505-647879735378; experimentSessionId=0bbb26c1-e219-4160-b9f4-6613046659eb; rt_var=prd; _gid=GA1.2.1582685885.1690383053; _gcl_au=1.1.101160339.1690383054; _ga=GA1.2.1682997008.1690383053; device=Desktop; country_code=PK; _capterra2_session=9e914ac83da73577453abffa3028688e; _rdt_uuid=1690383054885.fb01f15b-9910-4593-89f3-e42ef1173f88; ln_or=eyIyNjk3MCI6ImQifQ%3D%3D; AMCVS_04D07E1C5E4DDABB0A495ED1%40AdobeOrg=1; AMCV_04D07E1C5E4DDABB0A495ED1%40AdobeOrg=-637568504%7CMCIDTS%7C19565%7CMCMID%7C61227119494459938270664742230499704681%7CMCAAMLH-1690987855%7C3%7CMCAAMB-1690987855%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1690390255s%7CNONE%7CvVersion%7C5.1.1; seerid=4ec55292-a4bb-4848-8401-a77c5798a221; ELOQUA=GUID=73955716F2F147F686E68601C8D45669; SignUpShowingProductToSaveExperiment=dbe52a30-2bc3-11ee-9e00-2f63a88762a7; _gat_UA-126190-1=1; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jul+27+2023+07%3A24%3A32+GMT%2B0500+(Pakistan+Standard+Time)&version=202301.2.0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.capterra.com%2Fp%2F189398%2FQuickBooks-Online%2Freviews%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; seerses=e; _uetsid=d2b820302bc311ee8d52393341c15f03; _uetvid=d2b83ec02bc311ee89bf5b4d39e299f4; _gat=1; fs_lua=1.1690424673392; fs_uid=#18VAT4#e5abc983-e6f9-49fd-ac3c-3e41583f4d13:20e62c23-308b-4679-ada2-d28caa0326f4:1690422667889::2#/1721919054; _px3=aa40220a71199c69f4dc01a320470238f8bd6ca62c56da85ce7c747c2fc3a403:pn9de2daFpfRgC2wF1rCUWL5PGceUvhjsVbSdzAXQiiMHHmmRBcjMQSLOnri1sZKv3ix9uTSXsKRT73yMUa60g==:1000:FYNZHv4NGsTAEaG8Yb96X+RlDU+IzOMRAL8PbNf06EB2qKuRm1LfBr5BBJTZ8LcBcH7NpNUYQ25sSwYkba64fAsij9k/Tp6CXIeIFHqUFTGlCaXisSuBvQ1I1Fg0abxwedruHSVHc4Dc+3GrScNV6rSV/FNV6o5Kpmb6Xo8HlhOXetMbTd6zdKRsLeCU00OCNY92Opvh1hPpSoXvmj1fnQ==; _ga_T9V61700R6=GS1.1.1690424668.4.1.1690424695.33.0.0; _pxde=755f92dd92952f1ded63cb37846a18fb6828c01c00db0b37e282cd8692771ca9:eyJ0aW1lc3RhbXAiOjE2OTA0MjQ3MDE5ODIsImZfa2IiOjAsImlwY19pZCI6W119; _ga_M5DGBDHG2R=GS1.1.1690422663.2.1.1690424705.23.0.0',
        'referer': 'https://www.capterra.com/p/189398/QuickBooks-Online/reviews/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    def start_requests(self):
        product_id = self.product_url.split('/p/')[-1].split('/')[0]
        offset = 0
        url = self.api_url.format(product_id=product_id,offset=offset)
        yield scrapy.Request(
            url,
            callback=self.information,
            headers=self.headers,
            cookies=self.cookies,
            meta={"product_id":product_id,"offset":offset+25})
    

    def information(self,response):
        print(response.url)
        meta = response.meta

        product_id = meta.get('product_id')
        offset = meta.get('offset')


        data = json.loads(response.text)
        if len(data["hits"])>0:
            
            for review in data["hits"]:
                item = {}
                item["Name"] = review['reviewer'].get('fullName','NA')
                item["Job Title"] = review['reviewer'].get('jobTitle','NA')
                company = review['reviewer'].get('industry','')
                if company is None:
                    company = ''
                if review['reviewer'].get('companySize'):
                    company += ", "+review['reviewer'].get('companySize')
                item["Company"] = company
                item["Software Usage"] = review['reviewer'].get('timeUsedProduct','NA')
                item["Overall Rating"] = review.get('overallRating','NA')
                item["Ease of Use"] = review.get('easeOfUseRating','NA')
                item["Customer Service"] = review.get('customerSupportRating','NA')
                item["Features"] = review.get('functionalityRating','NA')
                item["Value for Money"] = review.get('valueForMoneyRating','NA')
                item["Likelihood to Recommend"] = review.get('recommendationRating','NA')
                item["Source"] = review.get('sourceSite','NA')
                date = review.get("writtenOn",'NA')
                if date !='NA':
                    date = datetime.strptime(date.split()[0].strip(),"%Y-%m-%d").strftime('%d/%m/%Y')
                item["Date"] = date
                item["Overall"] = review.get('generalComments','NA')
                item["Pro"] = review.get('prosText','NA')
                item["Cons"] = review.get('consText','NA')
                yield item

            url = self.api_url.format(product_id=product_id,offset=offset)
            yield scrapy.Request(
                url,
                callback=self.information,
                headers=self.headers,
                cookies=self.cookies,
                meta={"product_id":product_id,"offset":offset+25})