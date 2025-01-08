import time
import json
import os
from datetime import datetime
import pygame
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, Label, Frame
from threading import Timer




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


"""-------------------------------------------------------------------------------------- Funkciók és függvények -----------------------------------------------------------------------------------------"""

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
    
def handle_driver_id(input_value):
    """Kezeli a sofőrazonosító megadását."""
    if input_value in drivers:
        boot_message_label.config(text="Kérem adja meg a járműazonosítót!", fg="black")
        input_var.set("")
        play_button_click_sound()
        show_confirm_screen(input_value)
        return "confirm_driver_id"
    else:
        boot_message_label.config(text="Hibás sofőrazonosító!", fg="red")
        play_error_sound()
        input_var.set("")  # Clear invalid input
        window.after(2000, lambda: boot_message_label.config(text="Kérem adja meg az azonosítóját!", fg="black"))
        return "driver_id"

def handle_vehicle_id(input_value):
    """Kezeli a járműazonosító megadását."""
    if input_value in routes:
        boot_message_label.config(text="Járat megadva", fg="green")
        display_route(input_value)
        show_operation_buttons()
        hide_input_elements()  
        play_button_click_sound()
        return "completed"
    else:
        boot_message_label.config(text="Hibás járműazonosító!", fg="red")
        play_error_sound()
        input_var.set("")  # Clear invalid input
        window.after(2000, lambda: boot_message_label.config(text="Kérem adja meg a járműazonosítót!", fg="black"))
        return "vehicle_id"

def submit_input():
    """Fő input kezelő, amely a lépésekhez irányít."""
    global current_step
    input_value = input_var.get()
    
    if not input_value:  # Skip if input is empty
        return
        
    if current_step == "driver_id":
        current_step = handle_driver_id(input_value)
    elif current_step == "vehicle_id":
        current_step = handle_vehicle_id(input_value)
    elif current_step == "confirm_driver_id":
        if input_value in routes:  # Only proceed if valid vehicle ID
            display_route(input_value)
            show_operation_buttons()
            hide_input_elements()
            current_step = "completed"
        else:
            boot_message_label.config(text="Hibás járműazonosító!", fg="red")
            play_error_sound()
            input_var.set("")
            window.after(2000, lambda: boot_message_label.config(text="Kérem adja meg a járműazonosítót!", fg="black"))
            current_step = "vehicle_id"

def show_confirm_screen(input_value):
    """Megjeleníti a megerősítő képernyőt a sofőrazonosítóval."""
    # Háttér téglalap
    confirm_frame = Frame(window, bg="#9F9F9F", width=689, height=416)
    confirm_frame.place(x=0, y=0)

    # Canvas létrehozása a téglalapoknak
    canvas_confirm = Canvas(confirm_frame, width=689, height=416, bg="#9F9F9F", highlightthickness=0)
    canvas_confirm.place(x=0, y=0)

    canvas_confirm.create_rectangle(
        0.0,
        392.0,
        134.0,
        413.0,
        fill="#CDCDCD",
        outline=""
    )

    canvas_confirm.create_rectangle(
        142.0,
        392.0,
        515.0,
        413.0,
        fill="#CDCDCD",
        outline=""
    )

    canvas_confirm.create_rectangle(
        521.0,
        392.0,
        603.0,
        413.0,
        fill="#CDCDCD",
        outline=""
    )

    # Kattintható téglalap
    rectangle_id = Canvas(confirm_frame, width=680, height=266, bg="#E2E0FF", highlightthickness=0)
    rectangle_id.place(x=5, y=111)
    rectangle_id.bind("<Button-1>", lambda e: proceed_to_vehicle_id(confirm_frame))

    display_name = "járműmozgató" if input_value == "1" else input_value

    # Szöveg (Label) létrehozása és középre helyezése
    confirm_message = Label(confirm_frame, text=f"{display_name}", fg="#000000", bg="#E2E0FF", font=("Inter", 20))
    confirm_message.place(relx=0.5, rely=0.5, anchor="center")

def proceed_to_vehicle_id(confirm_frame):
    """Továbbhalad a járműazonosító megadására."""
    global current_step
    play_button_click_sound()
    confirm_frame.destroy()
    boot_message_label.config(text="Kérem adja meg a járműazonosítót!", fg="black")
    input_var.set("")
    current_step = "vehicle_id"



def display_route(vehicle_id):
    route = routes.get(vehicle_id, [])
    if route:
        # Update the route number, name, and short number on the canvas
        canvas.itemconfig(route_number_text, text=f"{vehicle_id}/")
        canvas.itemconfig(route_name_text, text=f"{route[-1]['stop']}")
        canvas.itemconfig(route_short_number_text, text=vehicle_id[:3])

        # Initialize the start index for displaying stops
        display_route.start_index = 0

        def update_stops():
            # Clear previous stop labels
            for label in display_route.stop_labels:
                label.place_forget()

            # Display up to 5 stops starting from the current index
            y_position = 200
            for i in range(display_route.start_index, min(display_route.start_index + 5, len(route))):
                stop = route[i]
                stop_label = Label(window, text=f"{stop['stop']} - {stop['time']}", bg="#EAEAEA", fg="#000000", font=("Inter", 12))
                stop_label.place(x=60, y=y_position)
                display_route.stop_labels.append(stop_label)
                y_position += 40

        def scroll_up():
            if display_route.start_index > 0:
                display_route.start_index -= 1
                update_stops()

        def scroll_down():
            if display_route.start_index + 5 < len(route):
                display_route.start_index += 1
                update_stops()

        # Store stop labels for easy clearing
        display_route.stop_labels = []

        # Bind scroll buttons to their functions
        button_15.config(command=lambda: [scroll_up(), play_button_click_sound()])
        button_16.config(command=lambda: [scroll_down(), play_button_click_sound()])

        # Initial update of stops
        update_stops()

        

        # Show images
        canvas.itemconfig(image_1, state='normal')
        canvas.itemconfig(image_2, state='normal')
    else:
        canvas.itemconfig(route_number_text, text="0")
        canvas.itemconfig(route_name_text, text="NEM SZALLIT UTASOKAT")
        canvas.itemconfig(route_short_number_text, text="")

        # Hide images
        canvas.itemconfig(image_1, state='hidden')
        canvas.itemconfig(image_2, state='hidden')



def show_boot_screen():
    # Főkeret a teljes ablak lefedéséhez
    boot_frame = Frame(window, bg="#000000", width=689, height=416)
    boot_frame.place(x=0, y=0)  # A frame elhelyezése az ablak bal felső sarkába

    # Képernyő közepén megjelenő üzenet
    boot_message = Label(boot_frame, text="IVU", fg="#FFFFFF", bg="#000000", font=("Inter", 20))
    boot_message.place(relx=0.5, rely=0.5, anchor="center")  # Középre helyezzük a szöveget

    # 1 másodperc után eltüntetjük az üzenetet
    window.after(500, lambda: boot_message.place_forget())

    # Hátteret képpel helyettesítjük, miután az üzenet eltűnt
    window.after(500, lambda: show_boot_image(boot_frame))

def show_boot_image(boot_frame):
    # Hátteret képpel helyettesítjük
    boot_image = PhotoImage(file=relative_to_assets("boot.png"))  # Az elérési út a képedhez
    boot_background = Label(boot_frame, image=boot_image)
    boot_background.image = boot_image  # Ne veszítsük el a referenciát a képről
    boot_background.place(x=0, y=0, width=689, height=416)  # Kép kitöltése az ablak teljes területén

    # 3 másodperc után eltüntetjük a képet és folytatódik a bejelentkezési képernyő
    window.after(500, lambda: boot_frame.destroy())  # Eltünteti a hátteret és a boot képernyőt
    window.after(500, lambda: show_login_screen())  # A bejelentkezési képernyő következik


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
        
    submit_button.place_forget()









""" ------------------------------------------------------------------------------------------ Vászon és ablak beállítása --------------------------------------------------------------------------------------- """

window = Tk()
window.title("IVU Szimuláció")
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

current_time_var = StringVar()
current_date_var = StringVar()

def update_current_time():
    current_time = time.strftime("%H:%M:%S")  # Óra:Perc:Másodperc
    current_time_var.set(current_time)
    canvas.itemconfig(time_label, text=current_time_var.get())  # Frissíti a vásznon lévő szöveget
    canvas.after(1000, update_current_time)  # Frissítés másodpercenként


def update_current_date():
    # Get the current date and format it
    current_date = time.strftime("%Y_%m_%d")  # Get date in YYYY_MM_DD format
    # Get the current weekday in Hungarian
    weekday_hungarian = time.strftime("%a")  # Get abbreviated weekday name
    hungarian_weekdays = {
        "Mon": "Hé",
        "Tue": "Ke",
        "Wed": "Sz",
        "Thu": "Cs",
        "Fri": "Pé",
        "Sat": "Szo",
        "Sun": "Vas"
    }
    # Replace the English weekday with Hungarian
    weekday_hungarian = hungarian_weekdays.get(weekday_hungarian, weekday_hungarian)
    formatted_date = f"{weekday_hungarian} {current_date}"  # Format the date
    current_date_var.set(formatted_date)
    canvas.itemconfig(date_text_id, text=current_date_var.get())  # Update the date on the canvas
    canvas.after(86400000, update_current_date)  # Update every 24 hours



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

route_number_text = canvas.create_text(
    2.0,
    5.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Inter", 20 * -1)
)

route_name_text = canvas.create_text(
    0.0,
    27.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Inter", 20 * -1)
)

route_short_number_text = canvas.create_text(
    122.0,
    5.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Inter", 20 * -1)
)

time_label = canvas.create_text(
    517.0,
    2.0,
    anchor="nw",
    text=current_time_var.get(),  # Initialize with the current time
    fill="#000000",
    font=("Inter", 22 * -1)
)

date_text_id = canvas.create_text(
    517.0,
    26.0,
    anchor="nw",
    text="Pé 2022_02_11",
    fill="#000000",
    font=("Inter Bold", 16 * -1)
)

canvas.create_text(
    188.0,
    5.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Inter", 20 * -1)
)


boot_message_label = Label(
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
    width=10,
    anchor="w"
)
input_label.place(x=10.0, y=130.0)

button_images = {}
number_buttons = []
# Adjusted order of buttons for 1-9 followed by clear, 0, and submit
button_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'clear', 0, 'submit']

for i in button_order:
    if i == 'clear':
        button_images[i] = PhotoImage(file=relative_to_assets("button_clear.png"))
        number_buttons.append(Button(
            image=button_images[i],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [clear_input(), play_button_click_sound()],
            relief="flat"
        ))
    elif i == 'submit':
        button_images[i] = PhotoImage(file=relative_to_assets("button_submit.png"))
        number_buttons.append(Button(
            image=button_images[i],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [submit_input(), play_button_click_sound()],
            relief="flat"
        ))
    else:
        button_images[i] = PhotoImage(file=relative_to_assets(f"button_{i}.png"))
        number_buttons.append(Button(
            image=button_images[i],
            borderwidth=0,
            highlightthickness=0,
            command=lambda num=i: [handle_number_input(num), play_button_click_sound()],
            relief="flat"
        ))


for button in number_buttons:
    button.place_forget()

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




button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: print("button_15 clicked"), relief="flat")
button_15.place(x=306.0, y=113.0, width=34.0, height=30.741180419921875)

button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: print("button_16 clicked"), relief="flat")
button_16.place(x=306.0, y=353.0, width=34.0, height=30.741180419921875)

button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: print("button_17 clicked"), relief="flat")
button_17.place(x=654.0, y=112.0, width=34.0, height=30.741180419921875)

button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: print("button_18 clicked"), relief="flat")
button_18.place(x=654.0, y=352.0, width=34.0, height=30.741180419921875)

button_image_task = PhotoImage(file=relative_to_assets("button_task.png"))
button_task = Button(image=button_image_task, borderwidth=0, highlightthickness=0, command=lambda: print("Tevekenyseg clicked"), relief="flat")
button_task.place(x=2.0, y=51.0, width=134.0, height=54.78265380859375)

button_image_send_messages = PhotoImage(file=relative_to_assets("button_sendmessages.png"))
button_send_messages = Button(image=button_image_send_messages, borderwidth=0, highlightthickness=0, command=lambda: print("Uzenet kuldes clicked"), relief="flat")
button_send_messages.place(x=140.0, y=51.0, width=134.0, height=54.78265380859375)

button_image_sounds = PhotoImage(file=relative_to_assets("button_22.png"))
button_sounds = Button(image=button_image_sounds, borderwidth=0, highlightthickness=0, command=lambda: print("Tárolt hangok clicked"), relief="flat")
button_sounds.place(x=278.0, y=51.0, width=134.0, height=54.78265380859375)

button_image_settings = PhotoImage(file=relative_to_assets("button_settings.png"))
button_settings = Button(image=button_image_settings, borderwidth=0, highlightthickness=0, command=lambda: print("Beallitasok clicked"), relief="flat")
button_settings.place(x=416.0, y=51.0, width=134.0, height=54.78265380859375)

button_image_messages = PhotoImage(file=relative_to_assets("button_messages.png"))
button_messages = Button(image=button_image_messages, borderwidth=0, highlightthickness=0, command=lambda: print("Uzenetek clicked"), relief="flat")
button_messages.place(x=554.0, y=51.0, width=134.0, height=54.78265380859375)

button_image_menetrend = PhotoImage( file=relative_to_assets("button_menetrend.png")) 
button_menetrend = Button( image=button_image_menetrend, borderwidth=0, highlightthickness=0, command=lambda: print("A mentrend betartása érdekében várakozunk"), relief="flat" ) 
button_menetrend.place( x=355.0, y=114.0, width=293.33349609375, height=55.0 ) 

button_image_maszk = PhotoImage( file=relative_to_assets("button_maszk.png")) 
button_maszk = Button( image=button_image_maszk, borderwidth=0, highlightthickness=0, command=lambda: print("A Korona virus miatt maszk viselése kötelező"), relief="flat" ) 
button_maszk.place( x=355.0, y=175.0, width=293.33349609375, height=55.0 ) 

button_image_ajto = PhotoImage( file=relative_to_assets("button_ajto_var.png")) 
button_ajto = Button( image=button_image_ajto, borderwidth=0, highlightthickness=0, command=lambda: print("Ajto zarva, allunk varunk"), relief="flat" ) 
button_ajto.place( x=355.0, y=236.0, width=293.33349609375, height=55.0 ) 

button_image_beallas = PhotoImage( file=relative_to_assets("button_nem_tud_beallni.png")) 
button_beallas = Button( image=button_image_beallas, borderwidth=0, highlightthickness=0, command=lambda: print("A jarmu nem tud beallni, ovatosan a felszallassal"), relief="flat" ) 
button_beallas.place( x=354.0, y=297.0, width=293.33349609375, height=55.0 )


# Gombokat tartalmazó lista
operation_buttons = [
    (button_15, 306.0, 113.0),
    (button_16, 306.0, 353.0),
    (button_17, 654.0, 112.0),
    (button_18, 654.0, 352.0),
    (button_task, 2.0, 51.0),
    (button_send_messages, 140.0, 51.0),
    (button_sounds, 278.0, 51.0),
    (button_settings, 416.0, 51.0),
    (button_messages, 554.0, 51.0),
    (button_menetrend, 355.0, 114.0),
    (button_maszk, 355.0, 175.0),
    (button_ajto, 355.0, 236.0),
    (button_beallas, 354.0, 297.0),

]
    

# Függvény, hogy megjelenítsd az összes gombot
def show_operation_buttons():


    for button, x, y in operation_buttons:
        button.place(x=x, y=y)

# Függvény, hogy elrejtsd az összes gombot
def hide_operation_buttons():

    for button, _, _ in operation_buttons:
        button.place_forget()


image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(323.0,252.0,image=image_image_1)
canvas.itemconfig(image_1, state='hidden')

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(46.61248779296875, 248.0, image=image_image_2)
canvas.itemconfig(image_2, state='hidden')


canvas.create_rectangle(
    293.0,
    5.0,
    393.0,
    29.0,
    fill="#2C9943",
    outline="")


""" ----------------------------------------------------------------------------------------------------- Adatok, JSON --------------------------------------------------------------------------------------------- """

# Data setup
drivers = {"1": "járműmozgató", "5678": "ttk"}
path = 'forgalmi.json'

with open(path, 'r') as file:
    routes = json.load(file)


current_step = "driver_id"

window.resizable(False, False)

show_boot_screen()

update_current_time()
update_current_date()
hide_operation_buttons()
""" display_route('23700001') """

window.mainloop()
