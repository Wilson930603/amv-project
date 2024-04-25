import scrapy,json,csv,os, requests, urllib, shutil,ast
from scrapy import Selector
class CrawlerSpider(scrapy.Spider):
    name = 'vuori'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Reviews-Origin': 'REVIEWS.io Widget',
        'Origin': 'https://vuoriclothing.com',
        'Connection': 'keep-alive',
        'Referer': 'https://vuoriclothing.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'type': 'product_review',
        'store': 'vuori-clothing',
        'sort': 'date_desc',
        'page': '1',
        'per_page': '8',
        'sku': 'VW323BLKXXS;VW323BLKXSM;VW323BLKSML;VW323BLKMED;VW323BLKLRG;VW323BLKXLG;VW323BLKXXL;39630921924711;22964239794234;22964239827002;22964239859770;22964239892538;22964239925306;39630922809447',
        'lang': 'en',
        'enable_syndication': 'true',
        'enable_avatars': 'true',
        'include_subrating_breakdown': '1',
    }
    def start_requests(self):
        skulst=['VW323BLKXXS;VW323BLKXSM;VW323BLKSML;VW323BLKMED;VW323BLKLRG;VW323BLKXLG;VW323BLKXXL;39630921924711;22964239794234;22964239827002;22964239859770;22964239892538;22964239925306;39630922809447','VW303HLKXXS;VW303HLKXSM;VW303HLKSML;VW303HLKMED;VW303HLKLRG;VW303HLKXLG;VW303HLKXXL;40095636717671;40095636750439;40095636783207;40095636815975;40095636848743;40095636881511;40095636914279','VW3000BCMXXS;VW3000BCMXSM;VW3000BCMSML;VW3000BCMMED;VW3000BCMLRG;VW3000BCMXLG;VW3000BCMXXL;39614338072679;39614338105447;39614338138215;39614338170983;39614338203751;39614338236519;39614338269287','V8003WHEONS;39806055481447','VW158WGPXXS;VW158WGPXSM;VW158WGPSML;VW158WGPMED;VW158WGPLRG;VW158WGPXLG;VW158WGPXXL;40095621906535;40095621939303;40095621972071;40095622004839;40095622037607;40095622070375;40095622103143','VS001WHT007;VS001WHT009;VS001WHT010;VS001WHT011;VS001WHT012;VS001WHT013;VS001WHT014;VS001WHT015;VS001WHT016;VS001WHT017;VS001WHT018;VS001WHT019;VS001WHT020;VS001WHT021;VS001WHT022;VS001WHT023;VS001WHT025;40075961172071;40075961204839;40075961237607;40075961270375;40075961303143;40075961335911;40075961368679;40075961401447;40075961434215;40075961499751;40075961565287;40075961630823;40075961696359;40075961761895;40075961794663;40075961860199;40075961925735','VW108HINXXS;VW108HINXSM;VW108HINSML;VW108HINMED;VW108HINLRG;VW108HINXLG;VW108HINXXL;39631253373031;23449276776506;23449276809274;23449276842042;23449276874810;23449276907578;39631253766247','VW1005HBKXXS;VW1005HBKXSM;VW1005HBKSML;VW1005HBKMED;VW1005HBKLRG;VW1005HBKXLG;VW1005HBKXXL;39399222935655;39399222870119;39399222804583;39399222771815;39399222739047;39399222837351;39399222902887']
        with open('vuorif.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Stars', 'Description', 'Date', 'Helpful'])
        for sku in skulst:
            self.params['sku']=sku
            url="https://api.reviews.io/timeline/data"
            yield scrapy.FormRequest(url,callback=self.get_reviews, method='GET', headers=self.headers,formdata = self.params,meta={'sku':sku},dont_filter=True)
    def get_reviews(self,response):
        Data=json.loads(response.text)
        for item in Data['timeline']:
            Name=item['_source']['author']
            Stars=item['_source']['rating']
            Desc=item['_source']['comments']
            if item['_source']['helpful'] is None:
               Helpful=0
            else:
               Helpful=item['_source']['helpful']
            Date=item['_source']['date_updated'].split(' ')[0]
            with open('vuorif.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([Name,Stars,Desc,Date,Helpful])
        if len(Data['timeline']) >= 8:
            page = self.params['page']
            N_page = str(int(page)+1)
            self.params['page'] = N_page
            self.params['sku']=response.meta['sku']
            url=response.url
            yield scrapy.FormRequest(url,callback=self.get_reviews, method='GET', headers=self.headers,formdata = self.params,meta={'sku':response.meta['sku']},dont_filter=True)