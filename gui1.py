import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from threading import Timer

# Szimulált adatbázis a buszokhoz és menetrendekhez
routes = {
    "10500001": [
        {"stop": "Kossuth tér", "time": "08:00"},
        {"stop": "Deák tér", "time": "08:10"},
        {"stop": "Astoria", "time": "08:15"},
        {"stop": "Blaha Lujza tér", "time": "08:20"},
        {"stop": "Keleti", "time": "08:30"}
    ],
    "500001": [
        {"stop": "Hősök tere", "time": "09:00"},
        {"stop": "Oktogon", "time": "09:10"},
        {"stop": "Nyugati pályaudvar", "time": "09:20"},
        {"stop": "Deák tér", "time": "09:30"},
        {"stop": "Kálvin tér", "time": "09:40"}
    ],
    "21300001": [
        {"stop": "Nyugati pályaudvar", "time": "10:00"},
        {"stop": "Oktogon", "time": "10:10"},
        {"stop": "Hősök tere", "time": "10:20"},
        {"stop": "Deák tér", "time": "10:30"},
        {"stop": "Kossuth tér", "time": "10:40"}
    ]
}

# Sofer azonosítók és járműazonosítók
drivers = {
    "1": {"vehicle_ids": ["10500001", "500001", "21300001"], "name": "járműmozgató"}
}

# Globális változók a járműszámához és soför azonosítójához
vehicle_id = ""
driver_id = ""

# Rendszer színek kezelése (placeholder színek, ha nem adunk meg URL-t)

# Kép placeholder - URL használata
def load_image(url, width=200, height=200):
    try:
        image = PhotoImage(file=url)
        image = image.subsample(width // 100, height // 100)  # Kép átméretezése
        return image
    except Exception as e:
        print(f"Hiba a kép betöltésekor: {e}")
        return None

# Ablak beállítások
window = tk.Tk()
window.title("IVU Szimuláció")
window.geometry("720x480")

# Egyedi gombstílus
style = ttk.Style()
style.configure("Custom.TButton")

# Boot képernyő
def boot_screen():
    for widget in window.winfo_children():
        widget.destroy()

    boot_label = tk.Label(window, text="Rendszer indítása...", font=("Consolas", 18))
    boot_label.pack(expand=True)

    # 3 másodperc után a bejelentkezési képernyő jön
    Timer(3.0, login_screen).start()

# Bejelentkezési képernyő
def login_screen():
    for widget in window.winfo_children():
        widget.destroy()

    def add_digit(digit):
        nonlocal driver_id_label
        global driver_id
        driver_id += digit
        driver_id_label.config(text=driver_id)

    def clear_input():
        nonlocal driver_id_label
        global driver_id
        driver_id = ""
        driver_id_label.config(text="")

    def submit_driver():
        if driver_id in drivers:
            vehicle_screen()
        else:
            error_label.config(text="Hibás soförazonosító!")

    frame = tk.Frame(window)
    frame.pack(expand=True, fill="both")

    left_frame = tk.Frame(frame)
    left_frame.pack(side="left", fill="y", padx=20, pady=20)

    driver_id_label = tk.Label(left_frame, text="Kérem adja meg soförazonosítóját", font=("Helvetica", 16), anchor="w")
    driver_id_label.pack(fill="both", pady=10)

    right_frame = tk.Frame(frame)
    right_frame.pack(side="right", padx=20, pady=20)

    keypad_frame = tk.Frame(right_frame)
    keypad_frame.pack()

    for i, digit in enumerate("1234567890"):
        button = ttk.Button(keypad_frame, text=digit, command=lambda d=digit: add_digit(d),
                            width=5, style="Custom.TButton")
        button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    ttk.Button(right_frame, text="Törlés", command=clear_input, style="Custom.TButton").pack(pady=5)
    ttk.Button(right_frame, text="Tovább", command=submit_driver, style="Custom.TButton").pack(pady=10)

    error_label = tk.Label(window, text="", font=("Helvetica", 14), fg="red")
    error_label.pack()

# Járműszám megadása
def vehicle_screen():
    for widget in window.winfo_children():
        widget.destroy()

    def add_digit(digit):
        nonlocal vehicle_id_label
        global vehicle_id
        vehicle_id += digit
        vehicle_id_label.config(text=vehicle_id)

    def clear_input():
        nonlocal vehicle_id_label
        global vehicle_id
        vehicle_id = ""
        vehicle_id_label.config(text="")

    def submit_vehicle():
        if vehicle_id in drivers[driver_id]["vehicle_ids"]:
            route_screen()
        else:
            error_label.config(text="Hibás járműazonosító!")

    frame = tk.Frame(window)
    frame.pack(expand=True, fill="both")

    left_frame = tk.Frame(frame)
    left_frame.pack(side="left", fill="y", padx=20, pady=20)

    vehicle_id_label = tk.Label(left_frame, text="Kérem adja meg járműazonosítóját", font=("Helvetica", 16), anchor="w")
    vehicle_id_label.pack(fill="both", pady=10)

    right_frame = tk.Frame(frame)
    right_frame.pack(side="right", padx=20, pady=20)

    keypad_frame = tk.Frame(right_frame)
    keypad_frame.pack()

    for i, digit in enumerate("1234567890"):
        button = ttk.Button(keypad_frame, text=digit, command=lambda d=digit: add_digit(d),
                            width=5, style="Custom.TButton")
        button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    ttk.Button(right_frame, text="Törlés", command=clear_input, style="Custom.TButton").pack(pady=5)
    ttk.Button(right_frame, text="Tovább", command=submit_vehicle, style="Custom.TButton").pack(pady=10)

    error_label = tk.Label(window, text="", font=("Helvetica", 14), fg="red")
    error_label.pack()

# Járatok és megállók megjelenítése
def route_screen():
    for widget in window.winfo_children():
        widget.destroy()

    tk.Label(window, text=f"Soför: {drivers[driver_id]['name']} | Jármű: {vehicle_id}", font=("Helvetica", 14)).pack(pady=10)

    left_frame = tk.Frame(window)
    left_frame.pack(side="left", fill="both", padx=20, pady=20)

    route_list = routes.get(vehicle_id, [{"stop": "Nincs adat", "time": "Nincs adat"}])
    
    # Menetrend megjelenítése
    listbox = tk.Listbox(left_frame, height=10, font=("Helvetica", 14))
    listbox.pack(side="left", fill="y", padx=10)

    for stop in route_list:
        listbox.insert(tk.END, f"{stop['stop']} - {stop['time']}")

    # Nyilak a lista navigálásához
    def scroll_up(event):
        listbox.yview_scroll(-1, "units")

    def scroll_down(event):
        listbox.yview_scroll(1, "units")

    listbox.bind("<Up>", scroll_up)
    listbox.bind("<Down>", scroll_down)

    right_frame = tk.Frame(window)
    right_frame.pack(side="right", padx=20, pady=20)

    tk.Label(right_frame, text="Tárolt hangok", font=("Helvetica", 14)).pack(pady=10)

    # Tárolt hangok menü
    sound_listbox = tk.Listbox(right_frame, height=10, font=("Helvetica", 14))
    sound_listbox.pack(side="right", fill="y", padx=10)
    sound_listbox.insert(tk.END, "Hang 1")
    sound_listbox.insert(tk.END, "Hang 2")
    sound_listbox.insert(tk.END, "Hang 3")

    ttk.Button(window, text="Kilépés", command=window.destroy, style="Custom.TButton").pack(padx=20)

# Indító képernyő megjelenítése
boot_screen()

# Főciklus
window.mainloop()
