# # #Lesson 18
# # def salam():
# #     x = 20
# #     def salam2():
# #         x = 10
# #         print(x)
# #     salam2()
# #     print(x)
# # salam()


# # def kalkulyator():
# #     print("Kalkulyator")
# #     print("Əməliyyatlar: +, -, *, /")
# #     print("Çıxış üçün 'q' yazın")
# #     try:
# #         while True:
# #             birinci_reqem = reqem_yaz("\nBirinci rəqəmi daxil edin (və ya 'q' çıxış üçün): ")
# #             if birinci_reqem is None:
# #                 print("Kalkulyatordan çıxılır...")
# #                 break
# #             emeliyyat = emeliyyat_al()

# #             ikinci_reqem = reqem_yaz("Ikinci rəqəmi daxil edin: ")
# #             if ikinci_reqem is None:
# #                 print("Kalkulyatordan çıxılır...")
# #                 break
# #             netice = hesablama_et(birinci_reqem, emeliyyat, ikinci_reqem)
# #             netice_goster(birinci_reqem, emeliyyat, ikinci_reqem, netice)
# #     except KeyboardInterrupt:
# #         print("\n\nProgram dayandırıldı!")
# #     except Exception as e:
# #         print(f"Gözlənilməz xəta: {e}")
# # if __name__ == "__main__":
# #     kalkulyator()


# def reqem_al(mesaj):
#     while True:
#         try:
#             daxil_edilmis = input(mesaj)
#             if daxil_edilmis.lower() == 'q':
#                 return None
#             return float(daxil_edilmis)
#         except ValueError:
#             print("XƏTA: Düzgün rəqəm daxil edin!")

# def emeliyyat_al():
#     while True:
#         try:
#             emeliyyat = input("Əməliyyatı seçin (+, -, *, /): ")
#             if emeliyyat in ['+', '-', '*', '/']:
#                 return emeliyyat
#             else:
#                 raise ValueError("Yalnız +, -, *, / əməliyyatları mümkündür!")
#         except ValueError as e:
#             print(f"XƏTA: {e}")

# def toplama(a, b):
#     return a + b

# def cixma(a, b):
#     return a - b

# def vurma(a, b):
#     return a * b

# def bolme(a, b):
#     try:
#         if b == 0:
#             raise ZeroDivisionError("Sıfıra bölmək olmaz!")
#         return a / b
#     except ZeroDivisionError as e:
#         print(f"XƏTA: {e}")
#         return None

# def hesablama_et(a, emeliyyat, b):
#     if emeliyyat == '+':
#         return toplama(a, b)
#     elif emeliyyat == '-':
#         return cixma(a, b)
#     elif emeliyyat == '*':
#         return vurma(a, b)
#     elif emeliyyat == '/':
#         return bolme(a, b)

# def netice_goster(a, emeliyyat, b, netice):
#     if netice is not None:
#         print(f"\nNəticə: {a} {emeliyyat} {b} = {netice}")
#     else:
#         print("Əməliyyat yerinə yetirilə bilmədi!")

# def kalkulyator():
#     print("=== KALKULYATOR ===")
#     print("Əməliyyatlar: +, -, *, /")
#     print("Çıxış üçün 'q' yazın")
    
#     while True:

#         birinci_reqem = reqem_al("\nBirinci rəqəmi daxil edin (və ya 'q' çıxış üçün): ")
#         if birinci_reqem is None:
#             print("Kalkulyatordan çıxılır...")
#             break
        
#         emeliyyat = emeliyyat_al()
        
#         ikinci_reqem = reqem_al("İkinci rəqəmi daxil edin: ")
#         if ikinci_reqem is None:
#             print("Kalkulyatordan çıxılır...")
#             break

#         netice = hesablama_et(birinci_reqem, emeliyyat, ikinci_reqem)
        
#         netice_goster(birinci_reqem, emeliyyat, ikinci_reqem, netice)

# kalkulyator()


# #Homework
import hashlib
import json
import os
from datetime import datetime
import re
def istifadeci_sistemi():
    data_file = "istifadeciler.json"
    def melumatlari_yukle():
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return{}
        return{}
    def melumatlari_yaddasa_ver(data):
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    def sifreni_hash_et(sifre):
        return hashlib.sha256(sifre.encode()).hexdigest()
    def email_yoxla(email):
        if '@' not in email:
            return False
        hisseler = email.split('@')
        if len(hisseler) != 2:
            return False
        ad_hissesi, domen_hissesi = hisseler
        if '.' not in domen_hissesi:
            return False
        domen_parcalari = domen_hissesi.split('.')
        if len(domen_parcalari[-1]) > 2:
            return False
        
        return True
    def sifre_gucunu_yoxla(sifre):
        if len(sifre) < 6:
            return False
        sifrenin_guc_bali = 0
        if re.search(r'[A-Z]',sifre): 
            sifrenin_guc_bali += 1
        if re.search(r'[a-z]',sifre): 
            sifrenin_guc_bali += 1
        if re.search(r'[0-9]',sifre): 
            sifrenin_guc_bali += 1
        if re.search(r'[!@#$%^&*(),.?|{}:;<>aha]',sifre): 
            sifrenin_guc_bali += 1

        if sifrenin_guc_bali >= 3:
            return True, "Powerful password"
        elif sifrenin_guc_bali >= 2:
            return True, "Good password"
        else:
            return False, "Weak password"
    try:
        istifadeciler = melumatlari_yukle()

        print("İstifadəçi sisteminə xoş gəlmisiniz!")
        print("=" * 55)
        print("1. Qeydiyyat")
        print("2. Giriş")
        print("3. Statistika görüntülə")
        print("4. Şifrə dəyişdirmə")
        print("5. Çıxış")
        print("=" * 55)
        secim = input("Seçiminizi edin(1 - 5): ").strip()
        if secim == "1":
            print("\n Qeydiyyat")
            print("-" * 20)
            while True:
                ad_soyad = input("Ad və Soyadınızı daxil edin: ").strip()
                if len(ad_soyad.split()) >= 2 and ad_soyad.replace(" ", "").isalpha():
                    break
                print("Düzgün Ad və Soyad daxil edin. (Ən az 2 söz və yalnız hərflər)")
            while True:
                username = input("İstifadəçi adını daxil edin: ").strip().lower()
                if len(username) < 6:
                    print("İstifadəçi adı ən az 6 simvoldan ibarət olmalıdır.")
                elif not username.replace('_','').isalnum():
                    print("İstifadəçi adı yalnız hərf, rəqəm və alt xətt(_) ola bilər.")
                elif username in istifadeciler:
                    print("Bu istifadəçi adı artıq mövcuddur.")
                else:
                    break
            while True:
                email = input("Email ünvanını daxil edin: ").strip().lower()
                if email_yoxla(email):
                    email_movcud = any(data.get('email') == email for data in istifadeciler.values())
                    if not email_movcud:
                        break
                    else:
                        print("Bu email artıq qeydiyyatdan keçib.")
                else:
                    print("Düzgün email formatı daxil edin.")
            while True:
                sifre = input("Şifrəni daxil edin: ").strip()
                sifre_uygun, mesaj = sifre_gucunu_yoxla(sifre)
                if sifre_uygun:
                    sifre_tekrar = input("Şifrəni təkrar daxil edin: ").strip()
                    if sifre == sifre_tekrar:
                        print(f"✅ {mesaj}")
                        break
                    else:
                        print("Şifrələr uyğun deyil.")
                else:
                    print(f"❌ {mesaj}")
            istifadeciler[username] = {
                'ad_soyad': ad_soyad,
                'email': email,
                'sifre': sifreni_hash_et(sifre),
                'qeydiyya_tarixi': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'giris_sayi': 0,
                'son_giris': None
            }
            melumatlari_yaddasa_ver(istifadeciler)
            print(f"\n {ad_soyad}, qeydiyyatınız uğurla tamamlandı!")
            print(f" Təsdiq linki {email} ünvanına göndərildi (simulyasiya)")
            
        elif secim == "2":
            print("\n GİRİŞ")
            print("-" * 20)
            
            if not istifadeciler:
                print(" Heç bir istifadəçi qeydiyyatdan keçməyib")
                return
            
            username = input("İstifadəçi adı: ").strip().lower()
            sifre = input("Şifrə: ").strip()
            
            if username in istifadeciler:
                if istifadeciler[username]['sifre'] == sifreni_hash_et(sifre):
                    istifadeciler[username]['giris_sayi'] += 1
                    istifadeciler[username]['son_giris'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    melumatlari_yaddasa_ver(istifadeciler)
                    
                    print(f"\n Xoş gəldiniz, {istifadeciler[username]['ad_soyad']}!")
                    print(f" Giriş sayınız: {istifadeciler[username]['giris_sayi']}")
                    print(f" Qeydiyyat tarixi: {istifadeciler[username]['qeydiyyat_tarixi']}")
                else:
                    print("❌ Şifrə səhvdir")
            else:
                print(" İstifadəçi tapılmadı")
                
        elif secim == "3":
            print("\n SİSTEM STATİSTİKASI")
            print("-" * 30)
            
            if not istifadeciler:
                print(" Heç bir istifadəçi qeydiyyatdan keçməyib")
                return
            
            print(f" Ümumi istifadəçi sayı: {len(istifadeciler)}")
            print(f" Ümumi giriş sayı: {sum(user['giris_sayi'] for user in istifadeciler.values())}")
            
            en_aktiv = max(istifadeciler.items(), key=lambda x: x[1]['giris_sayi'])
            print(f" Ən aktiv istifadəçi: {en_aktiv[1]['ad_soyad']} ({en_aktiv[1]['giris_sayi']} giriş)")
            
            son_qeydiyyat = max(istifadeciler.items(), key=lambda x: x[1]['qeydiyyat_tarixi'])
            print(f" Son qeydiyyat: {son_qeydiyyat[1]['ad_soyad']}")
            
        elif secim == "4":
            print("\n ŞİFRƏ DƏYİŞDİRMƏ")
            print("-" * 25)
            
            username = input("İstifadəçi adı: ").strip().lower()
            if username in istifadeciler:
                kohne_sifre = input("Köhnə şifrə: ").strip()
                if istifadeciler[username]['sifre'] == sifreni_hash_et(kohne_sifre):
                    while True:
                        yeni_sifre = input("Yeni şifrə: ").strip()
                        sifre_uygun, mesaj = sifre_gucunu_yoxla(yeni_sifre)
                        if sifre_uygun:
                            istifadeciler[username]['sifre'] = sifreni_hash_et(yeni_sifre)
                            melumatlari_yaddasa_ver(istifadeciler)
                            print("✅ Şifrə uğurla dəyişdirildi!")
                            break
                        else:
                            print(f"❌ {mesaj}")
                else:
                    print(" Köhnə şifrə səhvdir")
            else:
                print(" İstifadəçi tapılmadı")
                
        elif secim == "5":
            print(" Sistem tərk edildi. Sağ olun!")
            return
        else:
            print(" Səhv seçim! 1-5 arası rəqəm seçin")
            
    except KeyboardInterrupt:
        print("\n\n Proqram istifadəçi tərəfindən dayandırıldı")
    except Exception as e:
        print(f"\n Gözlənilməz xəta baş verdi: {str(e)}")
        print(" Dəstək üçün admin ilə əlaqə saxlayın")
    finally:
        print("\n Sistem təhlükəsiz şəkildə bağlandı")


istifadeci_sistemi()