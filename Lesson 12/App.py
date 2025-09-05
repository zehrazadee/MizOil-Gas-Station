# #Homework
# #Task 1
# def kub(n):
#     return n**3
# print(kub(5))

# #Task 2
# def bigNumber(x,y):
#     if x > y:
#         return x
#     return y
# print(bigNumber(25,14))

# #Task 3
# def musbetdir(n):
#     return n>0
# print(musbetdir(5))
# print(musbetdir(-3))

# #Task 4
# def toplama (a, b):
#     return a+b
# def cixma (a, b):
#     return a-b
# def vurma (a, b):
#     return a*b
# def bolme (a, b):
#     if b!= 0:
#         return a/b
#     else:
#         return "Sıfıra bölmək olmaz!"
# def calculator(sechim, a, b):
#     if sechim == "toplama":
#         return toplama (a, b)
#     elif sechim ==  "cixma":
#         return cixma (a, b)
#     elif sechim == "vurma":
#         return vurma (a, b)
#     elif sechim == "bolme":
#         return bolme (a, b)
#     else:
#         return "Yanlış seçim etmisiniz!"
# print(calculator("toplama", 6, 4))
# print(calculator("cixma", 3, 5))
# print(calculator("vurma", 4, 5))
# print(calculator("bolme", 35, 7))

# #Task 5
# def square (t):
#     for i in range (t):
#         print("* " * t)
# square (6)

# #Task 6 
# def sadeeded (n):
#     if n<2:
#         return False
#     for i in range (2, n):
#         if n % i == 0:
#             return False
#     return True
# print(sadeeded(7))
# print(sadeeded(12))

# #Task 7 
# def factorial(n):
#     result = 1
#     for i in range (1, n + 1):
#         result = result * i
#     return result
# print(factorial(5))

# #Task 8 
# def quvvet_hesabla (esaseded, quvvet):
#     netice = 1
#     for i in range (quvvet):
#         netice = netice * esaseded
#     return netice
# print(quvvet_hesabla(2, 3))

# #or (another way)

# def quvvet_hesabla (esaseded, quvvet):
#     return esaseded ** quvvet
# print(quvvet_hesabla(3, 2))

# #Task 9
# def topla_araliq(a, b):
#     cem = 0
#     for i in range(a, b + 1):
#         cem = cem + i
#     return cem
# print(topla_araliq(2, 15))

# #Task 10
# def en_boyuk(liste):
#     max_eded = liste[0]
#     for eded in liste:
#         if eded > max_eded:
#             max_eded = eded
#     return max_eded
# print(en_boyuk([2, 5, 8, 19, 106]))



#Lesson 13

#Task 1
# import random

# def fillList(my_list, size, minvalue, maxvalue):
#     for _ in range(size):
#         my_list.append(random.randint(minvalue, maxvalue))

# count = 0
# for num in my_list:
#     # Şərti yoxlayırıq: 3-ə bölünsün VƏ 5-ə bölünməsin
#     if num % 3 == 0 and num % 5 != 0:
#         count += 1

# print(f"3-ə bölünüb, 5-ə bölünməyən ədədlərin sayı: {count}")

# my_list = []
# fillList(my_list, 10, 1, 100)
# print(f"Yaradılan list: {my_list}")

# #Task 1
# import random
# def fillList(list, size, min, max):
#     for i in range(size):
#         num = random.randint(min, max)
#         list.append(num)

# def printList(list):
#     for i in list:
#         print(f"{i}, " ,end= " ")
# def task1(list):
#     for i in list:
#         if i%3 == 0 and i%5!=0:
#             count +=1
#     return count
# myList1 = []
# fillList(myList1, 10, 1, 100)
# printList(myList1)
# print(task1(myList1))









#Homework
#Task 1
A = [1, 2, 3, 4, 5]
B = [5, 10, 15, 20, 25]
C = []
for i in range(5):
    C.append(A[i])
    C.append(B[i])
print(C)

#Task 2
A = [-4, -2, 1, 0, -3, 2, -1, 3, 4]
B = []
for x in A:
    if x<0:
        B.append(x)
for x in A:
    if x == 0:
        B.append(x)
for x in A:
    if x>0:
        B.append(x)
print(B)

#Task 3
import random
A = [random.randint(0, 100) for _ in range(5)]
print("Əvvəlcə:", A)
for i in range(len(A)):
    min_index = i
    for j in range(i+1, len(A)):
        if A[j]< A[min_index]:
            min_index = j
    A [i], A [min_index] = A[min_index], A[i]
print("Sonra:", A)

#Task 4 
M = [1, 2, 3, 4, 5, 7, 8, 9]
N = [2, 7, 12, 14, 5, 9]
C = []
for x in M:
    if x in N and x not in C:
        C.append(x)
print(C)

#Task 5 
M = [1, 3, 5, 7, 9, 11, 13, 15]
N = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
C = []
for x in M:
    if x not in N and x not in C:
        C.append(x)
print(C)