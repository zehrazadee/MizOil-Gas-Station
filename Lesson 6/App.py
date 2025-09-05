# for i in range (size):
#     for j in range (i+1):
#         print("*", end = " ")
#     print()

# size = 15
# for i in range (size):
#     for j in range (size):
#         if i ==0 or i == size - 1 or j == 0 or j == size -1:
#             print("*", end = " ")
#     else:
#         print()


# for row in range(1,6):
#     for col in range(1,6):
#         print(row, end =" ")
#     print()




#Task 2
for i in range(1, 6): 
        for j in range(5):  
            print(i, end=" ") 
        print()
#Task 3
for i in range(5):  
    for j in range(1, 6): 
            print(j, end=" ") 
    print() 

#Task 4
for i in range(5, 0, -1):  
        for j in range(5): 
            print(i, end=" ") 
        print()

#Task 5
for i in range (5): 
    for j in range (5, 0, -1):
         print(j, end=" ")
    print()

#Task 6
num = 1
for i in range (5):
     for j in range(5):
        if num< 10:
            print(num, end =" ")
        else:
            print(num, end =" ")
        num +=1
     print()

#Task 7
num = 1
for i in range (5):
     for j in range(5):
        if num < 10:
            print(num, end =" ")
        else:
            print(num, end=" ")
        num +=2
     print()

#Task 8
num = 2
for i in range (5):
     for j in range(5):
        if num < 10:
            print(num, end =" ")
        else:
            print(num, end=" ")
        num +=2
     print()

#Task 9
num = 1
for i in range (1, 6):
     for j in range(1, 6):
        cavab =  i*j
        if cavab< 10:
            print(cavab, end=" ")
        elif cavab< 100:
            print(cavab, end=" ")
        else:
            print(cavab, end=" ")
     print()

#Task 10
num_row = 5
num_col = 6 

for i in range(1, num_row + 1): 
    for j in range(1, num_col + 1): 
        if j == 1:
            print(1, end=" ") 
        elif j == 2:
            print(i, end=" ") 
        elif j == 3:
            print(2, end=" ") 
        elif j == 4:
            print(i, end=" ") 
        elif j == 5:
            print(3, end=" ") 
        elif j == 6:
            print(i, end=" ") 
    print() 

#Task 11
for i in range(1, 6):
    for j in range(1, 7):
        if j == 1 or j == 3 or j == 5:
            print(i, end=" ")
        elif j == 2:
            print(1, end=" ")
        elif j == 4:
            print(2, end=" ")
        elif j == 6:
            print(3, end=" ")
    print()


#Lesson 
