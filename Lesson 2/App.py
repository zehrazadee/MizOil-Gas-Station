 #Task 1
# ticket = float(input("Bilet qiymetini daxil edin"))
# boyukler = int(input("Boyuklerin sayini daxil edin"))
# kicikler = int(input("Kiciklerin sayini daxil edin"))
# qiymet = ( ticket*boyukler + ticket*kicikler*0.6)
# print("Ümumi məbləğ", qiymet)

 #Task 2
# eded = int(input("Üçrəqəmli ədəd daxil edin (məsələn 315):"))
# yuzluk = (eded //100) %10
# onluq = (eded//10) %10
# teklik = (eded //1) % 10 
# print(yuzluk, onluq, teklik, sep=',')

 #Task 3
# number = int(input("Dörd rəqəmli ədəd daxil edin (məsələn, 1234): "))
# teklik = (number//1)%10
# onluq = (number //10)%10
# yuzluk = (number//100)%10
# minlik= (number//1000)%10

# print("1 - ci və 3 - cünün cəmi:", minlik + onluq)
# print("2 - ci və 4 - cünün fərqi:", yuzluk + teklik)

 #Task 4
# num1 = float(input("1. Kesr ədədi daxil edin: "))
# num2 = float(input("2. Kesr ədədi daxil edin: "))
# num1tam = num1//1
# num2tam = num2//1
# num1kesr = num1 - num1tam
# num2kesr = num2 - num2tam
# tamlarincemi = num1tam + num2tam
# kesrlerincemi = num1kesr + num2kesr
# print("Tamların cəmi:" , tamlarincemi)
# print("Kəsrlərin cəmi:" ,kesrlerincemi)

 #Task 5
# pul = float(input("Pulunuzu kəsrlə daxil edin:")) #1.3
# manat = int(pul) #1
# qepik = (pul - manat)*100
# print(pul,"->", manat, "manat", qepik, "qepikdir")

#Homework
#Task1
flash_gb = int(input("Flaş drive - ın ölçüsünü GB ilə daxil edin:"))
flash_mb = flash_gb*1024
film_sayi = flash_mb // 760
print("Flaşa yerləşəcək film sayı:", film_sayi)

 #Task2
eded = int(input("1 - 20 arası ədəd daxil edin:"))
print(
    eded == 2 or
    eded == 3 or
    eded == 5 or
    eded == 7 or
    eded == 11 or
    eded == 13 or
    eded == 17 or
    eded == 19
)

 #Task3
eded = input("5 rəqəmli ədəd daxil et:")
print(eded[0] == eded[4] and eded[1] == eded[3])

#Task4
eded = input("1-5 rəqəmli bir ədəd daxil et: ") + "    "
print("Bu ədəd", 
       (eded[4] != " ") * 5 +
       (eded[3] != " ") * 4 +
       (eded[2] != " ") * 3 +
       (eded[1] != " ") * 2 +
       (eded[0] != " ") * 1,
       "rəqəmlidir.")

#  #Task5
a = int(input("1-ci ədədi daxil et: "))
b = int(input("2-ci ədədi daxil et: "))
c = int(input("3-cü ədədi daxil et: "))

print("1-ci:", (a > b) * (a > c) == 1)
print("2-ci:", (b > a) * (b > c) == 1)
print("3-cü:", (c > a) * (c > b) == 1)
