from colorama import Fore, Back, Style
import numpy as np

class building(object):
    def __init__(self, health, length, breadth, x, y, symbol):
        self.max_health = health
        self.health = self.max_health
        self.length = length
        self.breadth = breadth
        self.x = x
        self.y = y
        self.symbol = symbol


    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
    
    def get_symbol(self):
        return self.symbol

    def get_length(self):
        return self.length
    
    def get_breadth(self):
        return self.breadth

    def get_health(self):
        return self.health

    def get_color(self, fore_color=Fore.RESET):
        if(self.health / self.max_health >= 0.5):
            return fore_color + Back.GREEN
        elif(self.health / self.max_health >= 0.2):
            return fore_color + Back.YELLOW
        else:
            return fore_color + Back.RED
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return False
        else:
            return True
    
    def display_building(self):
        for row in self.symbol:
            for char in row:
                print(char, end="")
            print()


# Variables 
th_max_health = 100
hut_max_health = 60
wall_max_health = 30
cannon_max_health = 50

cannon_damage = 5
cannon_range = 5

# Child classes

class town_hall(building):
    def __init__(self, x, y, max_health=th_max_health):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = self.max_health
        self.length = 4
        self.breadth = 3
        self.symbol = [
            ["/\\", "  ", "/\\"], 
            ["||", "/\\", "||"], 
            ["||", "__", "||"], 
            ["||", "∏∏", "||"]
            ]
        # self.symbol = "hell"
class hut(building):
    def __init__(self, x, y, max_health=hut_max_health):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = self.max_health
        self.length = 2
        self.breadth = 2
        self.symbol = [
            ["//", "\\\\"], 
            ["|_", "_|"]
            ]


class wall(building):
    def __init__(self, x, y, max_health=wall_max_health):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = self.max_health
        self.length = 1
        self.breadth = 1
        self.symbol = [["[]"]]

class cannon(building):
    def __init__(self, x, y, damage=cannon_damage, range=cannon_range, max_health=cannon_max_health):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = self.max_health
        self.length = 3
        self.breadth = 2
        self.symbol = [
            ["  ", "/O"],
            [" /", "/ "],
            ["==", "=="]
        ]
        self.damage = damage
        self.range = range
        self.not_shoot = True

    def get_range(self):
        x = self.get_x()
        y = self.get_y()
        length = self.get_length()
        breadth = self.get_breadth()
        return [(i, j) for i in range(x - self.range, x + length + self.range) for j in range(y - self.range, y + breadth + self.range)]

    def get_damage(self):
        return self.damage

    def get_color(self):
        if self.not_shoot:
            return super().get_color()
        else:
            return super().get_color(Fore.RED)
    
    def shooting(self, value):
        self.not_shoot = value

class tower(building):
    def __init__(self, x, y, damage=cannon_damage, range=cannon_range, max_health=cannon_max_health):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = self.max_health
        self.length = 3
        self.breadth = 2
        self.symbol = [
            [" /", "\\ "],
            [" |", "| "],
            [" |", "| "]
        ]
        self.damage = damage
        self.range = range
        self.not_shoot = True

    def get_range(self):
        x = self.get_x()
        y = self.get_y()
        length = self.get_length()
        breadth = self.get_breadth()
        return [(i, j) for i in range(x - self.range, x + length + self.range) for j in range(y - self.range, y + breadth + self.range)]

    def get_damage(self):
        return self.damage

    def get_color(self):
        if self.not_shoot:
            return super().get_color()
        else:
            return super().get_color(Fore.RED)
    
    def shooting(self, value):
        self.not_shoot = value