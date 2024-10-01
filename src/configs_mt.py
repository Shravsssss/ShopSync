"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

# package imports
from datetime import datetime
import requests
from ebaysdk.finding import Connection
from threading import Thread
import html
import json


# configs
WALMART = {
    'site': 'walmart',
    'url': 'https://www.walmart.com/search?q=',
    'item_component': 'div',
    'item_indicator': {
        'data-item-id': True
    },
    'title_indicator': 'span.lh-title',
    'price_indicator': ['span.f6.f5-l', 'span.f2'],
    'link_indicator': 'a'
}

AMAZON = {
    'site': 'amazon',
    'url': 'https://www.amazon.com/s?k=',
    'item_component': 'div',
    'item_indicator': {
        'data-component-type': 's-search-result'
    },
    'title_indicator': 'h2 a span',
    'price_indicator': 'span.a-price span',
    'link_indicator': 'h2 a.a-link-normal'
}

COSTCO = {
    'site': 'costco',
    'url': 'https://www.costco.com/CatalogSearch?dept=All&keyword=',
    'item_component': 'div',
    'item_indicator': {
        'class': 'product-tile-set'
    },
    'title_indicator': 'span a',
    'price_indicator': 'div.price',
    'link_indicator': 'span.description a',
}

BESTBUY = {
    'site': 'bestbuy',
    'url': 'https://www.bestbuy.com/site/searchpage.jsp?st=',
    'item_component': 'div',
    'item_indicator': {
        'class': 'embedded-sku'
    },
    'title_indicator': 'h4.sku-title a',
    'price_indicator': 'div.priceView-customer-price span',
    'link_indicator': 'a.image-link',
}


# individual scrapers
class scrape_target(Thread):
    def __init__(self, query):
        self.result = []
        self.query = query
        super(scrape_target,self).__init__()

    def run(self):
        """Scrape Target's api for data

        Parameters
        ----------
        query: str
            Item to look for in the api

        Returns
        ----------
        items: list
            List of items from the dict
        """

        # api_url = 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1'

        # page = '/s/' + self.query
        # params = {
        #     'key': '5938CFDFD3FB4A7DB7C060583C86663C',
        #     'channel': 'WEB',
        #     'count': '24',
        #     'default_purchasability_filter': 'false',
        #     'include_sponsored': 'true',
        #     'keyword': self.query,
        #     'offset': '0',
        #     'page': page,
        #     'platform': 'desktop',
        #     'pricing_store_id': '3991',
        #     'useragent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        #     'visitor_id': 'AAA',
        # }

        # data = requests.get(api_url, params=params).json()
        # items = []
        # if 'search' in data['data']:
        #     for p in data['data']['search']['products']:
        #         item = {
        #             'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        #             'title': html.unescape(p['item']['product_description']['title']),
        #             'price': '$' + str(p['price']['current_retail']),
        #             'website': 'target',
        #             #'link': shorten_url(p['item']['enrichment']['buy_url'])
        #             'link': p['item']['enrichment']['buy_url']
        #         }
        #         items.append(item)

        #     self.result = items
        # set up the request parameters
        params = {
            'api_key': '5938CFDFD3FB4A7DB7C060583C86663C',
            'search_term': 'Iphone',
            'type': 'search',
            'sort_by': 'best_match'
            }

        # make the http GET request to RedCircle API
        api_result = requests.get('https://api.redcircleapi.com/request', params).json()
        items = []
        # print("Requests Remaining on this account: " + api_result['request_info']['credits_remaining'])
        # print(api_result)
        if (api_result['request_info']['success']):
            for product in api_result['search_results']:
                try:
                    item = {
                        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        'title': product['product']['title'],
                        'price': product['offers']['primary']['symbol'] + str(product['offers']['primary']['price']),
                        'website': 'target',
                        'link': product['product']['link']
                    }
                except:
                    continue
                items.append(item)
            # print(items)
        self.result = items


class scrape_ebay(Thread):
    def __init__(self, query):
        self.result = {}
        self.query = query
        super(scrape_ebay,self).__init__()

    def run(self):
        """Scrape Target's api for data

        Parameters
        ----------
        query: str
            Item to look for in the api

        Returns
        ----------
        items: list
            List of items from the dict
        """

        EBAY_APP = 'BradleyE-slash-PRD-2ddd2999f-2ae39cfa'

        try:
            api = Connection(appid=EBAY_APP, config_file=None, siteid='EBAY-US')
            response = api.execute('findItemsByKeywords', {'keywords': self.query})
        except ConnectionError as e:
            print(e)
            self.result = []

        data = response.dict()

        items = []
        for p in data['searchResult']['item']:
            item = {
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'title': html.unescape(p['title']),
                'price': '$' + p['sellingStatus']['currentPrice']['value'],
                'website': 'ebay',
                #'link': shorten_url(p['viewItemURL'])
                'link': p['viewItemURL']
            }
            items.append(item)

        self.result = items


CONFIGS = [WALMART, AMAZON, COSTCO, BESTBUY]
