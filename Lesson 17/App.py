# #Lesson 17
# import uuid
# students = [
# {
#     "id": uuid.uuid4()

# }
# ]

telebeler = [
    {"id": 1, "name": "Zehra", "surname": "Mammadzada", "age": "16", "score": "90"},
    {"id": 2, "name": "Ayan", "surname": "Cabbarova", "age": "16", "score": "88"}
]
def goster():
    for telebe in telebeler:
        print(f"ID: {telebe['id']}, Name: {telebe['name']}, Surname: {telebe['surname']}, Age: {telebe['age']}, Score: {telebe['score']}")

def elave_et():
    yeni_id = len(telebeler) + 1
    name = input("Name: ")
    surname = input("Surname: ")
    age = int(input("Age: "))
    score = int(input("Score: "))
    telebeler.append({"id": yeni_id, "name": name, "surname": surname, "age": age, "score": score})
    print("Əlavə edildi!")

def sil():
    telebe_id = int(input("Silinəcək ID: "))
    for telebe in telebeler:
        if telebe['id'] == telebe_id:
            telebeler.remove(telebe)
            print("Silindi!")
            return
    print("Tapılmadı!")

def update():
    telebe_id = int(input("Yenilənəcək ID: "))
    for telebe in telebeler:
        if telebe['id'] == telebe_id:
            telebe['name'] = input("Yeni Name: ")
            telebe['surname'] = input("Yeni Surname: ")
            telebe['age'] = int(input("Yeni Age: "))
            telebe['score'] = int(input("Yeni Score: "))
            print("Yeniləndi!")
            return
    print("Tapılmadı!")

while True:
    print("\n1-Göstər 2-Əlavə et 3-Sil 4-Update 5-Çıxış")
    secim = int(input("Seçim: "))
    
    if secim == 1:
        goster()
    elif secim == 2:
        elave_et()
    elif secim == 3:
        sil()
    elif secim == 4:
        update()
    elif secim == 5:
        break
