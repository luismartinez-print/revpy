from rmpy.models import Book, FareClass
from rmpy.optimizers.single_resource.emsr import Emsr

# Testing the classes

#Some setup before
book = Book(capacity=100)
fares = [
    FareClass("Basic",    price=100,  mean=60, standard_devation=15),  # Index 0
    FareClass("Standard", price=200,  mean=40, standard_devation=10),  # Index 1
    FareClass("Flex",     price=500,  mean=25, standard_devation=8),   # Index 2
    FareClass("Business", price=1000, mean=10, standard_devation=4)    # Index 3
]
for fare in fares:
    book.add_fareclass(fare)

opt = Emsr()

result = opt.optimize(book, emsr_type= 'a')

print(result)
