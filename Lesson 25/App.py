import tkinter as tk
from tkinter import messagebox

# Ana pəncərə
pencere = tk.Tk()
pencere.title("9 Frame - Rəqəm Klavyesi")
pencere.geometry("400x400")

# Başlıq
baslik = tk.Label(pencere, text="9 Frame - Rəqəm Tapıcı", font=("Arial", 16))
baslik.grid(row=0, column=0, columnspan=3, pady=10)

# Seçilən rəqəmləri göstər
secilen_reqemler = ""
gosterici = tk.Label(pencere, text="Seçilən: ", font=("Arial", 12), bg="lightblue")
gosterici.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

# Hər rəqəm üçün ayrı funksiya
def reqem_1():
    global secilen_reqemler
    secilen_reqemler += "1"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_2():
    global secilen_reqemler
    secilen_reqemler += "2"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_3():
    global secilen_reqemler
    secilen_reqemler += "3"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_4():
    global secilen_reqemler
    secilen_reqemler += "4"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_5():
    global secilen_reqemler
    secilen_reqemler += "5"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_6():
    global secilen_reqemler
    secilen_reqemler += "6"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_7():
    global secilen_reqemler
    secilen_reqemler += "7"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_8():
    global secilen_reqemler
    secilen_reqemler += "8"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def reqem_9():
    global secilen_reqemler
    secilen_reqemler += "9"
    gosterici.config(text=f"Seçilən: {secilen_reqemler}")

def temizle():
    global secilen_reqemler
    secilen_reqemler = ""
    gosterici.config(text="Seçilən: ")

def netice_goster():
    if secilen_reqemler == "":
        messagebox.showinfo("Boş", "Heç bir rəqəm seçməmisən!")
    else:
        # Hansı rəqəmlərin seçildiyini say
        reqem_sayilari = {}
        for reqem in secilen_reqemler:
            if reqem in reqem_sayilari:
                reqem_sayilari[reqem] += 1
            else:
                reqem_sayilari[reqem] = 1
        
        netice_metni = f"Seçilən rəqəmlər: {secilen_reqemler}\n\n"
        netice_metni += "Hər rəqəmin sayı:\n"
        
        for reqem, say in reqem_sayilari.items():
            netice_metni += f"Rəqəm {reqem}: {say} dəfə\n"
        
        messagebox.showinfo("Nəticə", netice_metni)

# 9 Frame - 3x3 grid
# Frame 1 (row=2, col=0) - Rəqəm 1
frame1 = tk.Frame(pencere, bg="lightgreen", relief="raised", bd=2)
frame1.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
btn1 = tk.Button(frame1, text="1", font=("Arial", 20), command=reqem_1)
btn1.pack(expand=True, fill="both")

# Frame 2 (row=2, col=1) - Rəqəm 2
frame2 = tk.Frame(pencere, bg="lightcoral", relief="raised", bd=2)
frame2.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
btn2 = tk.Button(frame2, text="2", font=("Arial", 20), command=reqem_2)
btn2.pack(expand=True, fill="both")

# Frame 3 (row=2, col=2) - Rəqəm 3
frame3 = tk.Frame(pencere, bg="lightblue", relief="raised", bd=2)
frame3.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
btn3 = tk.Button(frame3, text="3", font=("Arial", 20), command=reqem_3)
btn3.pack(expand=True, fill="both")

# Frame 4 (row=3, col=0) - Rəqəm 4
frame4 = tk.Frame(pencere, bg="lightyellow", relief="raised", bd=2)
frame4.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
btn4 = tk.Button(frame4, text="4", font=("Arial", 20), command=reqem_4)
btn4.pack(expand=True, fill="both")

# Frame 5 (row=3, col=1) - Rəqəm 5
frame5 = tk.Frame(pencere, bg="lightpink", relief="raised", bd=2)
frame5.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
btn5 = tk.Button(frame5, text="5", font=("Arial", 20), command=reqem_5)
btn5.pack(expand=True, fill="both")

# Frame 6 (row=3, col=2) - Rəqəm 6
frame6 = tk.Frame(pencere, bg="lightgray", relief="raised", bd=2)
frame6.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
btn6 = tk.Button(frame6, text="6", font=("Arial", 20), command=reqem_6)
btn6.pack(expand=True, fill="both")

# Frame 7 (row=4, col=0) - Rəqəm 7
frame7 = tk.Frame(pencere, bg="orange", relief="raised", bd=2)
frame7.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
btn7 = tk.Button(frame7, text="7", font=("Arial", 20), command=reqem_7)
btn7.pack(expand=True, fill="both")

# Frame 8 (row=4, col=1) - Rəqəm 8
frame8 = tk.Frame(pencere, bg="violet", relief="raised", bd=2)
frame8.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
btn8 = tk.Button(frame8, text="8", font=("Arial", 20), command=reqem_8)
btn8.pack(expand=True, fill="both")

# Frame 9 (row=4, col=2) - Rəqəm 9
frame9 = tk.Frame(pencere, bg="cyan", relief="raised", bd=2)
frame9.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")
btn9 = tk.Button(frame9, text="9", font=("Arial", 20), command=reqem_9)
btn9.pack(expand=True, fill="both")

# Alt hissə düymələr
btn_temizle = tk.Button(pencere, text="Təmizlə", font=("Arial", 12), command=temizle, bg="red", fg="white")
btn_temizle.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

btn_netice = tk.Button(pencere, text="Nəticə", font=("Arial", 12), command=netice_goster, bg="green", fg="white")
btn_netice.grid(row=5, column=1, columnspan=2, padx=5, pady=10, sticky="ew")

# Grid konfiqurasiyası - bərabər böl
for i in range(3):
    pencere.columnconfigure(i, weight=1)
for i in range(2, 5):
    pencere.rowconfigure(i, weight=1)

pencere.mainloop()