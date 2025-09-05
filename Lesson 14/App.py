#Task 1
def perfect_number(n):
    if n <= 1:
        return False
    
    total = 0
    i = 1
    half = n//2
    while i <= half:
        if n % i == 0:
            total += i
        i += 1

    return total == n

def perfects_up_to(limit):
    result = []
    num = 1
    while num <= limit:
        if perfect_number(num):
            result.append(num)
        num += 1
    return result

if __name__ == "__main__":
    print(perfect_number(24))
    print(perfect_number(28))
    print(perfect_number(6))

#Task 2
def card_from_number(n: int) -> str:
    ranks = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["♣", "♦", "♥", "♠"]

    if not (1<= n <= 36):
        return "Xəta: n, 1 ilə 36 arasında olmalıdır."
    i = n - 1
    suit_index = i // len(ranks)
    rank_index = i% len(ranks)
    return f"{ranks[rank_index]}{suits[suit_index]}"        
print(card_from_number(1))
print(card_from_number(12))
print(card_from_number(42))

#Task 3
def yuvarlaqla(number, ndigits = 0):
    if ndigits >= 0:
        faktor = 10 ** ndigits
        yeni_eded = number * faktor
    else:
        faktor = 10 ** (-ndigits)
        yeni_eded = number / faktor
    if yeni_eded >= 0:
        yeni_eded = int(yeni_eded + 0.5)
    else:
        yeni_eded = int(yeni_eded - 0.5)

    if ndigits >= 0:
        return yeni_eded / faktor
    else:
        return yeni_eded * faktor
    
print(yuvarlaqla(3.14159, 2)) 
print(yuvarlaqla(2.675, 2))    
print(yuvarlaqla(123, -1))     
print(yuvarlaqla(-2.675, 2))    

#Task 4
def happy_num(number):
    if number < 100000 or number > 999999:
        return False
    ilk_3 = number // 1000
    son_3 = number % 1000
    def cem_3reqemli(x):
        reqem1 = x // 100
        reqem2 = (x// 10) % 10
        reqem3 = x % 10
        return reqem1 + reqem2 + reqem3

    return cem_3reqemli(ilk_3) == cem_3reqemli(son_3)

print(happy_num(123123))
print(happy_num(111111))
print(happy_num(453879))

#Task 5
def leap_year(year):
    if(year % 400 == 0):
        return True
    if(year % 100 == 0):
        return False
    if(year % 4 == 0):
        return True
    return 

def days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if leap_year(year) else 28
    else:
        raise ValueError("Ay 1 - 12 arası yazılmalıdır")

def date_to_days(year, month, day):
    days = 0 
    for y in range(1, year):
        days += 366 if leap_year(y) else 365
    for m in range(1, month):
        days += days_in_month(year, m)
    days += day
    return days

def diff_between_dates(y1, m1, d1, y2, m2, d2):
    days1 = date_to_days(y1, m1, d1)
    days2 = date_to_days(y2, m2, d2)
    return abs(days2 - days1)

print(leap_year(2020))
print(leap_year(2023))

print(diff_between_dates(2020, 1, 1, 2020, 12, 31))
print(diff_between_dates(2023, 3, 1, 2024, 3, 1))
print(diff_between_dates(2023, 1, 1, 2023, 1, 1))

#Task 6
import random
def ededi_orta(massive):
    if massive == []:
        return None
    cem = 0
    say = 0
    for eded in massive:
        cem += eded
        say += 1
    return cem / say
massive = [random.randint(1, 100) for _ in range(10)]
print("Massiv:", massive)
print("Ədədi orta:", ededi_orta(massive))

#Task 7 
import random

def count_numbers(massiv):
    sifir_say = 0
    menfi_say = 0
    musbet_say = 0
    for eded in massiv:
        if eded == 0:
            sifir_say += 1
        elif eded < 0:
            menfi_say += 1
        else:
            musbet_say += 1
    return sifir_say, menfi_say, musbet_say

massiv = [1, 5, -3, 0, 9, 12, 15, 17, 22, 30]
sifir, menfi, musbet = count_numbers(massiv)
print("Sıfırların sayı:", sifir)
print("Mənfilərin sayı:", menfi)
print("Müsbətlərin sayı:", musbet)

#Task 8 
def find_max_min(massiv):
    if massiv == []:
        return None, None
    maksimum = massiv[0]
    minimum = massiv[0]
    for eded in massiv:
        if eded > maksimum:
            maksimum = eded
        if eded < minimum:
            minimum = eded
    return maksimum, minimum

massiv = [1, 5, -3, 0, 9]
maks, minm = find_max_min(massiv)
print("Maksimum:", maks)
print("Minimum:", minm)

#Task 9
def reverse_list(massiv):
    reversed_list = []
    index = 0
    for _ in massiv:
        index += 1
    index -= 1
    while index >= 0:
        reversed_list.append(massiv[index])
        index -= 1
    return reversed_list

massiv = [1, 2, 3, 4, 5]
print("Əksinə massiv:", reverse_list(massiv))

#Task 10
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
        
    return True

def count_primes(numbers):
    count = 0
    for n in numbers:
        if is_prime(n):
            count += 1
    return count

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 78, 87, 92, 100]
print(count_primes(nums))