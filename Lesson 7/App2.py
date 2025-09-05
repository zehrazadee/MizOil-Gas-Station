#Task 1
size = 21

for row in range(size):
    for col in range(size):
        if (col ==0 or col == size-1 or row ==0 or row == size -1
            or col == size//4 and  row <= size//4
            or row == size//4 and col <= size//4
            or col == size*3//4 and row <= size//4
            or row == size//4 and col >= size*3//4
            or row == size*3//4 and col <= size//4   
            or col == size//4 and row >= size*3//4
            or row == size*3//4 and col >= size*3//4
            or col == size*3//4 and row >= size*3//4

            ):
            print("*", end="")
        else:
            print(end=" ")
    print()


#Task 2
size = 33

for row in range(size):
        for col in range(size):
            if (col ==0 or col == size-1 or row ==0 or row == size -1
                or col<=size/4 and  row<=size/4
                or col>=size*3/4-1 and row <= size/4
                or col<=size/4 and row>=size*3/4
                or col>=size*3/4-1 and row>=size*3/4

                ):
                print("*", end="")
            else:
                print(end=" ")
        print()



#Task 3 
size=21
for row in range(size//2):
     for col in range(size):
          if((col<row +1 or col>size-2-row)or col == size//2):
               print("*", end="")
          else:
               print(end=" ")
     print()
for row in range(size//2+1, size-1):
     for col in range(size):
          if((col>row  or col<size-row-1) or col == size//2):
               print("*", end="")
          else:
               print(end=" ")
     print()




#Task 4
size = 21  

for i in range(size // 2 + 1):
    for j in range(size):
        if j >= (size // 2 - i) and j <= (size // 2 + i):
            print("*", end="")
        else:
            print(" ", end="")
    print()


for i in range(size // 2 - 1, -1, -1):
    for j in range(size):
        if j >= (size // 2 - i) and j <= (size // 2 + i):
            print("*", end="")
        else:
            print(" ", end="")
    print()



#Task 5
size=21
for i in range(size):
    for j in range(size):
        if (j<size-i-1):
            print(end=" ")
        else:
            print("*", end=" ")
    print()



#Task 6
size=21
for i in range(size//2):
    for j in range(size):

        if (j==size//2-i-1 or (j==size//2+i-1)):
            print("*", end="")
        else:
            print(end=" ")
    print()
for i in range(size//2-1):
    for j in range(size):
         
         if(j==i+1 or j== size-i-4):
              print("*", end="")
         else:
              print(end=" ")
    print()


#Task 7
size = 15

for i in range(size):
    for j in range(size):
        if (
            i == 0 or i == size - 1   
            or j == 0 or j == size - 1  
            or i == j                  
            or j == size - i - 1       
        ):
            print("*", end="")
        else:
            print(" ", end="")
    print()
