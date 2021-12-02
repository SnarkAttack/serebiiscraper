from .base_scraper import BaseScraper, convert_to_integer
from src.objs.move import Move
from ..utilities import TYPES

class MoveScraper(BaseScraper):
    """
    Scrapes each of the attackdex type pages to gather the most basic information about moves,
    which includes name, type, category, pp, base damage, accuracy, and effect
    """

    def __init__(self, gen_code):
        super().__init__(gen_code, 'attackdex')

    def scrape_data(self, page_html):

        moves = []

        move_soup = self._soupify_html(page_html)
        move_table = move_soup.find(class_='dextable')
        # Remove first tr as it is table header
        move_rows = move_table.find_all('tr')[1:]

        for move in move_rows:
            move_components = move.find_all('td')

            name = move_components[0].find('a').getText().replace(' ', '').lower()
            type = move_components[1].find('img')['src'].split('/')[-1][:-4]
            category = move_components[2].find('img')['src'].split('/')[-1][:-4]
            pp = convert_to_integer(move_components[3].getText().strip())
            base_power = convert_to_integer(move_components[4].getText().strip())
            accuracy = convert_to_integer(move_components[5].getText().strip())
            effect = move_components[6].getText().strip()

            moves.append(Move(name, type, category, pp, base_power, accuracy, effect))

        return moves

    def scrape_all_data(self):

        moves = []

        for t in TYPES:
            page_html = self.get_page_html(t)
            moves += self.scrape_data(page_html)

        return moves