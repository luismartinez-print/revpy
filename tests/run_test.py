import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))


from rmpy.models import Book, FareClass
from rmpy.optimizers.single_resource.littlewood import Littlewoods

# Testing the classes

#Some setup before
book = Book(capacity=100)
book.add_fareclass(FareClass("Business", 1000, 20, 5))
book.add_fareclass(FareClass("Economy", 400, 50, 15))

opt = Littlewoods()

results = opt.optimize(book, show_inventory= True, show_statistics = True)