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
#       [2, "Tadı2", "Tsoyadı",11]
#         ]  
#     ]
# journal[0].pop(0)
# print(journal)



import uuid
import os
journal = []

while True:
    print("1. Jurnala bax\
           \n2. Telebe elave et\
          \n3. Telebeni redakte et\
          \n4. Qrup elave et\
          \n5. Telebeni xaric et\
          \n6. Telebeni goster\
          \n7. Cixis")
    secim = int(input("Seçiminizi daxil edin: "))
    if secim == 7:
        break
    elif secim == 1:
        for groupindex in range(len(journal)):
            print(f"=============={groupindex+1}===================")
            for telebe in journal[groupindex]:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                for melumat in telebe:
                    print(melumat, end=" ")
                print()
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("================================")
        os.system("pause")
    elif secim == 2:
        if len(journal)==0:
            journal.append([])
        for groupindex in range (len(journal)):
            print(f"{groupindex+1}) Qrup")
        qrupsecim = int(input("Telebe elave etmek istediyiniz qrupu secin."))
        if qrupsecim>len(journal):
            print("Düzgün qrup nömrəsi daxil edin.")
            os.system("Pause")
            continue
        qrupsecim-=1
        id = str(uuid.uuid4())
        name = input("Yeni telebenin adini daxil edin: ")
        surname = input("Yeni telebenin soyadini daxil edin: ")
        score = float(input("Yeni telebenin score - nu daxil edin: "))
        yenitelebe = [id, name, surname, score]
        journal[qrupsecim].append(yenitelebe)
    elif secim == 3:
            if len(journal)==0:
                print("Sistemdə tələbə yoxdur. Zəhmət olmasa tələbə əlavə edin.")
                os.system("Pause")
                continue
            for groupindex in range (len(journal)):
                print(f"{groupindex+1}) Qrup")
            qrupsecim = int(input("Telebe redakte etmek istediyiniz qrupu secin."))
            if qrupsecim>len(journal):
                print("Düzgün qrup nömrəsi daxil edin.")
                os.system("Pause")
                continue
            qrupsecim-=1
            for telebe in journal[qrupsecim]:
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    for melumat in telebe:
                        print(melumat, end=" ")
                    print()
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            telebesecim = input("Redaktə etmək istədiyiniz tələbənin id - sini daxil edin: ")
            edittelebe = None
            for telebe in journal[qrupsecim]:
                if telebe[0] == telebesecim:
                    edittelebe = telebe
                    break
            if edittelebe == None:
                print("Düzgün id daxil edin, daxil etdiyiniz id - də tələbə tapılmadı: ")
                os.system("Pause")
                continue


            name = input("Yeni telebenin adini daxil edin: ")
            surname = input("Yeni telebenin soyadini daxil edin: ")
            score = float(input("Yeni telebenin score - nu daxil edin: "))
            index = journal[qrupsecim].index(edittelebe)
            edittelebe[1] = name
            edittelebe[2] = surname
            edittelebe[3] = score
            journal[qrupsecim][index] = edittelebe
    elif secim == 4:
        cavab = input("Yeni qrup yaradım? (h/y)")
        if cavab.lower() == "h":
            journal.append([])
        else:
            print("Qrup əlavə edilmədi.")
    elif secim == 6:
            telebesecim = input("Görmək istədiyiniz tələbənin id - sini daxil edin: ")
            viewtelebe = None
            for group in journal:
                for telebe in group:
                    if telebe[0] == telebesecim:
                        viewtelebe = telebe
                        break
            if viewtelebe == None:
                print("Düzgün id daxil edin, daxil etdiyiniz id - də tələbə tapılmadı: ")
                os.system("Pause")
                continue
            for melumat in viewtelebe:
                print(melumat, end= " ")
            os.system("Pause")
            print()
    elif secim == 5:
        telebesecim = input("Görmək istədiyiniz tələbənin id - sini daxil edin: ")
        removeindex = None
        secgroupindex = None
        for groupindex in range(len(journal)):
            for telebeindex in range(len(journal[groupindex])):
                if journal[groupindex][telebeindex][0] == telebesecim:
                    removeindex = telebeindex
                    secgroupindex = groupindex
                    break
        if removeindex == None:
            print("Düzgün id daxil edin, daxil etdiyiniz id - də tələbə tapılmadı: ")
            os.system("Pause")
            continue    
        journal[secgroupindex].pop(telebeindex)

