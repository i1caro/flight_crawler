#!/usr/bin/python
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from flight_crawler.spiders.skyscanner_spider import SkyScannerOriginDestinationSpider

import sys


def compact_date(date):
    day, month, year = date.split('-')
    return '%s%s%s' % (year[2:], month.zfill(2), day.zfill(2))


def run_spider(origin='', destination='', departure_date='', return_date=''):
    spider = SkyScannerOriginDestinationSpider(
            origin=origin,
            destination=destination,
            departure_date=compact_date(departure_date),
            return_date=compact_date(return_date),
        )
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python test_scraper.py fao lis 1-12-2013 12-12-2013'
    else:
        # Test usage
        run_spider(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    