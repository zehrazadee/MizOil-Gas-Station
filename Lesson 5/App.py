#Dövr -- Hər hansı bir işin 2 və ya daha artıq təkrarlanmasına deyilir.
#While --  Müəyyən şərt daxilində təkrarlanan dövrə deyilir.
#For -- Müəyyən aralıq daxilində təkrarlanan dövrə deyilir.
#While  vasiləsi ilə sonsuz dövr yaranır.
#Sonsuz dövrdə işləyən dövrü dayandırmaq üçün, Ctrl + C basılmalıdır ki, **dayansın**.
#Literal - öz dəyərini saxa=layana deyilir --- rvalue (dəyərini dəyişə bilmir.)
#Dəyişən - adı, tipi, ölçüsü, adresi olan ram - da yer tutan
#Break - dövrü dayandırır
#Continue - özündən aşağıdakı kodları istifadə etmir, növbəti iterasiyaya (təkrara) keçir.

#Task1
# while True:
#     parol = input("Parolunuzu daxil edin.")
#     username = input("Istifadəçi adınızı daxil edin.")
#     if username == "admin" and parol == "admin":
#         print("Welcome!")
#         break
#     else:
#         print("Yanlış username və ya password. Yenidən cəhd edin.")

# #Task2
# import random
# menfi_eded = 0
# musbet_eded = 0
# sifir_ededi = 0
# say = 0
# while say < 10:
#     x = random.randint(-5, 5)
#     print("Düşən ədəd:", x)
    
#     if x < 0:
#         menfi_eded += 1
#     elif x > 0:
#         musbet_eded += 1
#     else:
#         sifir_ededi += 1
    
#     say += 1
# menfi_faiz = (menfi_eded / 10) * 100
# musbet_faiz = (musbet_eded / 10) * 100
# sifir_faiz = (sifir_ededi / 10) * 100

# print("\n Nəticələr:")
# print("Mənfi faiz:", menfi_faiz, "%")
# print("Müsbət faiz:", musbet_faiz, "%")
# print("0 faiz:", sifir_faiz, "%")

# #Task3
# import random
# x = random.randint(1, 100)
# print("1 ilə 100 arasında bir ədəd seçildi. Tapmağa çalış.")

# isRunning = True
# cehd_sayi = 0 
# while isRunning:
#     texmini = int(input("Ədəd daxil et:"))
#     cehd_sayi += 1

#     if texmini == x: 
#         print("Congrats! Düz tapdın.")
#         print("Sən bunu", cehd_sayi, "cəhdə tapdın.")
#         isRunning = False
#     elif texmini < x:
#         print("Daha böyük bir ədəd daxil edin.")
#     else:
#         print("Daha kiçik bir ədəd daxil edin.")



#Homework
#Task 1
eded = 3
while eded <= 100:
    print(eded)
    eded = eded + 3

#Task 2
import random
eded = int(input("Ədəd daxil edin: "))
faktorial = 1
ifade = ""
while x > 0:
    faktorial = faktorial * x
    if ifade == "":
        ifade = str(x)
    else:
        ifade = str(x) + "*" + ifade
    x = x - 1
print(ifade + " = " + str(faktorial))

#Task 3
eded = int(input("Ədəd daxil edin: "))
final = ""
sayac = 0
while sayac < eded:
    final  = final + "*"
    sayac = sayac + 1
print(final)

#Task 4 
eded = 2
while eded <= 50:
    print(eded)
    eded = eded + 2

#Task 5
basla = int(input("İlk ədədi daxil edin: "))
son = int(input("Son ədədi daxil edin: "))
cem = 0
hasil = 1
eded = basla
while eded <= son:
    if eded % 2 == 0:
        cem = cem + eded
    else:
        hasil = hasil * eded
    eded = eded + 1
print("Cüt ədədlərin cəmi: ", cem)
print("Tək ədədlərin hasili: ", hasil)

#Task 12
number = int(input("Ədədi daxil edin: "))
ardicil_var = False
previous = -1
while number > 0:
    x = number % 10
    if x == previous:
        ardicil_var = True
        break
    previous = x
    number = number // 10

if ardicil_var:
    print("İki ardıcıl eyni rəqəm var.")
else:
    print("İki ardıcıl eyni rəqəm yoxdur.")

#Task 13
number = int(input("Ədədi daxil edin: "))
artan = True
previous = -1
while number > 0:
    x = number % 10
    if previous != -1 and x > previous:
        artan = False
        break
    previous = x
    number = number // 10

if artan:
    print("Rəqəmlər artan ardıcıllıqdadır.")
else:
    print("Rəqəmlər artan ardıcıllıqda deyil.")