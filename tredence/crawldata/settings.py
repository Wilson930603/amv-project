# Scrapy settings for crawldata project
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawldata'

SPIDER_MODULES = ['crawldata.spiders']
NEWSPIDER_MODULE = 'crawldata.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawldata (+http://www.yourdomain.com)'

#Crawlera: pip install scrapy-crawlera
#CRAWLERA_ENABLED = True
#CRAWLERA_APIKEY = '75aadc426ded420c833bfe1476386cd6'
#AUTOTHROTTLE_ENABLED = False
#CRAWLERA_PRESERVE_DELAY=5

#Luminati: pip install scrapyx-luminati
#LUMINATI_ENABLED = True
#LUMINATI_URL = '127.0.0.1:24000'
#RANDOM_UA_PER_PROXY = True
#RANDOM_UA_SAME_OS_FAMILY =True

# pip install scrapy-rotating-proxies
ROTATING_PROXY_LIST_PATH = '../proxy_10000.txt'
#import requests,re
#response=requests.get("http://ddxnms.com/vnexpress_net.txt")
#ROTATING_PROXY_LIST=re.split('\r\n|\n',response.text)
#print(ROTATING_PROXY_LIST)
ROTATING_PROXY_PAGE_RETRY_TIMES=100

#SPLASH_URL = 'http://ddxnms.com:8050'
#DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
#HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
#SPLASH_COOKIES_DEBUG = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'getdata (+http://www.yourdomain.com)'

URLLENGTH_LIMIT = 50000

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOW_ALL=True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'content-type': 'text/plain',
    'Connection': 'keep-alive',
    'TE': 'trailers',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawldata.middlewares.CrawldataSpiderMiddleware': 543,
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html

#pip install scrapy_user_agents
RANDOM_UA_PER_PROXY=True
FAKEUSERAGENT_FALLBACK='Mozilla'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#    'crawldata.middlewares.CrawldataDownloaderMiddleware': 543,
#    'scrapy_splash.SplashCookiesMiddleware': 723,
#    'scrapy_splash.SplashMiddleware': 725,
#    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
#    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
#    'scrapy_crawlera.CrawleraMiddleware': 610,
#    'scrapyx_luminati.LumninatiProxyMiddleware': 610,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawldata.pipelines.CrawldataPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#LOG_ENABLED = True
#LOG_LEVEL='ERROR'
#LOG_FORMAT = '%(levelname)s: %(message)s'
