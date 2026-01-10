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
class Book:
    """Represents the total inventory and list of fares""" #make this a property or airline in the future
    capacity: int
    fares: List[FareClass] = field(default_factory = list)

    def add_fareclass(self, fareclass: FareClass):
        """Adds Class and keeps the list sorted desc"""
        self.fares.append(fareclass)
        # Here I will sort them since, it makes the math easier
        self.fares.sort(key = attrgetter('price'), reverse = True)

        def get_total_demand(self):
            return sum(fare.mean for fare in self.fares)