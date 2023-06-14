import threading

import requests
from bs4 import BeautifulSoup


class WikiWorkerScheduler(threading.Thread):

    def __init__(self, out_queues, inout_value, **kwargs):

        self._out_queues = out_queues
        self._url = inout_value
        super(WikiWorkerScheduler, self).__init__(**kwargs)

        self.start()

    def run(self) -> None:
        wiki_worker = WikiWorker(self._url)

        sybol_count = 0
        for symbol in wiki_worker.get_500_companies():
            for out_queue in self._out_queues:
                out_queue.put(symbol)

            sybol_count += 1
            if sybol_count > 100:
                break

class WikiWorker():
    def __init__(self, url):
        self._url = url

    @staticmethod
    def _extract_company_symbols(page_htm):
        soup = BeautifulSoup(page_htm, 'lxml')
        table = soup.find(id='constituents')
        table_rows = table.find_all('tr')
        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            yield symbol


    def get_500_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Couldn't get entries")
            return []

        yield from self._extract_company_symbols(response.text)