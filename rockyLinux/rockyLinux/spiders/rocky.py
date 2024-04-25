import scrapy
from scrapy.http import Request
from ..items import *



class rocky(scrapy.Spider):
    name = "rocky"
    # handle_httpstatus_list = [200, 400, 302, 503]

    allowed_domains = []
    download_delay = 0.5
    ptag = "&page=1"
    start_url = [
        "https://forums.rockylinux.org/directory_items.json?order=likes_received{ptag}&period=all"
    ]
    second = "https://forums.rockylinux.org/u/{username}/summary.json"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36 Edg/102.0.100.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/604.1 Edg/102.0.100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19042",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.9.1) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15",
    ]
    base_url = ""
    # LOG_STDOUT = True
    # LOG_FILE = './datafolder/log.txt'
    # ['DateExtractRun'] = strftime("%d/%m/%Y", gmtime())
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    # headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'}
    # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    # cookies = {'FlexoCMS.Currency':'USD','FlexoCMS.CurrentCountry':'US'}
    # <---START URL---->
    def __init__(self):
        super(rocky, self).__init__()

    def start_requests(self):
        yield Request(
            self.start_url[0].format(ptag=""),
            callback=self.main_page,
            headers=self.headers,
        )

    def main_page(self, response):
        meta = response.meta
        totalpages = 81
        currentpage = meta.get("currentpage", 1)
        if currentpage <= totalpages:
            nextPage = self.start_url[0].format(ptag=f"&page={currentpage}")
            currentpage += 1
            yield Request(
                nextPage,
                callback=self.main_page,
                headers=self.headers,
                meta={"currentpage": currentpage},
            )
        body = response.json()
        users = body.get("directory_items")
        for user in users:
            received = user.get("likes_received")
            username = user.get("user").get("username")
            role = user.get("user").get("title")
            name = user.get('user').get('name')
            secondRequest = self.second.format(username=username)
            items = RockylinuxItem()
            items["URL"] = secondRequest.replace(".json", "")
            items["Username"] = username
            items["LikesReceived"] = received
            items['Role'] = role
            items['Name'] = name
            yield Request(
                f"https://forums.rockylinux.org/u/{username}/card.json",
                callback=self.information,
                headers=self.headers,
                meta={"items": items},
            )
            # input(f'User = {username} -- {received} -- \n\n{secondRequest}')

    def information(self, response):
        items = response.meta.get("items")
        body = response.json()
        try:
            badge = body.get("user").get("created_at").split("T")[0]
        except:
            badge = None
        # try:
        #     badge = body.get('user_summary').get('badges')[3].get('granted_at').split('T')[0]
        # except:
        # badge = body.get('user_summary').get('badges')[0].get('granted_at').split('T')[0]

        items["Joined"] = badge
        yield items
