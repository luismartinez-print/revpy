from abc import ABC, abstractmethod

#This is to create a template that all my optimization methods use
class BaseOptimizer(ABC):
    @abstractmethod
    def optimize(self, order_book): #if I keep going as Book objcets
        pass
    # This is just to create a simple same method for all optimizations