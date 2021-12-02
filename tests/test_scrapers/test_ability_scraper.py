import os
from tests.test_utilities import TEST_DB
from src.scrapers import AbilityScraper

def test_ability_scraper():

    abs = AbilityScraper(gen_code=TEST_DB.gen_code)
    # Shortcut requests call and just load from file
    abilities = abs.scrape_file_data(os.path.join('tests', 'samples', 'example_basic_abilities.html'))
    assert len(abilities) == 264

def test_ability_db_saving():

    abs = AbilityScraper(gen_code=TEST_DB.gen_code)
    abilities = abs.scrape_file_data(os.path.join('tests', 'samples', 'example_basic_abilities.html'))

    ability_table = TEST_DB.get_or_create_ability_table()

    ability_table.insert_list_into_table(abilities)

    loaded_abilities = TEST_DB.load_abilities()

    assert len(abilities) == 264

    ability_names = [ability.name for ability in loaded_abilities]

    assert all([name in ability_names for name in ['honeygather', 'wimpout', 'mistysurge']])