#row == sətir, column == sütun
import tkinter as tk

root = tk.Tk()
root.title("Simple GUI")
root.geometry("300x200")
# tk.Label(root, text="Label 1", bg="red").pack(side="top")
# tk.Label(root, text="Label 1", bg="red").pack(side="left", fill="x", expand=True)
# tk.Label(root, text="Label 1", bg="red").pack(side="bottom", fill="y", expand=True)

#Grid
tk.Label(root, text="Label 1", bg="red").grid(row=0, column=0)
tk.Label(root, text="Label 2", bg="green").grid(row=0, column=1)
tk.Label(root, text="Label 3", bg="blue").grid(row=1, column=0, columnspan=2, sticky="we")
tk.Label(root, text="Label 4", bg="brown").grid(row=1, column=0, columnspan=2, sticky="nsew")

# #Place
# tk.Label(root, text="Label 1", bg="red").pack(side="left")
# tk.Label(root, text="Label 2", bg="red").pack(side="left")
# tk.Button(root, text="Button").place(relx=0.1, rely=0.1, relheight=0.5, relwidth=0.5, anchor="ne")
# tk.Label(root, text="Label 1", bg="red").place(x=50, y=70)

#Changed something
root.mainloop()