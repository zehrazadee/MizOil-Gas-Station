# import functions as fn

# fn.drawSquare()

#from functions import drawSquare, drawRectangle

# drawSquare()
# drawRectangle()

# from functions import createCar

from functions import *

gallery = createCarGallery()

car1 = createCar()
car2 = createCar()

addCarInGallery(gallery, car1)
addCarInGallery(gallery, car2)

printCarGallery(gallery)

removeCarFromGallery(gallery, car1)

printCarGallery(gallery)
