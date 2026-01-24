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
@dataclass
class Itinerary:
    """
    Docstring for Itinerary
    Commercial object that the customer buys, for example the flight ticket
    """
    name: str
    price: float
    legs: List[Leg]
    mean = float 
    std: float 

class AirlineNetwork:
    """
    Docstring for AirlineNetwork
    Create itineraries into Virtual Fareclasses
    """
    def __init__(self, legs: List[Leg], itineraries: List[Itinerary]):
        self.legs = legs
        self.itineraries = itineraries
    
    def map_demand(self):
        pass #here it will be the logic for Virtual Nesting




class HubNetwork(AirlineNetwork):
    """
    Class that creates a hub and spoke networks
    This makes the AirlineNetwork more easy to map that to go one by one
    """

    def __init__(self, hub_code: str):
        self.hub_code = hub_code
        self.spokes = []
        self._leg_map = {}
        self._generated_itineraries = []
        super().__init__(legs = [], itineraries=[])

    def add_spoke(self, city_code: str, capacity: int):
        """
        Docstring for add_spoke

        Adds an airport or city spoke and automatically creates the two legs necessary
        1. Inbound
        2. Outbound
        
        """
        self.spokes.append(city_code)

        leg_in = Leg(origin = city_code, destination=self.hub_code, capacity=capacity)
        self._leg_map[f"{city_code} - {self.hub_code}"] = leg_in
        self.legs.append(leg_in)

        leg_out = Leg(origin=self.hub_code, destination=city_code, capacity=capacity)
        self._leg_map[f"{self.hub_code} - {city_code}"] = leg_out
        self.legs.append(leg_out)

        def generate_fares(self, base_demand: float): #tie this to forecast
            self.itineraries = []

            for leg in self.legs:
                itin = Itinerary(
                    name = f'Local_{leg.name}',
                    price = 100,
                    mean = base_demand,
                    std = base_demand * 0.2
                )
                self.itineraries.append(itin)

            for origin, dest in permutations(self.spokes, 2):
                leg_1 = self._leg_map[f"{origin} - {self.hub}"]
                leg_2 = self._leg_map[f"{self.hub} - {dest}"]

                #create a connecting itin
                conn_itin = Itinerary(
                    name=f"Conn_{origin}-{dest}",
                    price = 250, #place holder
                    legs = [leg_1, leg_2],
                    mean = base_demand * 0.5, #place holder until I know what to do with it
                    std = base_demand * 0.1
                )
    
