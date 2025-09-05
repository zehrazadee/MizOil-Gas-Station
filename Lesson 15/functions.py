# def drawSquare():
#     for i in range(10):
#         for j in range(10):
#             print("*", end = "")
#         print()

# def drawRectangle():
#     for i in range(10):
#         for j in range(15):
#             print("*", end = "")
#         print()

def createCar():
    brand = input("Enter new car brand: ")
    model = input("Enter car model :")
    year = int(input("Enter car year: "))
    color = input("Enter car color: ")

    newCar = [brand, model, year, color]
    return newCar

def updateCar(car):
    print("Məlumatı dəyişmək istəməsən, Enter - a bas.")
    brand = input(f"brand ({car[0]}): ") or car[0]
    model = input(f"model ({car[1]}): ") or car[1]

    year_in = input(f"year ({car[2]}): ").strip()
    if year_in:
        while not year_in.isdigit():
            year_in = input("Ədəd daxil edin: ").strip()
        year = int(year_in)
    else:
         year = car[2]
    color = input(f"color ({car[3]}): ") or car[3]

    car[0] = brand
    car[1] = model
    car[2] = year
    car[3] = color
    return car

def addCarInGallery(gallery, car):
    gallery[1].append(car)
    print(f"{car[0]} {car[1]} qalereyaya əlavə olundu.")

def updateGallery(gallery):
    print(f"Qalereyanın indiki adı: {gallery[0]}")
    new_name = input("Yeni ad daxil et (boş buraxsan ad eyni qalacaq): ")
    if new_name:
        gallery[0] = new_name
        print("Qalereyanın adı dəyişdirildi. ")
    else:
        print("Qalereyanın adı dəyişilməz qaldı. ")

def removeCarFromGallery(gallery, car):
    if car in gallery[1]:
        gallery[1].remove(car)
        print(f"{car[0]} {car[1]} qalereyadan silindi.")
        return True
    else:
        print("Bu maşın qalereyada yoxdur.")
        return False
    

def createCarGallery():
        name = input("Enter New Gallery Name:")

        newGallery = [name, []]
        return newGallery

def printCar(car):
    print(f"{car[0]} {car[1]} ({car[2]}), Color: {car[3]}")

def printCarGallery(gallery):
    print(f"Gallery Name: {gallery[0]}")
    print("Cars in gallery:")

    if len(gallery[1]) == 0:
        print("  Qalereyada maşın yoxdur.")
    else:
        index = 1
        for car in gallery[1]:
            print(f"{index}. ", end="")
            printCar(car)
            index += 1
