from src.village import *
from src.input import *
import json
import os
import numpy as np
import time

replay_num = input("Which game do you want to replay? ")

with open("replays/replay.json", "r") as f:
    replays = json.load(f)

replay_input = replays[int(replay_num)]
replay_input.append("")

royal = replay_input[0]
replay_input = replay_input[1:]

my_village = village()
my_village.init_village(1, royal)

os.system("stty -echo")


for ch in replay_input:
    os.system("clear")
    if my_village.is_game_over():
        os.system("stty echo")
        break
    my_village.display_village()
    ts = my_village.get_time_step()
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
    time.sleep(ts)

