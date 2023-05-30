import requests
from bs4 import BeautifulSoup


class WikiWorker():
    def __init__(self):
        self._url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    @staticmethod
    def _extract_company_symbols(page_htm):
        soup = BeautifulSoup(page_htm, 'lxml')
        table = soup.find(id='constituents')
        table_rows = table.find('tr')
        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            yield symbol


    def get_500_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Couldn't get entries")
            return []

        yield from _extract_company_symbols(response.text)