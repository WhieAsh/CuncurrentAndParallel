import _random
import time
import random
import threading
import time

import requests
from bs4 import BeautifulSoup
from lxml import html


class YahooFinanceScheduler(threading.Thread):
    def __init__(self, input_queue):
        super(YahooFinanceScheduler, self).__init__()
        self._input_queue = input_queue

        self.start()

    def run(self) -> None:

        while True:
            symbol = self._input_queue.get()
            if symbol=='DONE':
                break
            yahoo_pinance_worker = YahooFinanceWorker(symbol)
            price = yahoo_pinance_worker.get_yahoo_price()
            print(f'{symbol}  = {price}')
            time.sleep(random.random())


class YahooFinanceWorker():
    def __init__(self, symbol, **keyargs):
        self._base_url = 'https://finance.yahoo.com/quote/'
        self._symbol = symbol
        self._url = f'{self._base_url}{self._symbol}'


    def get_yahoo_price(self):

        response = requests.get(self._url)
        #response = requests.get('https://finance.yahoo.com/quote/EVGO')
        #print('status_code = ', response.status_code)
        page_content = html.fromstring(response.text)

        #price = page_content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')
        #price = float(page_content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text)
        price = round(100*random.random(), 2)
        return price