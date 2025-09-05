#Tkinter - GUI Programming
# import tkinter as tk
# root = tk.Tk()
# root.title("Tkinter GUI") #Pəncərə başlığı
# root.geometry("400x300+100+100") #Pəncərənin ölçüsü və yerləşməsi (mövqeyi)
# def click_me():
#     label_text.set(f"Hello, {entry_text.get()}")
#     entry_text.set(" ") #Entry-dəki mətni sıfırlayır

# entry_text = tk.StringVar()
# label_text = tk.StringVar() #Entry üçün StringVar yaradılır

# #root.resizable(False, False)
# tk.Label(root, text="Hello Tkinter!", font=("Arial", 20)).pack() #Etiket əlavə
# #tk.Label(root, text="Hello, Tkinter!", font=("Arial", 20)).pack()
# tk.Entry(root, font=("Arial", 20), textvariable=entry_text).pack() #Entry əlavə edirik
# tk.Button(root, text="Click Me", font=("Arial", 20), command=click_me).pack(pady=20) #Düymə əlavə edirik
# tk.Label(root, textvariable=label_text, font=("Arial", 20)).pack() #Etiket əlavə


#When the user enters two numbers, when they press the button, add the numbers and display the result in a label
# def click_me()
# :
# import tkinter as tk

# def add():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 + num2
#         result_var.set(f"Nəticə: {result}")
#     except ValueError:
#         result_var.set("Zəhmət olmasa ədəd daxil edin!")

# def substract():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 - num2
#         result_var.set(f"Nəticə: {result}")
#     except ValueError:
#         result_var.set("Zəhmət olmasa ədəd daxil edin!")

# def multiply():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 * num2
#         result_var.set(f"Nəticə: {result}")
#     except ValueError:
#         result_var.set("Zəhmət olmasa ədəd daxil edin!")

# def divide():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 / num2
#         result_var.set(f"Nəticə: {result}")
#     except ValueError:
#         result_var.set("Zəhmət olmasa ədəd daxil edin!")
#     except ZeroDivisionError:
#         result_var.set("Sıfıra bölmə xətası!")

# root = tk.Tk()
# root.title("Calculator")

# entry1 = tk.Entry(root, width = 10)
# entry1.pack(pady=5)

# entry2 = tk.Entry(root, width = 10)
# entry2.pack(pady=5)

# tk.Button(root, text="+", width=5, command=add).pack(pady=2)
# tk.Button(root, text="-", width=5, command=substract).pack(pady=2)
# tk.Button(root, text="*", width=5, command=multiply).pack(pady=2)
# tk.Button(root, text="/", width=5, command=divide).pack(pady=2)

# result_var = tk.StringVar()
# result_var.set("Nəticə: ")

# result_label = tk.Label(root, textvariable=result_var)
# result_label.pack(pady = 5)


# root.mainloop()




#İstifadəçi username və şifrə daxil edir hər ikisi admin olarsa "Uğurlu giriş" yaz, "əks halda "İstifadəçi adı və ya şifrə yanlışdır" yaz
import tkinter as tk
def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "admin":
        result_var.set("Uğurlu giriş")
    else:
        result_var.set("İstifadəçi adı və ya şifrə yanlışdır")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
def clear():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    result_var.set("")
    entry_username.focus()
    entry_password.delete(0, tk.END)
    entry_password.focus()
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

entry_password = tk.Entry(root)
entry_password.pack(pady=5)

tk.Button(root, text="Giriş", command=login).pack(pady=5)
tk.Button(root, text="Təmizlə", command=clear).pack(pady=5)

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var)
result_label.pack(pady=5)

root.mainloop()