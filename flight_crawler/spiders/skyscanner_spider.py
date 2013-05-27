from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy import log
from flight_crawler.items import QuoteItem

import json
import re


header = {
    'Host': 'www.skyscanner.pt',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Language': 'en-GB,en;q=0.8,en-US;q=0.6,pt-PT;q=0.4,pt;q=0.2',
    }


def list_to_dict(key, value, data):
    response = dict([(item[key], item[value]) for item in data])
    return response


class SkyScannerOriginDestinationSpider(BaseSpider):
    name = 'skyscanner'
    allowed_domains = ['skyscanner.pt']
    start_urls = [
        "http://www.skyscanner.pt/"
    ]

    dataservices_url = 'http://www.skyscanner.pt/dataservices/routedate/v2.0/'
    flight_information_url = 'http://www.skyscanner.pt/voos'

    def build_search_url(self):
        result = self.flight_information_url

        try:
            result += '/'+self.origin
        except AttributeError:
            pass
        try:
            result += '/'+self.destination
        except AttributeError:
            pass
        try:
            result += '/'+self.compact_date(self.departure_date)
        except AttributeError:
            pass
        try:
            result += '/'+self.compact_date(self.return_date)
        except AttributeError:
            pass

        self.log('%s' % result, level=log.INFO)
        return result

    def parse(self, response):
        request = Request(url=self.build_search_url(),
                        callback=self.after_building_flight_url)
        return request

    def after_building_flight_url(self, response):

        key = self.find_session_key(response)
        if not key:
            self.log('No SessionKey found. At %s' % response.url, level=log.ERROR)
            return

        url = self.dataservices_url + key 
        self.log("Requesting url %s" % url, level=log.INFO)
        header['Referer'] = response.url
        request = Request(
                    url=url, 
                    headers=header, 
                    callback=self.get_flight_information)
        return request

    def find_session_key(self, response):
        site = HtmlXPathSelector(response)
        site_scripts = site.select('//script[@type="text/javascript"]/text()')

        for script in site_scripts.extract():
            found = re.search('"SessionKey":"([\w\d-]+)"', script)
            if found:
                return found.group(1)
        return None

    def get_flight_information(self, response):
        try:
            response_json = json.loads(response.body)
        except Exception, e:
            self.log("In flight information. %s" % e, level=log.ERROR)
            return
        
        quote_request = list_to_dict(
                key='Id', 
                value='AgentId', 
                data=response_json['QuoteRequests'])
        agents = list_to_dict(
                key='Id', 
                value='Name', 
                data=response_json['Agents'])

        items = list()
        for quote in response_json['Quotes']:
            agent_id = quote_request.get(quote['QuoteRequestId'], None)
            agent_name = agents.get(agent_id, None)
            price = quote['Price']

            item = QuoteItem()
            item['agent_name'] = agent_name
            item['price'] = price

            items.append(item)

        # Order by price
        result = items and sorted(items, key=lambda y: y['price'])
        # Order by agent
        result = result and sorted(result, key=lambda y: y['agent_name'])

        self.write_in_file(result) 
        return result

    def write_in_file(self, results):
        f = open('results.txt','w')
        for result in results:
            f.write(u'%s\n' % result)
        f.close()

