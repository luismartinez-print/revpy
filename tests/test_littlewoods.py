from rmpy.models.airline import Leg, FareClass
from rmpy.optimizers.single_resource.littlewood import Littlewoods

# Testing the classes

#Some setup before
book = Leg(origin='New York', destination='Los Angeles', capacity= 100)

book.add_fareclass(FareClass("Business", 1000, 20, 5))
book.add_fareclass(FareClass("Economy", 400, 50, 15))

opt = Littlewoods()

results = opt.optimize(book, show_inventory= True, show_statistics = True)
