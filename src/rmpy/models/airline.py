from .base import Resource
from dataclasses import dataclass, field
from typing import List
from operator import attrgetter

@dataclass
class FareClass:
    """Represent a single fare class and its demand distribution"""
    name: str
    price: float
    mean: float
    standard_devation: float

@dataclass
class Leg(Resource):
    """
    Docstring for Leg:
    Implementation of a flight leg with a predifined origination and destination
    """

    def __init__(self, origin:str, destination:str, capacity:int):
        super().__init__(capacity)

        self.origin = origin
        self.destination = destination
        
        self._fares: List[FareClass] = []

    def add_fareclass(self, product):
        self._fares.append(product)
        self._fares.sort(key = attrgetter('price'), reverse = True)

    @property
    def fares(self) -> List[FareClass]:
        return self._fares
    
    def get_total_demand(self) -> float:
        return sum(fare.mean for fare in self._fares)
    
    @property
    def name(self) -> str:
        return f'{self.origin} - {self.destination}'