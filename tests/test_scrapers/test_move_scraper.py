import os
from tests.test_utilities import TEST_DB
from src.scrapers.move_scraper import MoveScraper

def test_move_scraper():

    ms = MoveScraper(gen_code=TEST_DB.gen_code)

    # Shortcut requests call and just load from file
    moves = ms.scrape_file_data(os.path.join('tests', 'samples', 'example_basic_moves.html'))

    assert len(moves) == 33

def test_move_db_saving():

    ms = MoveScraper(gen_code=TEST_DB.gen_code)
    moves = ms.scrape_file_data(os.path.join('tests', 'samples', 'example_basic_moves.html'))

    TEST_DB.get_or_create_move_table().insert_list_into_table(moves)

    loaded_moves = TEST_DB.load_moves()

    assert len(moves) == 33

    move_names = [move.name for move in loaded_moves]

    assert all([name in move_names for name in ['silverwind', 'pollenpuff', 'attackorder']])