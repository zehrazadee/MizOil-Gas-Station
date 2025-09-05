# #Classwork

import time
import os

user_data = {}
def loading_bar():
    bar_length = 40
    for i in range(101):
        time.sleep(0.02)
        os.system("cls" if os.name == "nt" else "clear")
        filled = int(bar_length * i // 100)
        bar = "|" * filled + "-" * (bar_length - filled)
        print(f"[{bar}] {i}%")
    print("Yükləndi\n")

def login_page():
    global user_data
    while True:
        print("=== LOGIN PAGE ===")
        print("1. Login")
        print("2. Register")
        choice = input("Seçim edin: ")

        if choice == "1":
            if not user_data:
                print("Hələ heç bir hesab yoxdur. Zəhmət olmasa qeydiyyatdan keçin!\n")
                continue

            email = input("Email: ")
            password = input("Password: ")
            if email == user_data.get("email") and password == user_data.get("password"):
                print("Login uğurludur!\n")
                dashboard()
                return
            else:
                print("Email və ya şifrə səhvdir!\n")
        
        elif choice == "2":
            name = input("Ad: ")
            email = input("Email: ")
            password = input("Şifrə: ")
            user_data["name"] = name
            user_data["email"] = email
            user_data["password"] = password
            print("Qeydiyyat uğurla tamamlandı!\n")
            dashboard()
            return
        
        else:
            print("Yanlış seçim!\n")
def dashboard():
    global user_data
    while True:
        if not user_data:
            return

        print(f"\n=== DASHBOARD ===\nXoş gəldin, {user_data['name']}!\n")
        print("1. İstifadəçi məlumatlarına bax")
        print("2. İstifadəçi məlumatlarını dəyiş")
        print("3. Şifrəni dəyiş")
        print("4. Çıxış et")
        choice = input("Seçim edin: ")

        if choice == "1":
            print("\nİstifadəçi məlumatları:")
            print(f"Ad: {user_data.get('name')}")
            print(f"Email: {user_data.get('email')}")
            print(f"Şifrə: {user_data.get('password')}\n")
        
        elif choice == "2":
            new_name = input("Yeni ad: ")
            new_email = input("Yeni email: ")
            user_data["name"] = new_name
            user_data["email"] = new_email
            print("Ad və email yeniləndi!\n")

        elif choice == "3":
            new_pass = input("Yeni şifrə: ")
            user_data["password"] = new_pass
            print("Şifrə yeniləndi!\n")

        elif choice == "4":
            user_data.clear()
            print("Hesabdan çıxış edildi. Login səhifəsinə yönləndirilirsiniz...\n")
            return
        
        else:
            print("Yanlış seçim!\n")

loading_bar()
while True:
    login_page()