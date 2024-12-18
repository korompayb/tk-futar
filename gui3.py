import time
import os
import pygame
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, Label, Frame
from threading import Timer



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


pygame.mixer.init()
os.system('cls' if os.name == 'nt' else 'clear')
print("ELINDULT A PROGRAM")


button_click_sound = relative_to_assets("bkkfutar_btnpress.wav")
error_sound = relative_to_assets("bkkfutar_longpiep.wav")



def play_button_click_sound():
    pygame.mixer.Sound(str(button_click_sound)).play()

def play_error_sound():
    pygame.mixer.Sound(str(error_sound)).play()

def handle_number_input(number):
    current_text = input_var.get()
    input_var.set(current_text + str(number))
    play_button_click_sound()  # Gombnyomás hang lejátszása

def clear_input():
    input_var.set("")
    play_button_click_sound()  # Gombnyomás hang lejátszása

def handle_number_input(number):
    current_text = input_var.get()
    input_var.set(current_text + str(number))

def clear_input():
    input_var.set("")

def submit_input():
    global current_step
    input_value = input_var.get()
    if current_step == "driver_id":
        if input_value in drivers:
            current_step = "vehicle_id"
            boot_message_label.config(text="Kérem adja meg a járműazonosítót!")

            input_var.set("")
            play_button_click_sound()
        else:
            boot_message_label.config(text="Hibás sofőrazonosító!", fg="red")
            play_error_sound()
            window.after(2000, lambda: boot_message_label.config(text="Kérem adja meg az azonosítóját!", fg="black"))

    elif current_step == "vehicle_id":
        if input_value in routes:
            boot_message_label.config(text="Járat megadva", fg="green")
            display_route(input_value)
            # Elrejtjük a gombokat és input boxot a járat helyes megadása után
            hide_input_elements()
            play_button_click_sound()
        else:
            boot_message_label.config(text="Hibás járműazonosító!", fg="red")
            window.after(2000, lambda: boot_message_label.config(text="Kérem adja meg a járműazonosítót!", fg="black"))
            play_error_sound()

def show_boot_screen():
    # Főkeret a teljes ablak lefedéséhez
    boot_frame = Frame(window, bg="#000000", width=689, height=416)
    boot_frame.place(x=0, y=0)  # A frame elhelyezése az ablak bal felső sarkába

    # Képernyő közepén megjelenő üzenet
    boot_message = Label(boot_frame, text="IVU", fg="#FFFFFF", bg="#000000", font=("Inter", 20))
    boot_message.place(relx=0.5, rely=0.5, anchor="center")  # Középre helyezzük a szöveget

    # 1 másodperc után eltüntetjük az üzenetet
    window.after(1000, lambda: boot_message.place_forget())

    # Hátteret képpel helyettesítjük, miután az üzenet eltűnt
    window.after(1000, lambda: show_boot_image(boot_frame))




def show_confirm_screen():
    def rectangle_clicked(event):
        play_button_click_sound()
        # A téglalap színének megváltoztatása
        canvas.itemconfig(rectangle_id, fill="#FFD700")
        boot_message.config(bg="#FFD700")
        # 1 másodperc múlva visszaállítjuk az eredeti színeket
        window.after(100, lambda: canvas.itemconfig(rectangle_id, fill="#E2E0FF"))
        window.after(100, lambda: boot_message.config(bg="#E2E0FF"))
        window.after(200, lambda: canvas.delete("all"))  # Erase canvas after click
        
        

    # Canvas létrehozása
    canvas = Canvas(window, bg="#FFFFFF", height=416, width=689, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Háttér téglalap
    canvas.create_rectangle(0.0, 0.0, 689.0, 388.0, fill="#9F9F9F", outline="")
    canvas.create_rectangle(0.0, 388.0, 689.0, 417.0, fill="#595959", outline="")

    # Szöveg (Label) létrehozása és középre helyezése, az input_var alapján
    boot_message = Label(canvas, text=input_var.get(), fg="#000000", bg="#E2E0FF", font=("Inter", 20))
    boot_message.place(relx=0.5, rely=0.5, anchor="center")

    # Kattintható téglalap
    rectangle_id = canvas.create_rectangle(5.0, 111.0, 680.0, 377.0, fill="#E2E0FF", outline="black")
    canvas.tag_bind(rectangle_id, "<Button-1>", rectangle_clicked)

    # További téglalapok
    canvas.create_rectangle(0.0, 392.0, 134.0, 413.0, fill="#CDCDCD", outline="")
    canvas.create_rectangle(142.0, 392.0, 515.0, 413.0, fill="#CDCDCD", outline="")
    canvas.create_rectangle(521.0, 392.0, 683.0, 413.0, fill="#CDCDCD", outline="")

def show_boot_image(boot_frame):
    # Hátteret képpel helyettesítjük
    boot_image = PhotoImage(file=relative_to_assets("boot.png"))  # Az elérési út a képedhez
    boot_background = Label(boot_frame, image=boot_image)
    boot_background.image = boot_image  # Ne veszítsük el a referenciát a képről
    boot_background.place(x=0, y=0, width=689, height=416)  # Kép kitöltése az ablak teljes területén

    # 3 másodperc után eltüntetjük a képet és folytatódik a bejelentkezési képernyő
    window.after(2000, lambda: boot_frame.destroy())  # Eltünteti a hátteret és a boot képernyőt
    window.after(2500, lambda: show_login_screen())  # A bejelentkezési képernyő következik


def show_login_screen():
    # Visszaállítjuk az ablakot a bejelentkezési képernyőre
    window.configure(bg="#FFFFFF")
    boot_message_label.config(text="Kérem adja meg az azonosítóját!")
    input_var.set("")  # Töröljük az esetleges korábbi adatokat
    # Itt következhet a további bejelentkezési folyamat

def hide_input_elements():
    # Elrejtjük az input elemeket (gombok és input box)
    input_label.place_forget()
    for button in number_buttons:
        button.place_forget()
    clear_button.place_forget()
    submit_button.place_forget()

def display_route(vehicle_id):
    route = routes.get(vehicle_id, [])
    if route:
        # Bal oldalon, lentől felfelé a járat megállók és érkezési idők
        y_position = 300
        for stop in route:
            
            stop_label = Label(window, text=f"{stop['stop']} - {stop['time']}", bg="#EAEAEA", fg="#000000", font=("Inter", 12))
            stop_label.place(x=20, y=y_position)
            y_position += 20

        # Jobb oldalon a "Hangok" szöveg
        sound_label = Label(window, text="Hangok", bg="#EAEAEA", fg="#000000", font=("Inter", 16))
        sound_label.place(x=500, y=300)
    else:
        route_display_label.place(x=20.0, y=140.0)
        route_display_label.config(text="Nincs elérhető járat az adott járműazonosítóhoz.")
    current_time = time.strftime("%H:%M:%S")
    driver_info_label.config(text=f"Sofőr: {drivers.get('1', 'járműmozgató')}\nJárat: {vehicle_id}\nIdő: {current_time}")



window = Tk()
window.title("IVU Szimuláció")
window.winfo_toplevel().wm_title("IVU Szimuláció")
icon = PhotoImage(file=relative_to_assets("logo.png"))  # A saját ikonod fájlja
window.iconphoto(True, icon)
window.geometry("689x416")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=416,
    width=689,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_rectangle(
    0.0,
    0.0,
    689.0,
    388.0,
    fill="#9F9F9F",
    outline=""
)

canvas.create_rectangle(
    0.0,
    388.0,
    689.0,
    417.0,
    fill="#595959",
    outline="")

boot_message_label = Label(
    window,
    text="boot",
    bg="#CDCDCD",
    fg="#000000",
    font=("Inter", 12)
)
boot_message_label.place(x=145.0, y=392.0)

input_var = StringVar()
input_label = Label(
    window,
    textvariable=input_var,
    bg="#CDCDCD",
    fg="#000000",
    font=("Inter", 26),
    width=20,
    anchor="w"
)
input_label.place(x=10.0, y=130.0)

button_images = {}
number_buttons = []

# Adjusted order of buttons for 1-9 followed by 0
button_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

for i in button_order:
    button_images[i] = PhotoImage(file=relative_to_assets(f"button_{i}.png"))
    number_buttons.append(Button(
        image=button_images[i],
        borderwidth=0,
        highlightthickness=0,
        command=lambda num=i: [handle_number_input(num), play_button_click_sound()],  # Pittyegés minden gombnyomásnál
        relief="flat"
    ))

# Place number buttons in a grid-like layout
x_start, y_start = 345, 111
button_width, button_height = 82, 52
spacing_x, spacing_y = 88, 60

for idx, button in enumerate(number_buttons):
    row, col = divmod(idx, 3)
    button.place(
        x=x_start + col * spacing_x,
        y=y_start + row * spacing_y,
        width=button_width,
        height=button_height
    )

clear_button_image = PhotoImage(file=relative_to_assets("button_clear.png"))
clear_button = Button(
    image=clear_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [clear_input(), play_button_click_sound()],  # Pittyegés a törlésnél is
    relief="flat"
)
clear_button.place(
    x=433.0,
    y=291.0,
    width=82.0,
    height=52.0
)

canvas.create_rectangle(
    0.0,
    111.0,
    345.0,
    387.0,
    fill="#CDCDCD",
    outline="")

canvas.create_rectangle(
    0.0,
    392.0,
    134.0,
    413.0,
    fill="#CDCDCD",
    outline="")

canvas.create_rectangle(
    142.0,
    392.0,
    515.0,
    413.0,
    fill="#CDCDCD",
    outline="")

canvas.create_rectangle(
    521.0,
    392.0,
    603.0,
    413.0,
    fill="#CDCDCD",
    outline="")

submit_button_image = PhotoImage(file=relative_to_assets("button_submit.png"))
submit_button = Button(
    image=submit_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [submit_input(), play_button_click_sound()],  # Pittyegés a submitnél is
    relief="flat"
)
submit_button.place(
    x=521.0,
    y=291.0,
    width=82.0,
    height=52.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_back.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_login_screen(),
    relief="flat"
)
button_12.place(
    x=606.0,
    y=391.0,
    width=81.0,
    height=23.0
)

route_display_label = Label(
    window,
    text="",
    bg="#9F9F9F",
    fg="#000000",
    font=("Inter", 16)
)
route_display_label.place_forget()


driver_info_label = Label(
    window,
    text="",
    bg="#9F9F9F",
    fg="#000000",
    font=("Inter", 16)
)
driver_info_label.place(x=500.0, y=60.0)

# Data setup
drivers = {"1": "járműmozgató", "5678": "ttk"}
routes = {
    "10500001": [
        {"stop": "Kossuth tér", "time": "08:00"},
        {"stop": "Deák tér", "time": "08:10"},
        {"stop": "Astoria", "time": "08:20"},
        {"stop": "Blaha Lujza tér", "time": "08:30"}
    ],
    "21300001": [
        {"stop": "Nyugati", "time": "09:00"},
        {"stop": "Oktogon", "time": "09:10"},
        {"stop": "Vörösmarty tér", "time": "09:20"},
        {"stop": "Erzsébet tér", "time": "09:30"}
    ],
    "30100001": [
        {"stop": "Keleti pályaudvar", "time": "10:00"},
        {"stop": "Blaha Lujza tér", "time": "10:10"},
        {"stop": "Astoria", "time": "10:20"},
        {"stop": "Deák tér", "time": "10:30"}
    ],
    "40200001": [
        {"stop": "Déli pályaudvar", "time": "11:00"},
        {"stop": "Móricz Zsigmond körtér", "time": "11:10"},
        {"stop": "Újbuda-központ", "time": "11:20"},
        {"stop": "Szent Gellért tér", "time": "11:30"}
    ],
    "50300001": [
        {"stop": "Hősök tere", "time": "12:00"},
        {"stop": "Andrássy út", "time": "12:10"},
        {"stop": "Oktogon", "time": "12:20"},
        {"stop": "Nyugati", "time": "12:30"}
    ]
}

current_step = "driver_id"

window.resizable(False, False)

show_boot_screen()
""" display_route('10500001') """
window.mainloop()
