# -*- coding: utf-8 -*-

# Scrapy settings for getdata project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'getdata'

SPIDER_MODULES = ['getdata.spiders']
NEWSPIDER_MODULE = 'getdata.spiders'

#LUMINATI_ENABLED = True
#LUMINATI_URL = '127.0.0.1:24000'
#RANDOM_UA_PER_PROXY = True
#RANDOM_UA_SAME_OS_FAMILY =True

#ROTATING_PROXY_LIST_PATH = '../proxy_list.txt'
#ROTATING_PROXY_PAGE_RETRY_TIMES=50

#Crawlera
#CRAWLERA_ENABLED = True
#CRAWLERA_APIKEY = '93e57d75cebc4e5f840680e667ffef55'
#AUTOTHROTTLE_ENABLED = False
#CRAWLERA_PRESERVE_DELAY=5

#SPLASH_URL = 'http://localhost:8050'
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
CONCURRENT_REQUESTS = 3
RETRY_TIMES=5
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 500
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'getdata.middlewares.GetdataSpiderMiddleware': 543,
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'getdata.middlewares.GetdataDownloaderMiddleware': 543,
    #'scrapy_splash.SplashCookiesMiddleware': 723,
    #'scrapy_splash.SplashMiddleware': 725,
    #'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
#    'scrapy_crawlera.CrawleraMiddleware': 610
#    'scrapyx_luminati.LumninatiProxyMiddleware': 610,
#    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'getdata.pipelines.GetdataPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
