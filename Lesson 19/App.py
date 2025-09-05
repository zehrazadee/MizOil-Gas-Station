#Searching and sorting algorithms - today's lesson
#2 dene sort algoritmi arasdirib kodu ve izahi ile yazmaq --- Homework
# bubblesortlist = [3, 5, 2, 6, 8, 4, 1, 9, 7]
# for i in range(len(bubblesortlist)):
#     isSwapped = False
#     for j in range(0, len(bubblesortlist)-i-1):
#         if bubblesortlist[j] > bubblesortlist[j+1]:
#             temp = bubblesortlist[j]
#             bubblesortlist[j] = bubblesortlist[j+1]
#             bubblesortlist[j+1] = temp
#             isSwapped = True
#     if not isSwapped:
#         break
# print("Bubble Sort Nəticəsi:", bubblesortlist)
# bubblesortlist = [3, 5, 2, 6, 8, 4, 1, 9, 7]


# selectionsortlist = [3, 5, 2, 6, 8, 4, 1, 9, 7]
# for i in range(len(selectionsortlist)):
#     minIndex = i
#     for j in range(i+1, len(selectionsortlist)):
#         if selectionsortlist[j] < selectionsortlist[minIndex]:
#             minIndex = j
#     selectionsortlist[i], selectionsortlist[minIndex] = selectionsortlist[minIndex], selectionsortlist [i]
# print("Selection Sort Nəticəsi:", selectionsortlist)


# insertionsortlist = [3, 5, 2, 6, 8, 4, 1, 9, 7]
# for i in range(1, len(insertionsortlist)):
#     key = insertionsortlist[i]
#     j = i-1
#     while j>= 0 and key < insertionsortlist[j]:
#         insertionsortlist[j+1] = insertionsortlist[j]
#         j -= 1
#     insertionsortlist[j+1] = key
# print("Insertion Sort Nəticəsi:", insertionsortlist)



#Homework


#Merge Sort:

#Siyahını ortadan iki hissəyə bölür.
#Hər hissəni ayrıca sıralayır.
#Sonda ikisini birləşdirərək düz siyahı alır.
def merge_sort(ededler):
    if len(ededler) > 1:
        mid = len(ededler) // 2
        left = ededler[:mid]
        right = ededler[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                ededler[k] = left[i]
                i += 1
            else:
                ededler[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            ededler[k] = left[i]
            i += 1
            k +=1
        while j < len(right):
            j += 1
            k += 1
    return ededler
print(merge_sort([38, 27, 43, 3, 9, 82, 10]))


#Heap Sort:

#Əvvəlcə siyahını Max-Heap-a çeviririk → ən böyük element siyahının əvvəlində olur.
#Ən böyüyü götürüb sona qoyuruq.
#Qalan hissəni yenidən heap-ləyirik.
#Bu prosesi bütün elementlər üçün təkrarlayırıq.
def heapify(siyahi, n, i):
    largest = i    #kök (root)
    left = 2 * i + 1
    right = 2 * i +2
    if left < n and siyahi[left] > siyahi[largest]:
        largest = left
    if right < n and siyahi[right] > siyahi[largest]:
        largest = right
    if largest != i:
        siyahi[i], siyahi[largest] = siyahi[largest], siyahi[i]
        heapify(siyahi, n, largest)
def heap_sort(siyahi):
    n = len(siyahi)
    for i in range(n // 2 - 1, -1, -1):
        heapify(siyahi, n, i)
    for i in range(n - 1, 0, -1):
        siyahi[i], siyahi[0] = siyahi[0], siyahi[i]
        heapify(siyahi, i, 0)
    return siyahi
print(heap_sort([4, 10, 3, 5, 1]))