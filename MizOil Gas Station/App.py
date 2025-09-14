import tkinter as tk
from tkinter import ttk, Toplevel
from datetime import datetime
import qrcode
from PIL import Image, ImageTk

# -----Köməkçi Funksiyalar
def to_float(s):
    try:
        return float(str(s).replace(',', '.'))
    except:
        return 0.0

def format_amount(x):
    return f"{x:.2f}".replace('.', ',')

# -----Fuel Section
class FuelSection:
    def __init__(self, parent, update_total_callback):
        self.update_total_callback = update_total_callback
        self.fuel_types = {"AI-92":1.0, "AI-95":2.5, "AI-98":3.0, "Dizel":1.8}

        frame = tk.LabelFrame(parent, text="Benzin", font=("Arial",14,"bold"), padx=10, pady=10, bg="white")
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        tk.Label(frame, text="Benzin növü:", bg="white", font=("Arial",12)).grid(row=0, column=0, sticky="w")
        self.selected_fuel = tk.StringVar(value="AI-92")
        self.fuel_combo = ttk.Combobox(frame, values=list(self.fuel_types.keys()),
                                       textvariable=self.selected_fuel, state="readonly", font=("Arial",12))
        self.fuel_combo.grid(row=0, column=1, padx=5, pady=5)
        self.fuel_combo.bind("<<ComboboxSelected>>", self.update_price)

        tk.Label(frame, text="Qiymət (AZN):", bg="white", font=("Arial",12)).grid(row=1, column=0, sticky="w")
        self.fuel_price_var = tk.StringVar(value=str(self.fuel_types["AI-92"]))
        tk.Label(frame, textvariable=self.fuel_price_var, bg="white", font=("Arial",12)).grid(row=1, column=1, sticky="w")

        self.fuel_mode = tk.StringVar(value="litre")
        tk.Radiobutton(frame, text="Litr", variable=self.fuel_mode, value="litre", bg="white",
                       font=("Arial",12), command=self.update_total).grid(row=2, column=0)
        tk.Radiobutton(frame, text="Manat", variable=self.fuel_mode, value="manat", bg="white",
                       font=("Arial",12), command=self.update_total).grid(row=2, column=1)

        tk.Label(frame, text="Miqdar:", bg="white", font=("Arial",12)).grid(row=3, column=0)
        self.fuel_entry_var = tk.StringVar()
        self.fuel_entry = tk.Entry(frame, textvariable=self.fuel_entry_var, font=("Arial",12), width=10)
        self.fuel_entry.grid(row=3, column=1, pady=5)
        self.fuel_entry_var.trace_add("write", lambda *args: self.update_total())

        tk.Label(frame, text="Məbləğ:", bg="white", font=("Arial",12)).grid(row=4, column=0)
        self.fuel_total_var = tk.StringVar(value="0,00")
        tk.Label(frame, textvariable=self.fuel_total_var, bg="white", font=("Arial",12,"bold"), fg="blue").grid(row=4, column=1)

    def update_price(self, event=None):
        price = self.fuel_types[self.selected_fuel.get()]
        self.fuel_price_var.set(str(price))
        self.update_total()

    def update_total(self):
        price = to_float(self.fuel_price_var.get())
        qty = to_float(self.fuel_entry_var.get())
        if self.fuel_mode.get() == "litre":
            cost = price * qty
            display_text = f"{format_amount(cost)} AZN"
        else:
            cost = qty
            litres = qty / price if price > 0 else 0
            display_text = f"{format_amount(litres)} Litr"
        self.fuel_total_var.set(display_text)
        self.update_total_callback()

    def get_amount(self):
        text = self.fuel_total_var.get()
        if "AZN" in text:
            return to_float(text.split()[0])
        else:
            return to_float(self.fuel_entry_var.get()) if self.fuel_mode.get() == "manat" else 0

    def get_receipt_info(self):
        price = to_float(self.fuel_price_var.get())
        qty = to_float(self.fuel_entry_var.get())
        if self.fuel_mode.get() == "litre":
            cost = price * qty
            return f"{self.selected_fuel.get()}, {qty} Litr = {cost:.2f} AZN"
        else:
            litres = qty / price if price > 0 else 0
            return f"{self.selected_fuel.get()}, {format_amount(litres)} Litr = {qty:.2f} AZN"

# -----Cafe Section
class CafeSection:
    def __init__(self, parent, update_total_callback):
        self.update_total_callback = update_total_callback
        self.cafe_items = {"Hotdog":4.0,"Hamburger":5.0,"Cola":3.0,"Coffee":2.5}

        frame = tk.LabelFrame(parent, text="Mini-Kafe", font=("Arial",14,"bold"), padx=10, pady=10, bg="white")
        frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)

        self.cafe_vars = {}
        self.cafe_entry_vars = {}
        self.cafe_entries = {}  # Entry widget-ləri saxlamaq üçün

        for idx, (item, price) in enumerate(self.cafe_items.items()):
            # Checkbox
            var = tk.IntVar(value=0)
            chk = tk.Checkbutton(frame, text=f"{item} ({price} AZN)", variable=var, bg="white", font=("Arial",12), anchor="w")
            chk.grid(row=idx, column=0, sticky="w")
            
            # Entry
            entry_var = tk.StringVar(value="1")
            entry = tk.Entry(frame, width=8, state="disabled", textvariable=entry_var, font=("Arial",12))
            entry.grid(row=idx, column=1)

            # Callback-ləri təyin et
            var.trace_add("write", lambda *args, item=item: self.toggle_entry(item))
            entry_var.trace_add("write", lambda *args: self.update_total())

            # Saxla
            self.cafe_vars[item] = var
            self.cafe_entry_vars[item] = entry_var
            self.cafe_entries[item] = entry

        tk.Label(frame, text="Kafe hesabı:", bg="white", font=("Arial",12)).grid(row=len(self.cafe_items), column=0)
        self.cafe_total_var = tk.StringVar(value="0,00")
        tk.Label(frame, textvariable=self.cafe_total_var, bg="white", font=("Arial",12,"bold"), fg="green").grid(row=len(self.cafe_items), column=1)

    def toggle_entry(self, item):
        """Checkbox seçildikdə entry-ni aktivləşdir/deaktivləşdir"""
        entry = self.cafe_entries[item]
        
        if self.cafe_vars[item].get() == 1:
            # Seçildi - entry-ni aktivləşdir və boş qoy
            entry.config(state="normal")
            self.cafe_entry_vars[item].set("")  # Boş et ki, istifadəçi özü yazsın
        else:
            # Seçim ləğv edildi - entry-ni deaktivləşdir və boş qoy
            entry.config(state="disabled")
            self.cafe_entry_vars[item].set("")  # Boş qoy
            
        self.update_total()

    def update_total(self):
        """Kafe məhsullarının ümumi məbləğini hesabla"""
        total = 0
        for item, var in self.cafe_vars.items():
            if var.get() == 1:  # Seçilibsə
                try:
                    qty = to_float(self.cafe_entry_vars[item].get())
                    price = self.cafe_items[item]
                    total += qty * price
                except:
                    pass  # Səhv olsa, 0 hesab et
        
        self.cafe_total_var.set(format_amount(total))
        # Ümumi hesabı yenilə
        self.update_total_callback()

    def get_amount(self):
        """Kafe məbləğini qaytarır"""
        return to_float(self.cafe_total_var.get())

    def get_receipt_info(self):
        """Çek üçün məlumat"""
        purchases = {}
        for item, var in self.cafe_vars.items():
            if var.get() == 1:
                qty = to_float(self.cafe_entry_vars[item].get())
                price = self.cafe_items[item]
                purchases[item] = (qty, price)
        return purchases

# -----Total Section
class TotalSection:
    def __init__(self, parent):
        frame = tk.LabelFrame(parent, text="Ümumi Hesab", font=("Arial",14,"bold"), padx=10, pady=10, bg="white")
        frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        
        tk.Label(frame, text="Ümumi:", bg="white", font=("Arial",12)).grid(row=0, column=0)
        self.total_var = tk.StringVar(value="0,00")
        tk.Label(frame, textvariable=self.total_var, bg="white", font=("Arial",14,"bold"), fg="red").grid(row=0, column=1)

    def update(self, fuel_amount, cafe_amount):
        """Ümumi məbləği yenilə"""
        total = fuel_amount + cafe_amount
        self.total_var.set(format_amount(total))

    def get_total(self):
        """Ümumi məbləği qaytarır"""
        return to_float(self.total_var.get())

# -----Receipt
def show_receipt(fuel_info, cafe_purchases, total_amount):
    receipt_win = Toplevel()
    receipt_win.title("Çek")
    receipt_win.geometry("400x500")
    receipt_win.configure(bg="white")
    
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    tk.Label(receipt_win, text=f"Tarix: {now}", font=("Arial",12), bg="white").pack(pady=5)

    tk.Label(receipt_win, text="Alınan məhsullar:", font=("Arial",12,"bold"), bg="white").pack(pady=5)
    tk.Label(receipt_win, text="----------------------", bg="white").pack()

    # Kafe məhsulları
    for item, (qty, price) in cafe_purchases.items():
        tk.Label(receipt_win, text=f"{item} x{qty} = {qty*price:.2f} AZN",
                 font=("Arial",12), bg="white").pack(pady=2)

    tk.Label(receipt_win, text="----------------------", bg="white").pack()
    tk.Label(receipt_win, text="Benzin:", font=("Arial",12,"bold"), bg="white").pack()
    tk.Label(receipt_win, text=fuel_info, font=("Arial",12), bg="white").pack()

    tk.Label(receipt_win, text="----------------------", bg="white").pack()
    tk.Label(receipt_win, text=f"Ümumi: {total_amount:.2f} AZN", font=("Arial",14,"bold"), fg="red", bg="white").pack(pady=10)

    # QR Kod
    qr_data = f"Ödənilən məbləğ: {total_amount:.2f} AZN"
    qr_img = qrcode.make(qr_data)
    qr_img.save("qr.png")
    img = Image.open("qr.png")
    img = img.resize((120,120))
    qr_photo = ImageTk.PhotoImage(img)
    qr_label = tk.Label(receipt_win, image=qr_photo, bg="white")
    qr_label.image = qr_photo
    qr_label.pack(pady=10)

# -----Main App
class App:
    def __init__(self, root):
        root.title("MizOil Kassa Sistemi")
        root.geometry("950x600")
        root.configure(bg="#f0f0f0")

        # Komponentləri yarat
        self.total_section = TotalSection(root)
        self.fuel_section = FuelSection(root, self.update_total)
        self.cafe_section = CafeSection(root, self.update_total)

        # Hesabla düyməsi
        self.calc_btn = tk.Button(root, text="Hesabla", font=("Arial",12,"bold"),
                                  bg="orange", fg="white", command=self.calculate)
        self.calc_btn.grid(row=2, column=1, sticky="e", padx=10, pady=10)

    def update_total(self):
        """Ümumi məbləği yenilə"""
        # Benzin məbləği
        fuel_amt = self.fuel_section.get_amount()
        
        # Kafe məbləği
        cafe_amt = self.cafe_section.get_amount()
        
        # Ümumi hesabı yeniləmək
        self.total_section.update(fuel_amt, cafe_amt)

    def calculate(self):
        """Çek göstər"""
        fuel_info = self.fuel_section.get_receipt_info()
        cafe_purchases = self.cafe_section.get_receipt_info()
        total_amt = self.total_section.get_total()
        show_receipt(fuel_info, cafe_purchases, total_amt)

#Programı Çalışdırmaq
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()