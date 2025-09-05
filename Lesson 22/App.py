# import tkinter as tk 
# root = tk.Tk()
# mainvalue = tk.StringVar(value = "1")

# tk.Radiobutton(root, text="Option 1", variable=mainvalue, value="1").pack()
# tk.Radiobutton(root, text="Option 2", variable=mainvalue, value="2").pack()
# tk.Radiobutton(root, text="Option 3", variable=mainvalue, value="3").pack()

# root.mainloop()

# #Istifadəçi adını, soyadını və yaşını daxil etsin
# #Milliyətini listbox - dan seçəcək
# #Cinsiyyətini radiobuttondan seçir
# #Button - a click edəndə console - a yazdırır
# import tkinter as tk

# root = tk.Tk()
# root.title("User Information")

# tk.Label(root, text="Ad:").pack()
# ad_entry = tk.Entry(root)
# ad_entry.pack()

# tk.Label(root, text="Soyad:").pack()
# soyad_entry = tk.Entry(root)
# soyad_entry.pack()

# tk.Label(root, text="Yaş:").pack()
# yas_entry = tk.Entry(root)
# yas_entry.pack()

# tk.Label(root, text="Milliyət:").pack()
# milliyet_listbox = tk.Listbox(root)
# milliyetler = ["Azərbaycan", "Türkiyə", "Gürcüstan", "Rusiya"]
# for milliyet in milliyetler:
#     milliyet_listbox.insert(tk.END, milliyet)
# milliyet_listbox.pack()

# tk.Label(root, text="Gender:").pack()
# gender_var = tk.StringVar(value="Kişi")
# tk.Radiobutton(root, text="Kişi", variable=gender_var, value="Kişi").pack()
# tk.Radiobutton(root, text="Qadın", variable=gender_var, value="Qadın").pack()

# def submit():
#     ad = ad_entry.get()
#     soyad = soyad_entry.get()
#     yas = yas_entry.get()
#     milliyet = milliyet_listbox.get(milliyet_listbox.curselection())
#     gender = gender_var.get()
#     print(f"Ad: {ad}, Soyad: {soyad}, Yaş: {yas}, Milliyyət: {milliyet}, Cinsiyyət: {gender}")

# tk.Button(root, text="Göndər", command=submit).pack()
# root.mainloop()

#Istifadəçi ad və soyad daxil edir
#Buttona click edəndə istifadəçi listboxda görünür
#silmə düyməsinə click edəndə seçilim istifadəçi silinir.

import tkinter as tk
from tkinter import messagebox
def add_user():
    name = entry_name.get().strip()
    if name:
        listbox.insert(tk.END, name)
        messagebox.showinfo("Information:", "Istifadəçi əlavə olundu.")
        entry_name.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning:", "Istifadəçi adı daxil edilməyib.")
def delete_user():
    try:
        selected_index = listbox.curselection()[0]
        user = listbox.get(selected_index)
        listbox.delete(selected_index)
        messagebox.showinfo("Information:", f"Istifadəçi silindi: {user}")
    except IndexError:
        messagebox.showwarning("Warning:", "Silinmək üçün istifadəçi seçilməyib.")
root = tk.Tk()
root.title("User Management")
root.geometry("300x400")

def update_user():
    try:
        selected_index = listbox.curselection()[0]
        new_name = entry_name.get().strip()
        if new_name:
            old_name = listbox.get(selected_index)
            listbox.delete(selected_index)
            listbox.insert(selected_index, new_name)
            messagebox.showinfo("Information:", f"Istifadəçi yeniləndi: {old_name} → {new_name}")
            entry_name.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning:", "Yeni istifadəçi adı daxil edilməyib.")
    except IndexError:
        messagebox.showwarning("Warning:", "Yenilənmək üçün istifadəçi seçilməyib.")

label = tk.Label(root, text="Istifadəçi adı:")
label.pack(pady=5)

entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

add_button = tk.Button(root, text="Əlavə et", command=add_user)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Sil", command=delete_user)
delete_button.pack(pady=5)

listbox = tk.Listbox(root, width=40, height=10)
listbox.pack(pady=10)

root.mainloop()