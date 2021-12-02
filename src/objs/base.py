from abc import ABC, abstractmethod

class BaseObject(ABC):

    def __init__(self, table_name):
        
        self.table_name = table_name