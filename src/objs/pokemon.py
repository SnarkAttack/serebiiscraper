from .base import BaseObject

class Pokemon(BaseObject):

    def __init__(self,
                 name,
                 number,
                 type1,
                 type2,
                 ability1,
                 ability2,
                 hidden_ability,
                 hp,
                 att,
                 defn,
                 spa,
                 spd,
                 spe):
        self.name = name
        self.number = number
        self.type1 = type1
        self.type2 = type2
        self.ability1 = ability1
        self.ability2 = ability2
        self.hidden_ability = hidden_ability
        self.hp = hp
        self.att = att
        self.defn = defn
        self.spa = spa
        self.spd = spd
        self.spe = spe

