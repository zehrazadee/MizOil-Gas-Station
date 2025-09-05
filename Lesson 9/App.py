#Müxtəlif tipli elementləri 1 dəyişən adı altında saxlamağa list deyilir.
#string - hərflərdən, rəqəmlərdən, simvollardan ibarət mətn parçasıdır.
#Iterator - hər bir təkrarda qayıdan dəyər
#Iterasiya - bir prosesin təkrar-təkrar yerinə yetirilməsi deməkdir.
#Mutable -  (dəyişilə bilən) — proqramlaşdırmada bir obyektin yaradıldıqdan sonra içindəki
# məlumatların dəyişdirilə bilməsi deməkdir.
#Ascending - artan sırada düzülmək deməkdir.
#Descending -  azalan sırada düzülmək deməkdir.
#Clean method - listin içindəki hər şeyi silir, listi silmir.
#Pop method -  Axırıncı elementi silir. Pop - un içində index yazılsa, içindəkini silir.
#Del keyword - Dəyişəni məhv edir. Bir şeyi tamailə silir.Məsələn x adında dəyişən var. For example:
#x = 5
#print(x)
#del x
#print(x) --- error verəcək
#Append - sondan listə string əlavə edir.
#Insert - list (siyahı) üzərində istifadə olunan bir metoddur və siyahıya istədiyin yerdə yeni 
# element əlavə etməyə imkan verir.
#Extend Method -  list-lərin elementlərini başqa bir listə əlavə etmək üçün istifadə olunur.
#a = [1, 2, 3]
#b = [4, 5, 6]
#a.extend(b)
#print(a)  # [1, 2, 3, 4, 5, 6]
#Shallow copy - Adress copyalanır.
#Deep copy - Obyektin bütün səviyyələrini, yəni içindəki bütün obyektləri də copyalayır.

#E - Journal --- list
#Qruplar - Telebeler ->  ID, adı, soyadı, ortalama score (12 olmalıdır)
#Qrupların daxilində telebeler listi var, telebeler listinin daxilində
#adı soyadı score(max 12) olur

#Exercise
# journal = [
#     [
#         [1,"TAdı","TSoyad", 11.2],
#         [2, "TAdı2", "TSoyadı",11]
#         ],
#     [
#         [1,"TAdı","TSoyad", 11.2],
#         [2, "Tadı2", "Tsoyadı",11]
#         ],
#     [
#         [1,"TAdı","TSoyad", 11.2],
#         [2, "Tadı2", "Tsoyadı",11]
#         ]  
#     ]
# journal[0].pop(0)
# print(journal)
# qruplar = {
#     "Math": [],
#     "Physics": [],
#     "Chemistry": []
# }

# next_id = 1

# while True:
#     print("\n E-Journal Sistemi")
#     print("1) Jurnala bax")
#     print("2) Tələbə əlavə et")
#     print("3) Tələbə düzəliş et")
#     print("4) Tələbə sil")
#     print("5) Tələbə göstər")
#     print("6) Çıxış")

#     secim = input("Seçiminiz: ").strip()

#     if secim == "1":
#         for qrup in qruplar:
#             print("\n Qrup: " + qrup)
#             telebeler = qruplar[qrup]
#             if len(telebeler) == 0:
#                 print("  Hələ tələbə yoxdur.")
#             for telebe in telebeler:
#                 print("  ID: " + str(telebe["id"]) + " - " + telebe["ad"] + " " + telebe["soyad"] + " - Score: " + str(telebe["score"]))

#     elif secim == "2":
#         print("\nTələbə əlavə et")
#         qrup = input("Qrup adı (məsələn, Riyaziyyat): ").strip()
#         if qrup not in qruplar:
#             print("Bu adda qrup yoxdur! Yeni qrup yaradılır.")
#             qruplar[qrup] = []
#         ad = input("Ad: ").strip()
#         soyad = input("Soyad: ").strip()
#         while True:
#             try:
#                 score = float(input("Score (maksimum 12): "))
#                 if 0 <= score <= 12:
#                     break
#                 else:
#                     print("Score 0-dan 12-yə qədər olmalıdır.")
#             except:
#                 print("Düzgün ədəd daxil edin.")
#         telebe = {"id": next_id, "ad": ad, "soyad": soyad, "score": score}
#         qruplar[qrup].append(telebe)
#         print("Tələbə əlavə edildi. ID: " + str(next_id))
#         next_id += 1


#join method - araşdır nə ilə işləyir, genel araşdır
#(exception nədir?)
#find - mənfi bir qaytarır 
#index - kodu çökdürür(məncə)


journal = [
    [
        [1,"TAdı","TSoyad", 11.2],
        [2, "TAdı2", "TSoyadı",11]
        ],
    [
        [1,"TAdı","TSoyad", 11.2],
        [2, "Tadı2", "Tsoyadı",11]
        ],
    [
        [1,"TAdı","TSoyad", 11.2],
        [2, "Tadı2", "Tsoyadı",11]
        ]  
    ]

# journal[0].pop(0)
# print(journal)
# while True:
#     print("1. jurmnala bax.\
#             \n2. Telebe elave et\
#             \n3. )
