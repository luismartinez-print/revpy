import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from ..base import BaseOptimizer
from operator import attrgetter

class Emsr(BaseOptimizer):
    """
    Docstring for Emsr

    Heuristic for one or more fare optimization utilizing Littlewood's rule.
    It covers both EMSR-A (additive) and EMSR-B (Weighted Average of higher valued products)
    """

    def optimize(self, book, emsr_type = 'b', show_inventory = False, show_statistics= False):
        """
        Docstring for optimize
        
        :param self: Description
        :param book: Book where the fares are being stored
        :param emsr_type: If you want the emsr to be form weighted average or aggregated protection values
        :param show_inventory: Default false. Shows the inventory breakdown.
        :show_statistics: Default fase. Shows the statistics and probability breakdown

        :returns two dictionarie sone with the protection values and the other with booking limits
        """
        protection_levels = {} #here we will store the protection values
        booking_limits = {} #here the booking limits
        if emsr_type == 'a':
            fares = sorted(book.fares, key = attrgetter("price"), reverse = False)
            

            for i in range(len(fares)):
                low_fare = fares[i]

                protection_agg = 0

                protection_levels[f'Protection for > {low_fare.name}'] = protection_agg
                booking_limits[low_fare.name] = book.capacity - protection_agg

                for j in range(i + 1, len(fares)):
                    
                    higher_fare = fares[j]

                    protection_level = norm.ppf(1 - (low_fare.price / higher_fare.price), loc = higher_fare.mean, 
                                                scale = higher_fare.standard_devation) #f*ck this typo, gotta change it
                    
                    protection_level = round(protection_level)
                    
                    protection_agg += protection_level

        fares = book.fares
        sum_mean = fares[0].mean
        sum_variance = fares[0].standard_devation ** 2

        # weighted price of higher priced products
        weighted_revenue = fares[0].price * fares[0].mean

        for i in range(1, len(fares)):
            current_fare = fares[i]
            avg_price = weighted_revenue / sum_mean

            sum_std = np.sqrt(sum_variance)

            protection_level = norm.ppf( 1 - (current_fare.price / avg_price), loc = sum_mean, scale = sum_std) # joined for simplicity
            protection_level = round(protection_level)

            protection_levels[f'Protection againts > {current_fare.name}'] = protection_level
            booking_limits[current_fare.name] = book.capacity - protection_level

            sum_mean += current_fare.mean
            sum_variance += current_fare.standard_devation ** 2
            weighted_revenue += current_fare.price * current_fare.mean


        return protection_levels, booking_limits
    

    def _show_inventory(self):
        """
        Docstring for _show_inventory
        Inside function to manage to show the inventory with booking limits and protection values
        :param self: Description
        """

