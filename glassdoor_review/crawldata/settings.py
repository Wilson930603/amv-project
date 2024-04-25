# Tác giả: Trần Quang Tùng
# Email: tung@crawler.pro.vn - Phone/WhatsApp/Zalo: +84 931732381
# Website: tbco.com.vn

BOT_NAME = 'crawldata'

SPIDER_MODULES = ['crawldata.spiders']
NEWSPIDER_MODULE = 'crawldata.spiders'

#Glassdoor Account
GLASSDOOR_USER='info@crawler.pro.vn'
GLASSDOOR_PASSWORD='Abc123!@#'

URLLENGTH_LIMIT = 50000
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOW_ALL=True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 200
#CONCURRENT_REQUESTS_PER_DOMAIN = 999999
TELNETCONSOLE_ENABLED = False
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Alt-Used': 'www.glassdoor.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}
ITEM_PIPELINES = {'crawldata.pipelines.CrawldataPipeline': 300,}
#ROTATING_PROXY_LIST_PATH = '../proxy_250000.txt'
#ROTATING_PROXY_PAGE_RETRY_TIMES=100
#CONCURRENT_REQUESTS_PER_IP = 1
#DOWNLOADER_MIDDLEWARES = {
#    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#}