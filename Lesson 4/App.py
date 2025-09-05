# #Task1
# AZN = float(input("AZN daxil edin:"))
# secim = int(input("Seçim edin (1 - Avro, 2 - Dollar, 3 - Rubl):"))
# if secim == 1:
#       print("Avro:", AZN / 1.98)
# elif secim == 2:
#       print("Dollar:", AZN / 1.71)
# elif secim == 3:
#       print("Rubl:", AZN / 0.0218)
# else:
#       print("Yanlış seçim etmisiniz.")
# #Task2
# istifadeci_qiymet = float(input("Qiyməti daxil edin:"))
# istifadeci_gram = float(input("Qramı daxil edin:"))
# if istifadeci_gram <= 0:
#      print("Qram düzgün daxil edilməyib.")
# elif 0 < istifadeci_gram <= 100:
#       print("Endirim yoxdur.")
# elif 100 < istifadeci_gram <= 200:
#       print("3 faiz endirim.", istifadeci_qiymet *97 /100)
# elif 200 < istifadeci_gram <= 300:
#       print("5 faiz endirim.", istifadeci_qiymet *95 /100)
# else:
#       print("7 faiz endirim.", istifadeci_gram *93 /100)
# #Task3
# eded = float(input("Kəsr ədəd daxil edin:"))
# tam_hisse = int(eded)
# if tam_hisse != 0:
#      print("Tam hissə var.", tam_hisse) 
# else:
#      print("Tam hissə yoxdur.")
# # #Task4
# saat = int(input("Saat daxil edin:"))
# deqiqe = int(input("Dəqiqə daxil edin:"))
# if saat > 23:
#       print("Saat düzgün daxil edilməyib.")
# elif saat < 23:
#       print("Saat düzgün daxil edilib.")
# if deqiqe > 59:
#       print("Dəqiqə düzgün daxil edilməyib")
# elif deqiqe < 59:
#       print("Dəqiqə düzgün daxil edilib.")
# #Task5
# ay = int(input("Doğulduğunuz ayı daxil edin."))
# gun = int(input("Doğulduğunuz günü daxil edin."))
# if (ay == 1 and gun >=20) or (ay == 2 and gun <=18):
#     print("Dolça bürcü.")
# elif (ay == 2 and gun >=19) or(ay == 3 and gun <=20):
#     print("Balıqlar bürcü.")
# elif (ay == 3 and gun >=21) or (ay == 4 and gun <=19):
#     print("Qoç bürcü.")
# elif (ay == 4 and gun >=20) and (ay == 5 and gun <=20):
#     print("Buğa bürcü.")
# elif (ay == 5 and gun >=21) and (ay == 6 and gun <=20):
#     print("Əkizlər bürcü.")
# elif(ay == 6 and gun >=21) and (ay == 7 and gun <=22):
#     print("Xərçəng bürcü.")
# elif (ay == 7 and gun >=23) and (ay == 8 and gun <=22):
#     print("Şir bürcü.")
# elif (ay == 8 and gun >=23) and (ay == 9 and gun <=22):
#     print("Qız bürcü.")
# elif (ay == 9 and gun >= 23) and (ay == 10 and gun <=22):
#     print("Tərəzi bürcü.")
# elif (ay == 10 and gun >= 23) or (ay == 11 and gun <= 21):
#     print("Əqrəb bürcü.")
# elif (ay == 11 and gun >= 22) or (ay == 12 and gun <= 21):
#     print("Oxatan bürcü.")
# elif (ay == 12 and gun >= 22) or (ay == 1 and gun <= 19):
#     print("Oğlaq bürcü.")
# else:
#     print("Yanlış gün və ya ay daxil etdiniz.")


# #Task1
# print("Oyun Menyusu.")
# print("1. Yeni oyun")
# print("2. Oyunu davam et")
# print("3. Çıxış")

# sechim = input("Zəhmət olmasa seçiminizi daxil edin (1-3): ")

# if sechim == "1":
#     print("Yeni oyuna başladınız!")
# elif sechim == "2":
#     print("Oyun davam edir.")
# elif sechim == "3":
#     print("Çıxış edildi!")
# else:
#     print("Yanlış seçim etdiniz.")

# #Task3
# il = int(input("İli daxil edin:"))

# if (il % 400  == 0) or (il % 4 == 0 and il % 100 != 0):
#     print("Bu uzun ildir.")
# else:
#     print("Bu uzun il deyil.") 

# #Task5
# ceki = float(input("Çəkinizi daxil edin."))
# boy = float(input("Boyunuzu daxil edin."))
# ideal_ceki = boy - 110
# if ceki > ideal_ceki:
#     atilan_ceki = ceki - ideal_ceki
#     print("Ideal çəkidən artıqdır.", atilan_ceki, "Kilo atmalısınız.")
# elif ceki > ideal_ceki:
#     alinasi_ceki = ideal_ceki - ceki
#     print("Ideal çəkidən azdır.", alinasi_ceki, "Kilo almalısınız.")
# else:
#     print("Təbriklər! Siz ideal çəkidəsiniz.")

#Homework
#Task1
print("Oyun Menyusu.")
print("1. Yeni oyun")
print("2. Oyunu davam et")
print("3. Çıxış")

sechim = input("Zəhmət olmasa seçiminizi daxil edin (1-3): ")

if sechim == "1":
    print("Yeni oyuna başladınız!")
elif sechim == "2":
    print("Oyun davam edir.")
elif sechim == "3":
    print("Çıxış edildi!")
else:
    print("Yanlış seçim etdiniz.")
  
#Task2
yas = int(input("Yaşınızı daxil edin: "))
cins = input("Cinsinizi daxil edin (kişi/qadın): ")

if cins == "kişi":
    if yas >= 65:
        print("Siz təqaüd yaşındasınız.")
    else:
        print("Siz hələ təqaüd yaşında deyilsiniz.")
elif cins == "qadın":
    if yas >= 60:
        print("Siz təqaüd yaşındasınız.")
    else:
        print("Siz hələ təqaüd yaşında deyilsiniz.")
else:
    print("Cins düzgün daxil edilməyib.")

#Task3
il = int(input("İli daxil edin:"))

if (il % 400  == 0) or (il % 4 == 0 and il % 100 != 0):
    print("Bu uzun ildir.")
else:
    print("Bu uzun il deyil.") 

#Task4
gun = int(input("Günü daxil et: "))
ay = int(input("Ayi daxil et: "))
il = int(input("Ili daxil et: "))

# Hər ayın gün sayı:
ay_gunleri = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Uzun il: (fevral 29 olacaqsa)
if (il % 4 == 0 and il % 100 != 0) or (il % 400 == 0):
    ay_gunleri[1] = 29

# Gün ayın son günüdürsə:
if gun == ay_gunleri[ay - 1]:
    gun = 1
    if ay == 12:
        ay = 1
        il += 1
    else:
        ay += 1
else:
    gun += 1

print("Növbəti gün:", gun, ".", ay, ".", il)

#Task5
ceki = float(input("Çəkinizi daxil edin."))
boy = float(input("Boyunuzu daxil edin."))
ideal_ceki = boy - 110
if ceki > ideal_ceki:
    atilan_ceki = ceki - ideal_ceki
    print("Ideal çəkidən artıqdır.", atilan_ceki, "Kilo atmalısınız.")
elif ceki > ideal_ceki:
    alinasi_ceki = ideal_ceki - ceki
    print("Ideal çəkidən azdır.", alinasi_ceki, "Kilo almalısınız.")
else:
    print("Təbriklər! Siz ideal çəkidəsiniz.")

#Task6
eded = int(input("0-dan 35-ə qədər ədəd daxil et: "))
if eded < 9:
    nov = "kərpic"
elif eded < 18:
    nov = "pika"
elif eded < 27:
    nov = "ürək"
else:
    nov = "xaç"

qaliq = eded % 9
if qaliq == 0:
    deyer = "6"
elif qaliq == 1:
    deyer = "7"
elif qaliq == 2:
    deyer = "8"
elif qaliq == 3:
    deyer = "9"
elif qaliq == 4:
    deyer = "10"
elif qaliq == 5:
    deyer = "valet"
elif qaliq == 6:
    deyer = "dama"
elif qaliq == 7:
    deyer = "karol"
else:
    deyer = "tuz"

print(deyer, nov)