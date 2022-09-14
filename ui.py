# -------------------------------* Import statement *------------------------------- #
import tkinter.messagebox

import Poker
import Poker_Draft
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
import time
import pandas as pd


# -------------------------------* Get data from poker file *------------------------------- #
def data_convert(d):
    global flop, players

    flop = d['board']
    flop["frame"] = []
    flop["label"] = []
    flop["images"] = []
    del d['board']

    players = {}
    for key, value in d.items():
        players[key] = d[key]
        players[key]["frame"] = []
        players[key]["label"] = []
        players[key]["images"] = []

    return flop, players


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
def get_flop_card(cards, stage):
    global flop_image
    n = 0
    # -----------------------* Show card *----------------------- #
    for c in cards:
        flop["images"].append(resize_cards(f'images/cards/{c}.png'))
        flop["label"][n].config(image=flop["images"][n])
        n += 1

    # -----------------------* Check Round end / Show winner *----------------------- #

    global reward

    if stage == 'begin':
        winner = flop['winner']
        print(winner)
        try:
            win_con = players[winner]['type']

        except KeyError:
            win_con = "All fold"
            for i in players:
                if players[i]["fold"] == False:
                    winner = i

        # -----------------------* Display Winner label *----------------------- #
        flop["frame"][2].config(width=180, height=50, bg="#a00405", bd=2)
        flop["frame"][2].place(x=425, y=180)
        flop["label"][n + 1].config(text=f"Winner: {winner}\n{win_con}",
                                    bg="#a00405", anchor="center", justify=CENTER,
                                    font=("Impact", 18, ""), fg="#fff166")

        flop["label"][n].config(text=f"Pot: {reward} Chips", fg="#F6E382", font=("Impact", 20, ""))
        reward = 0


def get_player_card(cards, k, stage, fold):
    global Round
    time.sleep(0.1)
    global player_image
    n = 0
    if fold:
        players[k]["label"][1].grid_forget()
        players[k]["images"].append(resize_pic(f'images/cards/fold.png'))
        players[k]["label"][0].config(image=players[k]["images"][0])
        players[k]["label"][0].grid(row=0, column=0, columnspan=2, padx=10)
        players[k]["label"][0].update()

    elif len(cards) == 0:
        players[k]["images"].append(resize_pic(f'images/cards/none.png'))
        players[k]["label"][0].config(image=players[k]["images"][0])
        players[k]["label"][0].grid(row=0, column=0, columnspan=2, padx=10)
        players[k]["label"][0].update()

    else:
        for c in cards:
            # display player1 card / other player will display at the end of each round
            if k == "You" or stage == 'begin':
                players[k]["images"].append(resize_cards(f'images/cards/{c}.png'))
                players[k]["label"][n].config(image=players[k]["images"][n])
                players[k]["label"][n].update()


            else:
                players[k]["images"].append(resize_cards(f'images/cards/back.png'))
                players[k]["label"][n].config(image=players[k]["images"][n])
                players[k]["label"][n].update()
            n += 1


# -----------------------* User Input Command *----------------------- #
def _continue():
    if players["You"]["fold"] or len(players["You"]["cards"]) == 0 or flop['stage'] == 'begin':
        global loop_pause
        loop_pause = False
    else:
        tkinter.messagebox.showinfo(message="Please choose your action")


def fold():
    if not players["You"]["fold"] and len(players["You"]["cards"]) > 0 and flop['stage'] != 'begin':
        global loop_pause
        loop_pause = False
        you.fold = True
    else:
        tkinter.messagebox.showinfo(message="You're already fold")


def call():
    if not players["You"]["fold"] and len(players["You"]["cards"]) > 0 and flop['stage'] != 'begin':
        global loop_pause
        loop_pause = False
        highbet = flop["highest_bid"]
        bid = highbet - players["You"]["need"]
        you.call(highbet=highbet)
    else:
        tkinter.messagebox.showinfo(message="You're already fold")


def _raise():
    bid = int(slider.get())
    if not players["You"]["fold"] and len(players["You"]["cards"]) > 0 and flop['stage'] != 'begin':
        global loop_pause
        loop_pause = False
        you.rise(bet=bid)
    else:
        tkinter.messagebox.showinfo(message="You're already fold")


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
def show_card(d):
    # get all data
    data_convert(d)

    # reset all widget to avoid bugs(sizing)
    for widget in canvas.winfo_children():
        widget.destroy()

    global reward
    if flop['pot'] >= reward:
        reward = flop['pot']
    # -----------------------* Table card frame *----------------------- #
    flop["frame"].append(LabelFrame(canvas, bg="#1e7849", borderwidth=0))
    flop["frame"][0].place(x=360, y=240)
    no_of_loop = 0

    # -----------------------* Create each card Label *----------------------- #
    for _ in flop["cards"]:
        flop["label"].append(Label(flop["frame"][0], bg="#1e7849"))
        flop["label"][no_of_loop].grid(row=0, column=no_of_loop)
        no_of_loop += 1

    # -----------------------* Create Pot *----------------------- #
    flop["frame"].append(LabelFrame(canvas, bg="#0F3C25", borderwidth=0, width=180, height=30))
    flop["frame"][1].place(x=425, y=335)
    flop["frame"][1].pack_propagate(False)
    flop["label"].append(Label(flop["frame"][1], text=f"Pot: {reward} Chips", bg="#0F3C25", fg='#3B7A5A',
                               font=('', 20, '')))
    flop["label"][no_of_loop].pack()

    # -----------------------* highest bid *----------------------- #
    flop["frame"].append(LabelFrame(canvas, bg="#0F3C25", borderwidth=0, width=180, height=25))
    flop["frame"][2].place(x=425, y=205)
    flop["frame"][2].pack_propagate(False)
    flop["label"].append(
        Label(flop["frame"][2], text=f"Highest Bid: {flop['highest_bid']} Chips", bg="#0F3C25", fg='#3B7A5A',
              font=('', 15, '')))
    flop["label"][no_of_loop + 1].pack(padx=4, pady=4)

    # -----------------------* Display all table *----------------------- #
    get_flop_card(flop["cards"], flop["stage"])

    # -----------------------* Create Players *----------------------- #
    for k, p in players.items():

        # player frame
        p["frame"].append(LabelFrame(canvas, text=k, borderwidth=0, bg='black', fg='white'))

        # assign x and y for each player
        if k == "You":
            p["frame"][0].place(x=440, y=450)

        elif k == "F1":
            p["frame"][0].place(x=640, y=450)

        elif k == "F2":
            p["frame"][0].place(x=820, y=240)

        elif k == "F3":
            p["frame"][0].place(x=640, y=0)

        elif k == "F4":
            p["frame"][0].place(x=440, y=0)

        elif k == "F5":
            p["frame"][0].place(x=240, y=0)

        elif k == "F6":
            p["frame"][0].place(x=60, y=240)

        elif k == "F7":
            p["frame"][0].place(x=240, y=450)

        # first card
        p["label"].append(Label(p["frame"][0], borderwidth=0, bg='black'))
        p["label"][0].grid(row=0, column=0, sticky="W")

        # second card
        p["label"].append(Label(p["frame"][0], borderwidth=0, bg='black'))
        p["label"][1].grid(row=0, column=1, padx=5, sticky="E")

        # display chips left
        p["label"].append(
            Label(p["frame"][0], text=f"Chips: {p['chips']}\n total bet: {p['bet']}", bg='black', fg='white'))
        p["label"][2].grid(row=1, column=0, sticky="W", columnspan=2)

        if p["seats"] == "BB" or p["seats"] == "SB":
            p["label"].append(Label(p["frame"][0], text=p["seats"], bg='black', fg='white'))
            p["label"][3].grid(row=1, column=1, sticky="NE")

        get_player_card(p["cards"], k, flop['stage'], p["fold"])

    # to change scale value every turn
    global slider

    slider = Label(canvas)
    slider.destroy()

    slider = ttk.Scale(
        my_frame,
        from_=flop["highest_bid"] + 1,
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

# -------------------------------* Poker table *------------------------------- #
canvas = Canvas(root, width=1024, height=586, bg="black", highlightthickness=0)
bg = PhotoImage(file="images/logo/bg.png")
canvas.create_image(0, 0, image=bg, anchor=NW)
canvas.pack(pady=20, padx=20)
canvas.grid_propagate(False)

my_frame = Frame(root, bg="black")
my_frame.pack(pady=20, padx=20)

# -------------------------------* User selected number of player *------------------------------- #
game_start = False

global num_player, reward
reward = 0

while not game_start:
    num_player = int(input("How many players you want? (2-8 players) "))
    if 2 <= num_player <= 8:
        game_start = True
    else:
        print("Please input number between 2 to 8")

# -------------------------------* Game Loop *------------------------------- #
poker = Poker_Draft.Dealer(num_player)
Round = 0

Round = 0
Index = []
C_L = []
j = 0
for i in poker.players:
    j += 1
    C_L.append('name_' + str(j))
    C_L.append('seat_' + str(j))
    C_L.append('fold_' + str(j))
    C_L.append('all_in_' + str(j))
    C_L.append('chips_' + str(j))
    C_L.append('bet_' + str(j))
    C_L.append('hands_' + str(j))
    C_L.append('type_' + str(j))
    C_L.append('score_' + str(j))
A = [[], [], [], []]
for i in poker.players:
    for k in range(9):
        A.append([])

while poker.players[0].alive and len(poker.players) > 1:
    if poker.stage == 'begin':
        Round += 1
        poker.begin()
    elif poker.stage == 'preflop':
        poker.preflop()
    elif poker.stage == 'flop':
        poker.flop()
    elif poker.stage == 'turn':
        poker.turn()
    elif poker.stage == 'river':
        poker.river()

    Index.append(Round)
    A[0].append(poker.stage)
    A[1].append(poker.pod)
    A[2].append(poker.highbet)
    A[3].append(poker.board)

    for i in range(len(poker.players)):
        A[i * 9 + 4].append(poker.players[i].name)
        A[i * 9 + 5].append(poker.players[i].seat)
        A[i * 9 + 6].append(poker.players[i].fold)
        A[i * 9 + 7].append(poker.players[i].allin)
        A[i * 9 + 8].append(poker.players[i].chips)
        A[i * 9 + 9].append(poker.players[i].bet)
        A[i * 9 + 10].append(poker.players[i].hands)
        A[i * 9 + 11].append(poker.players[i].type)
        A[i * 9 + 12].append(poker.players[i].score)

    poker.get()

    data = {"board": {'cards': poker.board, 'highest_bid': poker.highbet, 'pot': poker.pod, 'stage': poker.stage,
                      'winner': poker.winner}}

    for i in poker.players:
        data[i.name] = {"seats": i.seat, 'fold': i.fold, 'chips': i.chips, "cards": i.hands,
                        "type": i.type, "score": i.score, "bet": i.bet, "need": i.need}
    poker.data = data
    show_card(data)
    you = poker.players[0]

    # -------------------------------* User Input *------------------------------- #

    call_button = ttk.Button(my_frame, text="Call", command=call)
    call_button.grid(row=0, column=3, pady=5)

    fold_button = ttk.Button(my_frame, text="Fold", command=fold)
    fold_button.grid(row=0, column=4, padx=10, pady=5)

    raise_button = ttk.Button(my_frame, text="Raise", command=_raise)
    raise_button.grid(row=0, column=2, padx=10, pady=5)

    value_label = ttk.Label(my_frame, text=get_current_value())
    value_label.grid(row=0, column=1)

    continue_button = ttk.Button(my_frame, text="Continue", command=_continue)
    continue_button.grid(row=0, column=5, padx=10, pady=5)
    # -------------------------------* Pause the loop until user click a button *------------------------------- #
    # I have comment line 91-92 for faster test
    # change to True for loop pause
    loop_pause = True

    while loop_pause:
        root.update()
        value_label.update()

for i in A:
    while len(i) < len(A[0]):
        i.append('')

R = pd.DataFrame({'next_stage': A[0]
                     , 'pod': A[1]
                     , 'high_bet': A[2]
                     , 'board': A[3]
                  })
for i in range(len(C_L)):
    R[C_L[i]] = A[i + 4]
R.index = Index
R.to_csv('Record.csv', encoding="utf_8_sig")

root.destroy()
poker.end()
root.mainloop()
