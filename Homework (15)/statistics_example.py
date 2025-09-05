#Bu program statistics modulundan istifadə edir
#Ədədlər üzərində statistik hesablama aparır

import statistics

numbers = [2, 4, 4, 4, 6, 8, 10]

print("Orta:", statistics.mean(numbers))
print("Median:", statistics.median(numbers))
print("Moda:", statistics.mode(numbers))