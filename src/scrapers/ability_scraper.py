from .base_scraper import BaseScraper, convert_to_integer
from src.objs.ability import Ability
from ..utilities import TYPES

class AbilityScraper(BaseScraper):
    """
    Scrapes each of the attackdex type pages to gather the most basic information about moves,
    which includes name, type, category, pp, base damage, accuracy, and effect
    """

    def __init__(self, gen_code):
        self._webpage_dir = f"abilitydex/"

    def scrape_data(self, page_html):

        page_soup = self._soupify_html(page_html)

        abilities = page_soup.find_all('option')

        # Make sure we filter out the default values for the dropdowns 
        return [Ability(ability.getText().replace(' ','').lower()) for ability in abilities if 'AbilityDex ' not in ability.getText()]

    def scrape_all_data(self):

        ability_base_html = self.get_base_page_html()
        return self.scrape_data(ability_base_html)