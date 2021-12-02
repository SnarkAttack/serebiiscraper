import os
from src.scrapers.pokemon_scraper import PokemonScraper
from tests.test_utilities import TEST_DB

def test_pokemon_scraper():

    ps = PokemonScraper(gen_code=TEST_DB.gen_code)

    pokemon = ps.scrape_file_data(os.path.join('tests', 'samples', 'example_basic_pokemon.html'))

    # This is 85, not 82, because the type pages have duplicated entries for gigantamax pokemon,
    # and we don't attempt to solve this until saving into the database
    assert len(pokemon) == 85

def test_pokemon_db_saving():

    ps = PokemonScraper(gen_code=TEST_DB.gen_code)
    pokemon = ps.scrape_file_data(os.path.join('tests', 'samples', 'example_basic_pokemon.html'))

    pokemon_table = TEST_DB.get_or_create_pokemon_table()

    pokemon_table.insert_list_into_table(pokemon)

    loaded_pokemon = TEST_DB.load_pokemon()

    assert len(loaded_pokemon) == 82

    pokemon_names = [pokemon.name for pokemon in loaded_pokemon]

    assert all([name in pokemon_names for name in ['frosmoth', 'wimpod', 'butterfree']])