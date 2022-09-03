# -------------------------------* Import statement *------------------------------- #

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
import random

# -------------------------------* test deck of cards *------------------------------- #

deck = ['♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K', '♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K', '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K', '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']

# ('aqua', 'step', 'clam', 'alt', 'default', 'classic')


# -------------------------------* Get all data from poker file *------------------------------- #
# TODO geting data from Poker file
def all_cards():
    global flop, players
    status = ['alive', 'fold']
    seat = ['BB', 'SB', '', '', '', '', '', '']

    def get_seat():
        s = random.choice(seat)
        seat.remove(s)
        return s

    flop = {"cards": [random.choice(deck), random.choice(deck), random.choice(deck), random.choice(deck),
                      random.choice(deck)],
            "frame": [],
            "label": [],
            "images": [],
            "pot": random.randint(25, 2000)
            }
    players = {
        "You": {
            "cards": [random.choice(deck), random.choice(deck)],
            "chips": random.randint(0, 500),
            "status": 'alive',
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": [],
        },
        "Player2": {
            "cards": [random.choice(deck), random.choice(deck)],
            "chips": 500,
            "status": random.choice(status),
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": [],
        },
        "Player3": {
            "cards": [random.choice(deck), random.choice(deck)],
            "chips": 500,
            "status": random.choice(status),
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": [],
        },
        "Player4": {
            "cards": [random.choice(deck), random.choice(deck)],
            "chips": 500,
            "status": "fold",
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": [],
        },
        "Player5": {
            "cards": ["♣3", "♣K"],
            "chips": 500,
            "status": "alive",
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": [],
        },
        "Player6": {
            "cards": ["♣3", "♣K"],
            "chips": 500,
            "status": "alive",
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": [],
        },
        "Player7": {
            "cards": [random.choice(deck), random.choice(deck)],
            "chips": random.randint(0, 500),
            "status": "alive",
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": []},
        "Player8": {
            "cards": [random.choice(deck), random.choice(deck)],
            "chips": random.randint(0, 500),
            "status": "alive",
            "seats": get_seat(),
            "frame": [],
            "label": [],
            "images": []}
    }


# -------------------------------* Resize Images *------------------------------- #
def resize_cards(card):
    card_img = Image.open(card)
    card_resize_image = card_img.resize((56, 82))
    card_image = ImageTk.PhotoImage(card_resize_image)

    return card_image


def resize_pic(pic):
    pic_img = Image.open(pic)
    pic_resize_image = pic_img.resize((120, 82))
    pic_image = ImageTk.PhotoImage(pic_resize_image)

    return pic_image


# -----------------------* Display Card/ Back of Card / Fold *----------------------- #
def get_flop_card(cards):
    global flop_image
    n = 0
    for c in cards:
        flop["images"].append(resize_cards(f'images/cards/{c}.png'))
        flop["label"][n].config(image=flop["images"][n])
        n += 1


def get_player_card(cards, k, round_end, status):
    global player_image
    n = 0
    if status == "fold":
        players[k]["label"][1].grid_forget()
        players[k]["images"].append(resize_pic(f'images/cards/fold.png'))
        players[k]["label"][0].config(image=players[k]["images"][0])
        players[k]["label"][0].grid(row=0, column=0, columnspan=2, padx=10)

    else:
        for c in cards:
            # display player1 card / other player will display at the end of each round
            if k == "You" or round_end:
                players[k]["images"].append(resize_cards(f'images/cards/{c}.png'))
                players[k]["label"][n].config(image=players[k]["images"][n])

            else:
                players[k]["images"].append(resize_cards(f'images/cards/back.png'))
                players[k]["label"][n].config(image=players[k]["images"][n])

            n += 1


# -----------------------* End round *----------------------- #
def end_round():
    show_card(True)


# -----------------------* User Input Command *----------------------- #
def fold():
    pass


def check():
    pass


def _raise():
    bid = int(slider.get())
    print(bid)


# -----------------------* Display Slider value *----------------------- #
def get_current_value():
    if var.get() == players["You"]["chips"]:
        value = "All-In!"
    else:
        value = round(var.get())
    return '{}'.format(value)


def slider_changed(event):
    value_label.configure(text=get_current_value())


# -----------------------* Display Board / Player *----------------------- #
def show_card(round_end=False):
    # get all data
    all_cards()

    # reset all widget to avoid bugs(sizing)
    for widget in canvas.winfo_children():
        widget.destroy()

    flop["frame"].append(LabelFrame(canvas, bg="#1e7849", borderwidth=0))
    flop["frame"][0].place(x=360, y=240)
    no_of_loop = 0

    for _ in flop["cards"]:
        flop["label"].append(Label(flop["frame"][0], bg="#1e7849"))
        flop["label"][no_of_loop].grid(row=0, column=no_of_loop)
        no_of_loop += 1

    get_flop_card(flop["cards"])

    flop["frame"].append(LabelFrame(canvas, bg="#0F3C25", borderwidth=0, width=180, height=30))
    flop["frame"][1].place(x=425, y=335)
    flop["frame"][1].pack_propagate(False)

    flop["label"].append(Label(flop["frame"][1], text=f"Pot: {flop['pot']} Chips", bg="#0F3C25", fg='#3B7A5A',
                               font=('', 20, '')))
    flop["label"][no_of_loop].pack()

    for k, p in players.items():
        p["frame"].append(LabelFrame(canvas, text=k, borderwidth=0, bg='black', fg='#a6a6a6'))

        # asign x and y for each player
        if k == "You":
            p["frame"][0].place(x=640, y=450)

        elif k == "Player2":
            p["frame"][0].place(x=820, y=240)

        elif k == "Player3":
            p["frame"][0].place(x=640, y=0)

        elif k == "Player4":
            p["frame"][0].place(x=440, y=0)

        elif k == "Player5":
            p["frame"][0].place(x=240, y=0)

        elif k == "Player6":
            p["frame"][0].place(x=60, y=240)

        elif k == "Player7":
            p["frame"][0].place(x=240, y=450)

        elif k == "Player8":
            p["frame"][0].place(x=440, y=450)

        # first card
        p["label"].append(Label(p["frame"][0], borderwidth=0, bg='black'))
        p["label"][0].grid(row=0, column=0, sticky="W")

        # second card
        p["label"].append(Label(p["frame"][0], borderwidth=0, bg='black'))
        p["label"][1].grid(row=0, column=1, padx=5, sticky="E")

        # display chips left
        p["label"].append(Label(p["frame"][0], text=f"Chips: {p['chips']}", bg='black', fg='#a6a6a6'))
        p["label"][2].grid(row=1, column=0, sticky="W", columnspan=2)

        if p["seats"] == "BB" or p["seats"] == "SB":
            p["label"].append(Label(p["frame"][0], text=p["seats"], bg='black', fg='#a6a6a6'))
            p["label"][3].grid(row=1, column=1, sticky="E")

        get_player_card(p["cards"], k, round_end, p["status"])

    # to change scale value every turn
    global slider

    slider = Label(canvas)
    slider.destroy()

    slider = ttk.Scale(
        my_frame,
        from_=highest_bid + 1,
        to=players["You"]["chips"],
        orient='horizontal',
        command=slider_changed,
        variable=var,
    )

    slider.focus()
    slider.grid(row=0, column=0, padx=5)


# -------------------------------* TK inter setup *------------------------------- #

root = ThemedTk(theme='black')
root.title("Poker")
root.configure(background="black")

# Int value for slider
var = IntVar()

# TODO get real highest bid
highest_bid = 20

# -------------------------------* Poker table *------------------------------- #
canvas = Canvas(width=1024, height=576, bg="black", highlightthickness=0)
bg = PhotoImage(file="images/logo/bg.png")
canvas.create_image(0, 0, image=bg, anchor=NW)
canvas.pack(pady=20, padx=20)
canvas.grid_propagate(False)

# -------------------------------* User Input *------------------------------- #
my_frame = Frame(root, bg="black")
my_frame.pack(pady=20, padx=20)

call_button = ttk.Button(my_frame, text="Call", command=end_round)

call_button.grid(row=0, column=3, pady=5)

fold_button = ttk.Button(my_frame, text="Fold", command=fold)
fold_button.grid(row=0, column=4, padx=10, pady=5)

raise_button = ttk.Button(my_frame, text="Raise", command=_raise)
raise_button.grid(row=0, column=2, padx=10, pady=5)

show_card()
value_label = ttk.Label(my_frame, text=get_current_value())
value_label.grid(row=0, column=1)


root.mainloop()
