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

        :returns a dictionary with protection values and booking limits for each fare
        """
        result_dict = {}
        capacity = book.capacity

        if emsr_type == 'a':
            fares = sorted(book.fares, key = attrgetter("price"), reverse = False)
            

            for i in range(len(fares)):
                low_fare = fares[i]
                protection_agg = 0
                protection_booking = []

                for j in range(i + 1, len(fares)):
                    
                    higher_fare = fares[j]

                    protection_level = norm.ppf(1 - (low_fare.price / higher_fare.price), loc = higher_fare.mean, 
                                                scale = higher_fare.standard_devation) #f*ck this typo, gotta change it
                    
                    protection_level = round(protection_level)
                    
                    protection_agg += protection_level
                
                booking_limit = book.capacity - protection_agg
                protection_booking.append(protection_agg)
                protection_booking.append(booking_limit)
                result_dict[low_fare.name] = protection_booking


        elif emsr_type == 'b':
            fares = book.fares
            result_dict[fares[0].name] = [0, capacity]
            sum_mean = fares[0].mean
            sum_variance = fares[0].standard_devation ** 2

            # weighted price of higher priced products
            weighted_revenue = fares[0].price * fares[0].mean

            for i in range(1, len(fares)):
                protection_booking = []
                current_fare = fares[i]
                avg_price = weighted_revenue / sum_mean

                sum_std = np.sqrt(sum_variance)

                protection_level = norm.ppf( 1 - (current_fare.price / avg_price), loc = sum_mean, scale = sum_std) # joined for simplicity
                protection_level = round(protection_level)
                booking_limit = book.capacity - protection_level

                protection_booking.append(protection_level)
                protection_booking.append(booking_limit)
                result_dict[current_fare.name] = protection_booking


                sum_mean += current_fare.mean
                sum_variance += current_fare.standard_devation ** 2
                weighted_revenue += current_fare.price * current_fare.mean

        if show_inventory == True:
            self._show_inventory(result_dict, capacity)
        return result_dict
    

    def _show_inventory(self, booking_limits, capacity):
        """
        Docstring for _show_inventory
        Inside function to manage to show the inventory with booking limits and protection values
        :param self: OOP
        """
        #create figure and axis
        fig, ax = plt.subplots(figsize = (10, 5), layout = 'constrained')

        names = list(booking_limits.keys())
        position = range(len(names))

        for i, (fare, values) in enumerate(booking_limits.items()):
            protection = values[0]
            bl = values[1]

            ax.barh(
                i,
                bl,
                color = '#008020',
                alpha = 0.8,
                height=0.6,
                label = 'Available to sell' if i == 0 else ''
            )
            ax.barh(
                i,
                protection,
                left = bl,
                alpha = 0.4,
                hatch = '///',
                height= 0.6,
                label = 'Protected for Higher Classes' if i == 0 else ''
            )

            if bl > 5:
                ax.text(bl /2, i, f"{bl}",
                        va = 'center', ha = 'center', color = 'white', fontweight = 'bold')
            if protection > 5:
                ax.text(bl + (protection /2), i, f"Protected: {protection}",
                        va = 'center', ha = 'center', color = 'black', fontweight = 'bold')
                

        ax.set_yticks(position)
        ax.set_yticklabels(names)
        ax.set_xlabel("Seats")
        ax.set_title(f"Inventory Controls (Total Capacity: {capacity})")
        

        ax.axvline(capacity, color="black", linestyle="--", linewidth=1, alpha=0.5)
        ax.text(capacity, -0.5, "Capacity", ha="center", fontsize=8)

        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
        
        plt.show()
