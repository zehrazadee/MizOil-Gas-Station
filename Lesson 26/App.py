import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Simple GUI")

def changeCb(event):
    print(mycb.get())

mycb = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"], state="readonly")
mycb.bind("<<ComboboxSelected>>", changeCb)
mycb.pack(pady=10)
ttk.Button(root, text="Submit").pack(pady=10)

root.mainloop()