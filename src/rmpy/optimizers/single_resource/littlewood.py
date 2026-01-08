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

        ph = book.fares[0]
        pl = book.fares[1]

        capacity = book.capacity #the inventory per day

        critical_ratio = pl / ph

        protection_level = norm.ppf(1 - critical_ratio,
                                    loc = ph.mean,
                                    scale = ph.standard_deviation)
        result = f"The optimal protection value for {ph.name} is {protection_level}"

        return result
    
    def _show_invetory(self, capacity, protection_level):
        """
        Docstring for _show_invetory
        plots a nested inventory for a lower and higher fare
        
        :param capacity: Daily constrained capacity
        :param protection_level: Protection value for higher rate
        """

        available = capacity - protection_level

        fig, ax = plt.subplot(figsize = (10, 2))
        #bars
        ax.barh(0, protection_level, color = "#008020", label = "Protected for Ph") #I like this green :)
        ax.barh(0, available, color = "#0A7FC7", label = "Available for both Ph and Pl") #check how to change the names
        #texts
        ax.text(protection_level / 2, 0, f'Protected: {protection_level}',
                va = 'center', ha = 'center', color = 'white', fontweight = 'bold')
        ax.text(protection_level + (available / 2), 0, f'Available for Pl {available}',
                va = 'center', ha = 'center', color = 'white', fontweight = 'bold')
        # Do some styling
        ax.set_yticks([]) # no y axis
        ax.set_xlim(0, capacity)
        ax.set_xlabel("Inventory Units") #think about hotel or airline later
        ax.set_title("Inventory Protection with Littlewood's Rule")
        ax.legend(loc = "upper center", bbox_to_anchor = (0.5, -0.5), ncol = 2)

        plt.tight_layout()
        plt.show()

    
    def _show_statistics(self, protection_level, mean, standard_deviation):
        """
        Docstring for _show_statistics
        
        :param protection_level: Protection level for higher fare
        :param mean: mean demand of higher fare
        :param standard_deviation: standard deviation of higher fare

        returns cdf and pdf with critical ration painted
        """
        fig, axs = plt.subplots(ncols= 2, figsize = (7, 7), layout = 'constrained')

        #get the x-axis
        x = np.linspace(mean - (3 * standard_deviation), mean + (3 * standard_deviation), mean)
        #get the y axis together
        y_pdf = norm.pdf(x, loc = mean, scale = standard_deviation)
        y_cdf = norm.cdf(x, loc = mean, scale = standard_deviation)

        axs[0].plot(x, y_pdf)
        axs[0].set_title("Density function of demnand")

        axs[1] = plt.plot(x, y_cdf)
        axs[1] = plt.set_title("Cummulative Density Function")
        
        

        