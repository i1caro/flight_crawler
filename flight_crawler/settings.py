# Scrapy settings for flight_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'flight_crawler'

SPIDER_MODULES = ['flight_crawler.spiders']
NEWSPIDER_MODULE = 'flight_crawler.spiders'

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'flight_crawler_test'
