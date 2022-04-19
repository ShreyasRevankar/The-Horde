from src.village import *
from src.input import *
from replays.make_replay import *
import json
import os
import numpy as np
import time

os.system("clear")
with open("src/utils/menu.txt", "r") as f:
    print(f.read())
input()

with open("src/utils/barb_king.txt", "r") as f:
    king_img = f.readlines()
with open("src/utils/arch_queen.txt", "r") as f:
    queen_img = f.readlines()

spacing = ""
for i in range(20):
    spacing += " "


os.system("clear")
for i in range(len(king_img)):
    king_img[i] = king_img[i].replace("\n", "")
    print(king_img[i], end="")
    print(spacing, end="")
    print(queen_img[i], end="")

royal = ""
while royal != "k" and royal != "q":
    royal = input("Enter k to play with king and q to play with queen: ")


my_village = village()
my_village.init_village(1, royal)

os.system("stty -echo")

replay_input = [royal]

while True:
    # try:
    os.system("clear")
    if my_village.is_game_over():
        make_replay(replay_input)
        os.system("stty echo")
        break
    my_village.display_village()
    ts = my_village.get_time_step()
    start = time.time()
    ch = input_to(Get(), ts)
    end = time.time()
    replay_input.append(ch)
    if ch == "q":
        os.system("stty echo")
        break
    elif ch and ord("1") <= ord(ch) <= ord("9"):
        my_village.spawn_troop(int(ch) - 1)
    elif ch == "w" or ch == "a" or ch == "s" or ch == "d":
        my_village.update_royal(ch)
    elif ch == " ":
        my_village.royal_attack()
    elif ch == "l":
        my_village.royal_attack_special()
    elif ch == "r":
        my_village.rage()
    elif ch == "h":
        my_village.heal_all()
    time.sleep(ts - min(end - start, ts))
    # except:
    #     # make_replay(init, replay_input)
    #     print()
    #     os.system("stty echo")
    #     break

