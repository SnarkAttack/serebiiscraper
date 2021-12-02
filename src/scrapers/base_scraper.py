import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

def convert_to_integer(val):

    if val == '--':
        return None
    else:
        return val

class BaseScraper(ABC):

    base_url = "https://www.serebii.net/"

    def __init__(self, gen_code, page_prefix):
        self._webpage_dir = f"{page_prefix}-{gen_code}/"

    def get_base_page_html(self):
        url = BaseScraper.base_url+self._webpage_dir
        r = requests.get(url)
        return r.text

    def get_page_html(self, page_name):
        full_url = BaseScraper.base_url+self._webpage_dir+page_name+'.shtml'
        r = requests.get(full_url)
        return r.text

    def _soupify_html(self, page_html):
        return BeautifulSoup(page_html, 'html.parser')

    @abstractmethod
    def scrape_data(self, page_html):
        pass

    def scrape_file_data(self, filepath):
        with open(filepath, 'r') as f:
            page_html = f.read()
        return self.scrape_data(page_html)

    @abstractmethod
    def scrape_all_data(self):
        pass
