from .base import BaseObject

class Move(BaseObject):

    def __init__(self,
                 name,
                 type,
                 category,
                 pp,
                 base_power,
                 accuracy,
                 effect):
        self.name = name
        self.type = type
        self.category = category
        self.pp = pp
        self.base_power = base_power
        self.accuracy = accuracy
        self.effect = effect

