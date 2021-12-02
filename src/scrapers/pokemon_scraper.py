from bs4 import BeautifulSoup
from .base_scraper import BaseScraper, convert_to_integer
from ..objs import Pokemon
from ..utilities import DEFAULT_GEN, TYPES

class PokemonScraper(BaseScraper):

    def __init__(self, gen_code):
        super().__init__(gen_code, 'pokedex')

    def scrape_data(self, page_html):

        all_pokemon = []

        pokemon_soup = self._soupify_html(page_html)
        pokemon_table = pokemon_soup.find(class_='dextable')
        
        # Remove first tr as it is table header, and then grab every other tr
        # because each pokemon entry contains a second one for displaying the picture
        pokemon_rows = pokemon_table.findChildren('tr', recusrive=False)[2::2]

        for pokemon in pokemon_rows:

            # Set up defaults for values that may not exist for a given pokemon
            type2 = None
            ability2 = None
            hidden_ability = None

            pokemon_components = pokemon.find_all('td')
            num = int(pokemon_components[0].getText().strip()[1:])
            name = pokemon_components[3].getText().strip().lower()
            types = [a['href'].split('/')[-1][:-6] for a in pokemon_components[4].find_all('a')]
            type1 = types[0]
            if len(types) == 2:
                type2 = types[1]
            
            abilities = [a['href'].split('/')[-1][:-6] for a in pokemon_components[5].find_all('a')]

            ability1 = abilities[0]

            if len(abilities) > 1:
                hidden_ability = abilities[-1]
            if len(abilities) == 3:
                ability2 = abilities[1]


            hp = int(pokemon_components[6].getText().strip())
            att = int(pokemon_components[7].getText().strip())
            defn = int(pokemon_components[8].getText().strip())
            spa = int(pokemon_components[9].getText().strip())
            spd = int(pokemon_components[10].getText().strip())
            spe = int(pokemon_components[11].getText().strip())

            all_pokemon.append(Pokemon(name, num, type1, type2, ability1, ability2, hidden_ability, hp, att, defn, spa, spd, spe))

        return all_pokemon

    def scrape_all_data(self):

        moves = []

        for t in TYPES:
            page_html = self.get_page_html(t)
            moves += self.scrape_data(page_html)

        return moves

        

        