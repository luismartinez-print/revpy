import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from ..base import BaseOptimizer


class Littlewoods(BaseOptimizer):
    """
    Littlewood's Rule optimization that utilizes the protection value for the highest fare, utilizing the
    formula Fl >= Fh * Pr[Xh >= Y]. We accept discounted fare if it is greater than or equal to the expected
    value of the demand for higher fare. The probability is that the demand for the higher fare is greater than
    or qual to the current protection value.
    
    """
    def optimize(self, book, show_inventory = False, show_statistics = False):
        """
        Calculates protection value for Higher fare
        
        :param book: object of class book
            :param fares: takes two fares into account and the mean and std demand of the higher fare
        : param show_inventory: user decides if they want to view the inventory graphically or not
        """
        if len(book.fares) < 2:
            raise ValueError("Littlewood's Rule Needs 2 fares")

        fare_1 = book.fares[0]
        fare_2 = book.fares[1]
        print(fare_1)

        ph = fare_1.price
        pl = fare_2.price
        

        capacity = book.capacity #the inventory per day

        critical_ratio = pl / ph

        protection_level = norm.ppf(1 - critical_ratio,
                                    loc = fare_1.mean,
                                    scale = fare_1.standard_devation)
        
        protection_level = round(protection_level)
        booking_limit = capacity - protection_level

        if show_inventory == True:
            self._show_inventory(capacity, protection_level, fare_1.name, fare_2.name)
        if show_statistics == True:
            self._show_statistics(protection_level, fare_1.mean, fare_1.standard_devation, critical_ratio)

        print(f"The optimal protection value for {fare_1.name} is {protection_level}",
                     f"The booking limit for {fare_2.name} is {booking_limit}", sep='\n')
        return protection_level
    
    def _show_inventory(self, capacity, protection_level, high_name, low_name):
        """
        Docstring for _show_invetory
        plots a nested inventory for a lower and higher fare
        
        :param capacity: Daily constrained capacity
        :param protection_level: Protection value for higher rate
        """

        available = capacity - protection_level

        fig, ax = plt.subplots(figsize = (10, 4))
        #bars
        ax.barh(0, protection_level, color = "#008020", label = f"Protected for {high_name}", edgecolor = "white") #I like this green :)
        ax.barh(0, available,left=protection_level, color = "#0A7FC7", label = f"Available for both {high_name} and {low_name}",
                edgecolor = "white") #check how to change the names
        #texts
        ax.text(protection_level / 2, 0, f'Protected: {protection_level}',
                va = 'center', ha = 'center', color = 'white', fontweight = 'bold')
        ax.text(protection_level + (available / 2), 0, f'Available for {low_name} {available}',
                va = 'center', ha = 'center', color = 'white', fontweight = 'bold')
        # Do some styling
        ax.set_yticks([]) # no y axis
        ax.set_xlim(0, capacity)
        ax.set_xlabel("Inventory Units") #think about hotel or airline later
        ax.set_title("Inventory Protection with Littlewood's Rule")
        ax.legend(loc = "upper center", bbox_to_anchor = (0.5, -0.5), ncol = 2)

        plt.tight_layout()
        plt.show()

    
    def _show_statistics(self, protection_value, mean, standard_deviation, critical_ratio):
        """
        Docstring for _show_statistics
        
        :param protection_level: Protection level for higher fare
        :param mean: mean demand of higher fare
        :param standard_deviation: standard deviation of higher fare

        returns cdf and pdf with critical ration painted
        """
        fig, axs = plt.subplots(ncols= 2, figsize = (8, 8), layout = 'constrained')

        #get the x-axis
        x = np.linspace(mean - (3 * standard_deviation), mean + (3 * standard_deviation), mean)
        #get the y axis together
        y_pdf = norm.pdf(x, loc = mean, scale = standard_deviation)
        y_cdf = norm.cdf(x, loc = mean, scale = standard_deviation)

        axs[0].plot(x, y_pdf)
        axs[0].set_title("Density function of demnand")
        axs[0].fill_between(x, y_pdf,
                            where = (x >= protection_value),
                            color = "red",#change the colors later
                            alpha = 0.3,
                            label = f'Critical Ratio {critical_ratio:.2f}')

        axs[1].plot(x, y_cdf)
        axs[1].set_title("Cummulative Density Function")
        axs[1].axhline(y = critical_ratio, color = 'red', linestyle = "--", label = "Critical Ratio")# add more legens and context
        plt.show()
        
        #### add text to the shading and to the lines, also refine the demand and intuiton

        