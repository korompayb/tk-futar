
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/korompaybertalan/Documents/tkinter/figmatk/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("689x416")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 416,
    width = 689,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    689.0,
    416.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    689.0,
    388.0,
    fill="#9F9F9F",
    outline="")

canvas.create_rectangle(
    0.0,
    388.0,
    689.0,
    417.0,
    fill="#595959",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=345.0,
    y=111.0,
    width=82.0,
    height=52.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=433.0,
    y=111.0,
    width=82.0,
    height=52.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=521.0,
    y=111.0,
    width=82.0,
    height=52.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=345.0,
    y=167.0,
    width=82.0,
    height=52.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=433.0,
    y=167.0,
    width=82.0,
    height=52.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=521.0,
    y=167.0,
    width=82.0,
    height=52.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=345.0,
    y=223.0,
    width=82.0,
    height=52.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=433.0,
    y=223.0,
    width=82.0,
    height=52.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(
    x=521.0,
    y=223.0,
    width=82.0,
    height=52.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=345.0,
    y=279.0,
    width=82.0,
    height=52.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_submit.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_11 clicked"),
    relief="flat"
)
button_11.place(
    x=521.0,
    y=279.0,
    width=82.0,
    height=52.0
)



button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_13 clicked"),
    relief="flat"
)
button_13.place(
    x=433.0,
    y=279.0,
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

canvas.create_text(
    0.0,
    113.0,
    anchor="nw",
    text="Kérem adja meg az azonosítóját!",
    fill="#000000",
    font=("Inter", 20 * -1)
)
window.resizable(False, False)
window.mainloop()
