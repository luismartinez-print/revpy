import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from ..base import BaseOptimizer

class Emsr(BaseOptimizer):
    """
    Docstring for Emsr

    Heuristic for one or more fare optimization utilizing Littlewood's rule.
    It covers both EMSR-A (additive) and EMSR-B (Weighted Average of higher valued products)
    """

    def optimize(self, order_book, emsr_type = 'b'):
        
        prices = [fare for fare in order_book.fares.price]
        demand = [mean for mean in order_book.fares.mean]
        std = [std for std in order_book.fares.standard_deviation]

        ### main skeleton of the loop, first trial
        
        
        
        
        
        if emsr_type == 'a':
            pass #here insert the logic of EMSR