import os
import sqlite3
from abc import ABC, abstractmethod
from functools import wraps

from .utilities import TYPES, MOVE_CATEGORIES, DEFAULT_GEN
from .objs import Ability, Move, Pokemon
from .scrapers import MoveScraper, AbilityScraper, PokemonScraper

class Table(ABC):

    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.fields = []

    def _get_field_names(self):
        return [f[0] for f in self.fields]

    def _create_table_schema_no_id(self):
        return [f"{f[0]} {f[1]}" for f in self.fields]

    def _create_table_schema_id(self):
        return ['id integer PRIMARY KEY AUTOINCREMENT'] + self._create_table_schema_no_id()

    def access_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            result = func(self, cursor, *args, **kwargs)
            conn.commit()
            conn.close()
            return result
        return wrapper

    @access_db
    def table_exists(self, cursor):
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?; ''', (self.table_name,))
        return cursor.fetchone()[0] == 1

    @access_db
    def create_table(self, cursor):
        table_schema = ', '.join(self.create_table_schema())
        print(f"Creating table {self.table_name}")
        cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {self.table_name}({table_schema});
            '''
        )

    @abstractmethod
    def populate_table(self, gen_code):
        pass

    @access_db
    def insert_into_table(self, cursor, obj):
        values = self.obj_to_values(obj)
        value_bindings = ','.join(['?'] * len(values))
        # rstrip in case a non-field value (like unique constraints including multiple rows)
        # is part of field_names
        field_names = ','.join(self._get_field_names()).rstrip(',')
        cursor.execute(
            f'''
            INSERT OR IGNORE INTO {self.table_name}({field_names}) VALUES({value_bindings});
            ''', values)

    @access_db
    def get_table_row_count(self, cursor):
        cursor.execute(
            f'''
            SELECT COUNT(*) from {self.table_name}
            '''
        )

    @access_db
    def load_from_table(self, cursor, **kwargs):
        # If a single element is passed in as a string for fields, make fields a list of length one
        if len(kwargs) == 0:
            cursor.execute(
                f'''
                SELECT * FROM {self.table_name};
                '''
            )
        objs = [self.__class__.obj_class(*data[1:]) for data in cursor.fetchall()]
        return objs


    @abstractmethod
    def obj_to_values(self, obj):
        pass

    @abstractmethod
    def create_table_schema(self):
        pass

    def insert_list_into_table(self, obj_list):
        for obj in obj_list:
            self.insert_into_table(obj)

class MoveTable(Table):

    obj_class = Move
    
    def __init__(self, db_path):
        super().__init__(db_path, 'moves')

        self.fields = [
            ('name', 'text NOT NULL'),
            ('type', 'text NOT NULL'),
            ('category', 'text NOT NULL'),
            ('pp', 'integer NOT NULL'),
            ('base_power', 'integer'),
            ('accuracy', 'integer'),
            ('effect', 'text'),
            ('', 'UNIQUE(name, category)')
        ]

        self.create_table()

    def create_table_schema(self):
        return super()._create_table_schema_id()

    def obj_to_values(self, move):
        return [
            move.name,
            move.type,
            move.category,
            move.pp,
            move.base_power,
            move.accuracy,
            move.effect
        ]
    
    def populate_table(self, gen_code):
        ms = MoveScraper(gen_code)
        moves = ms.scrape_all_data()
        self.insert_list_into_table(moves)

class AbilityTable(Table):

    obj_class = Ability

    def __init__(self, db_path):
        super().__init__(db_path, 'abilities')
        
        self.fields = [
            ('name', 'text NOT NULL UNIQUE'),
        ]

        self.create_table()

    
    def create_table_schema(self):
        return super()._create_table_schema_id()

    def obj_to_values(self, ability):
        return [
            ability.name,
        ]

    def populate_table(self, gen_code):
        abs = AbilityScraper(gen_code)
        abilities = abs.scrape_all_data()
        self.insert_list_into_table(abilities)

class PokemonTable(Table):

    obj_class = Pokemon
    
    def __init__(self, db_path):
        super().__init__(db_path, 'pokemon')

        self.fields = [
            ('name', 'text NOT NULL'),
            ('number', 'integer NOT NULL'),
            ('type1', 'text NOT NULL'),
            ('type2', 'text'),
            ('ability1', 'text NOT NULL'),
            ('ability2', 'text'),
            ('hidden_ability', 'text'),
            ('hp', 'integer NOT NULL'),
            ('att', 'integer NOT NULL'),
            ('def', 'integer NOT NULL'),
            ('spa', 'integer NOT NULL'),
            ('spd', 'integer NOT NULL'),
            ('spe', 'integer NOT NULL'),
            ('', 'UNIQUE(name, type1, type2)')
        ]

        self.create_table()

    def create_table_schema(self):
        return super()._create_table_schema_id()

    def obj_to_values(self, pokemon):
        return [
            pokemon.name,
            pokemon.number,
            pokemon.type1,
            pokemon.type2,
            pokemon.ability1,
            pokemon.ability2,
            pokemon.hidden_ability,
            pokemon.hp,
            pokemon.att,
            pokemon.defn,
            pokemon.spa,
            pokemon.spd,
            pokemon.spe,
        ]
    
    def populate_table(self, gen_code):
        ps = PokemonScraper(gen_code)
        pokemon = ps.scrape_all_data()
        self.insert_list_into_table(pokemon)


class SerebiiDatabase(object):

    def __init__(self, gen_code=DEFAULT_GEN, db_prefix='serebii'):
        self.gen_code = gen_code
        self.db_prefix = db_prefix

        self.db_path = os.path.join('databases', f"{self.db_prefix}_{self.gen_code}.db")

        self.tables = {}

    def _get_move_table(self):
        return self.tables['moves']

    def _create_move_table(self):
        self.tables['moves'] = MoveTable(self.db_path)
        return self.tables['moves']

    def get_or_create_move_table(self):
        try:
            return self._get_move_table()
        except KeyError as e:
            return self._create_move_table()

    def _get_ability_table(self):
        return self.tables['abilities']

    def _create_ability_table(self):
        self.tables['abilities'] = AbilityTable(self.db_path)
        return self.tables['abilities']

    def get_or_create_ability_table(self):
        try:
            return self._get_ability_table()
        except KeyError as e:
            return self._create_ability_table()

    def _get_pokemon_table(self):
        return self.tables['pokemon']

    def _create_pokemon_table(self):
        self.tables['pokemon'] = PokemonTable(self.db_path)
        return self.tables['pokemon']

    def get_or_create_pokemon_table(self):
        try:
            return self._get_pokemon_table()
        except KeyError as e:
            return self._create_pokemon_table()

    def populate_moves(self, gen_code=DEFAULT_GEN):
        move_table = self.get_or_create_move_table()
        move_table.populate_table(gen_code)

    def populate_abilities(self, gen_code=DEFAULT_GEN):
        ability_table = self.get_or_create_ability_table()
        ability_table.populate_table(gen_code)

    def populate_pokemon(self, gen_code):
        pokemon_table = self.get_or_create_pokemon_table()
        pokemon_table.populate_table(gen_code)

    def load_moves(self, **kwargs):
        return self._get_move_table().load_from_table(**kwargs)

    def load_abilities(self, **kwargs):
        return self._get_ability_table().load_from_table(**kwargs)

    def load_pokemon(self, **kwargs):
        return self._get_pokemon_table().load_from_table(**kwargs)
