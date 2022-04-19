# Person: movement_speed, movement, damage, health, max_health
from colorama import Fore, Back, Style
import numpy as np

class Person(object):
    def __init__(self, x, y, movement_speed, health, damage, symbol, length, breadth, range=1):
        self.x = x
        self.y = y
        self.movement_speed = movement_speed
        self.health = health
        self.max_health = health
        self.damage = damage
        self.symbol = symbol
        self.length = length
        self.breadth = breadth
        self.alive = True
        self.dir = "s"
        self.range = range
    
    def get_x(self):
        return int(self.x)
    
    def get_y(self):
        return int(self.y)

    def get_symbol(self):
        return self.symbol

    def get_movement_speed(self):
        return self.movement_speed

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_damage(self):
        return self.damage

    def get_symbol(self):
        return self.symbol

    def get_length(self):
        return self.length

    def get_breadth(self):
        return self.breadth

    def get_color(self):
        return ""

    def get_dir(self):
        return self.dir

    def get_range(self):
        return self.range

    def isAlive(self):
        return self.alive

    def set_dir(self, dir):
        self.dir = dir

    def set_symbol(self, symbol):
        self.symbol = symbol
    
    def set_length(self, length):
        self.length = length

    def set_breadth(self, breadth):
        self.breadth = breadth

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return False
        else:
            return True

    
    
    def kill(self):
        self.alive = False
        self.health = 0
        if self.get_length() == 2:
            self.set_symbol([["\U0001FAA6"], ["  "]])
        else:
            self.set_symbol([["\U0001FAA6", "  "]])

    def rage(self, damage_factor):
        self.damage *= damage_factor

    def heal(self, heal_factor):
        self.health = min(self.health * heal_factor, self.max_health)


# Variables
king_movement_speed = 1
king_health = 150
king_damage = 10    
queen_damage = 5

barb_damage = 5
barb_health = 50
barb_speed = 1

archer_range = 5

class King(Person):
    def __init__(self, x, y, royal, damage=king_damage, movement_speed=king_movement_speed, health=king_health):
        if royal == 'k':
            self.crown = "\U0001F451"
            self.sword = "\U0001F5E1 "
        else:
            self.crown = "\U0001F451"
            self.sword = "\U0001F3F9"
        super(King, self).__init__(x, y, movement_speed, health, damage, [[self.crown], [self.sword]], 2, 1)



    def health_bar(self):
        health_bar = ""
        for i in range(int(self.health*10/self.max_health)):
            if i < 2:
                health_bar += Fore.RED + "██"
            elif i < 5:
                health_bar += Fore.YELLOW + "██"
            else:
                health_bar += Fore.GREEN + "██"
        if (self.health*100/self.max_health) % 10 > 0:
            health_bar += "░░"
        health_bar += Style.RESET_ALL
        return health_bar

    def move(self, direction):
        if direction == "w":
            self.x -= self.movement_speed
            self.set_length(2)
            self.set_breadth(1)
            self.set_symbol([
                [self.sword], 
                [self.crown]])
        elif direction == "a":
            self.y -= self.movement_speed
            self.set_length(1)
            self.set_breadth(2)
            self.set_symbol([[self.sword, self.crown]])
        elif direction == "s":
            self.x += self.movement_speed
            self.set_length(2)
            self.set_breadth(1)
            self.set_symbol([
                [self.crown], 
                [self.sword]])
        elif direction == "d":
            self.y += self.movement_speed
            self.set_length(1)
            self.set_breadth(2)
            self.set_symbol([[self.crown, self.sword]])
        else:
            return
        self.set_dir(direction)
        
    

class Barbarian(Person):
    def __init__(self, x, y, movement_speed=barb_speed, health=barb_health, damage=barb_damage):
        self.helmet = "O/"
        super(Barbarian, self).__init__(x, y, movement_speed, health, damage, [[self.helmet]], 1, 1)

    def get_color(self):
        if self.isAlive():
            if(self.health / self.max_health >= 0.5):
                return Style.BRIGHT + Fore.YELLOW
            elif(self.health / self.max_health >= 0.2):
                return Style.NORMAL + Fore.YELLOW
            else:
                return Style.DIM + Fore.YELLOW
        else:
            return Back.RESET

    def find_building(self, grid):
        # 2d breadth first search on grid
        queue = [(self.get_x(), self.get_y())]
        visited = []
        while queue:
            x, y = queue.pop(0)
            if (x, y) not in visited:
                visited.append((x, y))
                if len(grid[x][y]):
                    b = grid[x][y].split()[0]
                    if b == "th" or b == "h" or b == "c":
                        return (x, y)
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if (i, j) not in visited and 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                            queue.append((i, j))


    def next_move(self, grid, target):
        '''
        Return wall position if next move is attacking a wall else return None
        '''
        # moves = {"w": np.array([-1, 0]), "a": np.array([0, -1]), "s": np.array([1, 0]), "d": np.array([0, 1]), "sd": np.array([1, 1]), "sa": np.array([1, -1]), "wa": np.array([-1, -1]), "wd": np.array([-1, 1])}
        moves = {"w": np.array([-1, 0]), "a": np.array([0, -1]), "s": np.array([1, 0]), "d": np.array([0, 1])}
        self.update_dir(target)
        x = self.get_x()
        y = self.get_y()
        pos = np.array([x, y])
        new_dir = self.get_dir()
        next_pos = pos + moves[new_dir]
        if grid[next_pos[0]][next_pos[1]] != "":
            return next_pos
        else:
            return new_dir

    def update_dir(self, building):
        self.dir = ""
        # if building[0] > self.get_x():
        #     self.dir += "s"
        # if building[0] < self.get_x():
        #     self.dir += "w"
        # if building[1] > self.get_y():
        #     self.dir += "d"
        # if building[1] < self.get_y():
        #     self.dir += "a"
        if building[0] > self.get_x():
            self.dir += "s"
        elif building[0] < self.get_x():
            self.dir += "w"
        elif building[1] > self.get_y():
            self.dir += "d"
        elif building[1] < self.get_y():
            self.dir += "a"
        # else:
        #     return "m"
        return self.dir

    def move(self, dir):
        for direction in dir:
            if direction == "w":
                self.x -= self.movement_speed
            elif direction == "a":
                self.y -= self.movement_speed
            elif direction == "s":
                self.x += self.movement_speed
            elif direction == "d":
                self.y += self.movement_speed
            else:
                return
        # self.set_dir(direction)
            
class Balloon(Person):
    def __init__(self, x, y, movement_speed=2*king_movement_speed, health=barb_health, damage=2*barb_damage):
        self.bal = "∫O"
        super().__init__(x, y, movement_speed, health, damage, [[self.bal]], 1, 1)

    def get_color(self):
        if self.isAlive():
            if(self.health / self.max_health >= 0.5):
                return Style.BRIGHT + Fore.CYAN
            elif(self.health / self.max_health >= 0.2):
                return Style.NORMAL + Fore.CYAN
            else:
                return Style.DIM + Fore.CYAN
        else:
            return Back.RESET

    def next_move(self, grid, target):
        '''
        Return wall position if next move is attacking a wall else return None
        '''
        # moves = {"w": np.array([-1, 0]), "a": np.array([0, -1]), "s": np.array([1, 0]), "d": np.array([0, 1]), "sd": np.array([1, 1]), "sa": np.array([1, -1]), "wa": np.array([-1, -1]), "wd": np.array([-1, 1])}
        # moves = {"w": np.array([-1, 0]), "a": np.array([0, -1]), "s": np.array([1, 0]), "d": np.array([0, 1])}
        # self.update_dir(target)
        # x = self.get_x()
        # y = self.get_y()
        # pos = np.array([x, y])
        # new_dir = self.get_dir()
        # next_pos = pos + moves[new_dir]
        return self.update_dir(target)

    def update_dir(self, building):
        self.dir = ""
        # if building[0] > self.get_x():
        #     self.dir += "s"
        # if building[0] < self.get_x():
        #     self.dir += "w"
        # if building[1] > self.get_y():
        #     self.dir += "d"
        # if building[1] < self.get_y():
        #     self.dir += "a"
        if building[0] > self.get_x():
            self.dir += "s"
        elif building[0] < self.get_x():
            self.dir += "w"
        elif building[1] > self.get_y():
            self.dir += "d"
        elif building[1] < self.get_y():
            self.dir += "a"
        # else:
        #     return "m"
        return self.dir

    def move(self, dir):
        for direction in dir:
            if direction == "w":
                self.x -= self.movement_speed
            elif direction == "a":
                self.y -= self.movement_speed
            elif direction == "s":
                self.x += self.movement_speed
            elif direction == "d":
                self.y += self.movement_speed
            else:
                return

class Archer(Person):
    def __init__(self, x, y, movement_speed=barb_speed*2, health=barb_health/2, damage=barb_damage/2):
        self.bow = "D-"
        super(Archer, self).__init__(x, y, movement_speed, health, damage, [[self.bow]], 1, 1, archer_range)
    
    def get_color(self):
        if self.isAlive():
            if(self.health / self.max_health >= 0.5):
                return Style.BRIGHT + Fore.BLUE
            elif(self.health / self.max_health >= 0.2):
                return Style.NORMAL + Fore.BLUE
            else:
                return Style.DIM + Fore.BLUE
        else:
            return Back.RESET

    def next_move(self, grid, target):
        '''
        Return wall position if next move is attacking a wall else return None
        '''
        # moves = {"w": np.array([-1, 0]), "a": np.array([0, -1]), "s": np.array([1, 0]), "d": np.array([0, 1]), "sd": np.array([1, 1]), "sa": np.array([1, -1]), "wa": np.array([-1, -1]), "wd": np.array([-1, 1])}
        moves = {"w": np.array([-1, 0]), "a": np.array([0, -1]), "s": np.array([1, 0]), "d": np.array([0, 1])}
        self.update_dir(target)
        x = self.get_x()
        y = self.get_y()
        pos = np.array([x, y])
        new_dir = self.get_dir()
        next_pos = pos + moves[new_dir]
        if grid[next_pos[0]][next_pos[1]] != "":
            return next_pos
        else:
            return new_dir

    def update_dir(self, building):
        self.dir = ""
        # if building[0] > self.get_x():
        #     self.dir += "s"
        # if building[0] < self.get_x():
        #     self.dir += "w"
        # if building[1] > self.get_y():
        #     self.dir += "d"
        # if building[1] < self.get_y():
        #     self.dir += "a"
        if building[0] > self.get_x():
            self.dir += "s"
        elif building[0] < self.get_x():
            self.dir += "w"
        elif building[1] > self.get_y():
            self.dir += "d"
        elif building[1] < self.get_y():
            self.dir += "a"
        # else:
        #     return "m"
        return self.dir

    def move(self, dir):
        for direction in dir:
            if direction == "w":
                self.x -= self.movement_speed
            elif direction == "a":
                self.y -= self.movement_speed
            elif direction == "s":
                self.x += self.movement_speed
            elif direction == "d":
                self.y += self.movement_speed
            else:
                return

# if __name__ == "__main__":
#     a = Balloon(0, 0)
#     print(a.get_symbol()[0)