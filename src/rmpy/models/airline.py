from .base import Resource
from dataclasses import dataclass, field
from typing import List
from operator import attrgetter
from itertools import permutations

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
    

### Network Logic

class HubNetwork:
    """
    Class that creates a hub and spoke network to run optimizations
    """

    def __init__(self, hub_code: str):
        self.hub_code = hub_code
        self.spokes = []
        self.legs = {}
        self.itineraries = []

    def add_spoke(self, city_code: str, capacity: int):
        """
        Docstring for add_spoke

        Adds an airport or city spoke and automatically creates the two legs necessary
        1. Inbound
        2. Outbound
        
        """
        self.spokes.append(city_code)
        leg_in = Leg(origin = city_code, destination=self.hub_code, capacity=capacity)
        self.legs[f"{city_code} - {self.hub_code}"] = leg_in

        leg_out = Leg(origin=self.hub_code, destination=city_code, capacity=capacity)
        self.legs[f"{self.hub_code} - {city_code}"] = leg_out

        def generate_fares(): 
            pass #comeback to this one
    
