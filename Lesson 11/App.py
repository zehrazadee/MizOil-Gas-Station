#Homework
# "Samsung S5, Samsung S6, Samsung S7, Samsung S8" elementlerne sahib bir list yaradin.
phones = ["Samsung S5", "Samsung S6", "Samsung S7", "Samsung S8"]
# Listin nece elementi var ?
print(len(phones))
# Listenin ilk ve son elementi nedir ?
print(phones[0])
print(phones[-1])
# "Samsung S5" elementini "Samsung S9" ile deyishin.
phones[phones.index("Samsung S5")] = "Samsung S9"
print(phones)
# "Samsung S6" listin bir elementidir ?
print("Samsung S6" in phones)
# Listin ilk 2 elementini alın. (slice)
print(phones[:2])
# Listin son 2 elementinin yerine "Samsung S9" ve "Samsung S10" deyerleri ile evez edin.
phones[-2:] = ["Samsung S9", "Samsung S10"]
print(phones)
# Listin üzerine "IPhone X" ve "IPhone XR" deyerlerini elave edin.
phones.append("Iphone X")
phones.append("Iphone XR")
print(phones)
# Listin son elementini silin.
phones.pop()
print(phones)
# Listin elementlerni tersden yazdırın.
print(phones[::-1])

