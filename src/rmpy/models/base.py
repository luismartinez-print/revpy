from abc import ABC, abstractmethod
from typing import List

class Resource(ABC):
    """
    Docstring for Resource

    Abstract base class for any type of inventory base resource
    Airline leg, hotel room, train ride etc
    """

    def __init__(self, capacity :int):
        self.capacity = capacity

    @abstractmethod
    def add_fareclass(self, product):
        """
        Docstring for add_product
        must implement in either way a add product method 
        """
        pass

    @abstractmethod
    def fares(self) -> List:
        "Must return the list of sorted fares for that exact resource"
        pass

    @abstractmethod
    def get_total_demand(self) -> float:
        "Must return the total demand" #change this so that we can have a forecasting module later
        pass           