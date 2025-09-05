# import tkinter as tk
# from tkinter import messagebox

# root = tk.Tk()
# root.title("Sadə Kalkulyator")

# entry1 = tk.Entry(root, width=20)
# entry1.pack(pady=5)

# entry2 = tk.Entry(root, width=20)
# entry2.pack(pady=5)

# result_entry = tk.Entry(root, width=20)
# result_entry.pack(pady=5)

# def add():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 + num2
#         result_entry.delete(0, tk.END)
#         result_entry.insert(0, str(result))
#     except ValueError:
#         messagebox.showerror("Xəta", "Ədədləri düzgün daxil edin!")

# def subtract():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 - num2
#         result_entry.delete(0, tk.END)
#         result_entry.insert(0, str(result))
#     except ValueError:
#         messagebox.showerror("Xəta", "Ədədləri düzgün daxil edin!")

# def multiply():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         result = num1 * num2
#         result_entry.delete(0, tk.END)
#         result_entry.insert(0, str(result))
#     except ValueError:
#         messagebox.showerror("Xəta", "Ədədləri düzgün daxil edin!")

# def divide():
#     try:
#         num1 = float(entry1.get())
#         num2 = float(entry2.get())
#         if num2 == 0:
#             messagebox.showerror("Xəta", "0-a bölmək olmaz!")
#             return
#         result = num1 / num2
#         result_entry.delete(0, tk.END)
#         result_entry.insert(0, str(result))
#     except ValueError:
#         messagebox.showerror("Xəta", "Ədədləri düzgün daxil edin!")


# button_add = tk.Button(root, text="+", width=10, command=add)
# button_add.pack(pady=2)

# button_sub = tk.Button(root, text="-", width=10, command=subtract)
# button_sub.pack(pady=2)

# button_mul = tk.Button(root, text="*", width=10, command=multiply)
# button_mul.pack(pady=2)

# button_div = tk.Button(root, text="/", width=10, command=divide)
# button_div.pack(pady=2)
# root.mainloop()

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("400x400")
root.title("Tic Tac Toe")
def checkWinner():
    b1 = button1.get()
    b2 = button2.get()
    b3 = button3.get()
    b4 = button4.get()
    b5 = button5.get()
    b6 = button6.get()
    b7 = button7.get()
    b8 = button8.get()
    b9 = button9.get()
    if b1 == b2 == b3 and b1 != "":
        messagebox.showinfo("Info", f"{b1} is the winner!")
    elif b4 == b5 == b6 and b4 != "":
        messagebox.showinfo("Info", f"{b4} is the winner!")
    elif b7 == b8 == b9 and b7 != "":
        messagebox.showinfo("Info", f"{b7} is the winner!")
    elif b1 == b4 == b7 and b1 != "":
        messagebox.showinfo("Info", f"{b1} is the winner!")
    elif b2 == b5 == b8 and b2 != "":
        messagebox.showinfo("Info", f"{b2} is the winner!")
    elif b3 == b6 == b9 and b3 != "":
        messagebox.showinfo("Info", f"{b3} is the winner!")
    elif b1 == b5 == b9 and b1 != "":
        messagebox.showinfo("Info", f"{b1} is the winner!")
    elif b3 == b5 == b7 and b3 != "":
        messagebox.showinfo("Info", f"{b3} is the winner!")

xTurn = True
def on_click_1():
    if button1.get() == "":
        if xTurn.get():
            button1.set("x")
            xTurn.set(False)
        else:
            button1.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")

def on_click_2():
    if button2.get() == "":
        if xTurn.get():
            button2.set("x")
            xTurn.set(True)
        else:
            button2.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_3():
    if button3.get() == "":
        if xTurn.get():
            button3.set("x")
            xTurn.set(False)
        else:
            button3.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_4():
    if button4.get() == "":
        if xTurn.get():
            button4.set("x")
            xTurn.set(False)
        else:
            button4.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_5():
    if button5.get() == "":
        if xTurn.get():
            button5.set("x")
            xTurn.set(False)
        else:
            button5.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_6():
    if button6.get() == "":
        if xTurn.get():
            button6.set("x")
            xTurn.set(False)
        else:
            button6.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_7():
    if button7.get() == "":
        if xTurn.get():
            button7.set("x")
            xTurn.set(False)
        else:
            button7.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_8():
    if button8.get() == "":
        if xTurn.get():
            button8.set("x")
            xTurn.set(False)
        else:
            button8.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")
        
def on_click_9():
    if button9.get() == "":
        if xTurn.get():
            button9.set("x")
            xTurn.set(False)
        else:
            button9.set("O")
            xTurn.set(True)
    else:
        messagebox.showinfo("Info", "This cell is already taken.")


xTurn = tk.BooleanVar(value = True)
button1 = tk.StringVar(value="")
button2 = tk.StringVar(value="")
button3 = tk.StringVar(value="")
button4 = tk.StringVar(value="")
button5 = tk.StringVar(value="")
button6 = tk.StringVar(value="")
button7 = tk.StringVar(value="")
button8 = tk.StringVar(value="")
button9 = tk.StringVar(value="")

tk.Button(root, height = 10, width = 50, textvariable = button1, command = on_click_1).grid(row = 0, column = 0, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button2, command = on_click_2).grid(row = 0, column = 1, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button3, command = on_click_3).grid(row = 0, column = 2, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button4, command = on_click_4).grid(row = 1, column = 0, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button5, command = on_click_5).grid(row = 1, column = 1, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button6, command = on_click_6).grid(row = 1, column = 2, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button7, command = on_click_7).grid(row = 2, column = 0, pady = 5, padx = 5)
tk.Button(root, height = 10, width = 50, textvariable = button8, command = on_click_8).grid(row = 2, column = 1, pady = 5, padx = 5) 
tk.Button(root, height = 10, width = 50, textvariable = button9, command = on_click_9).grid(row = 2, column = 2, pady = 5, padx = 5)

root.mainloop()