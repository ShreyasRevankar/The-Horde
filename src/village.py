from src.building import *
from src.person import *
from src.spells import *
from src.input import *
from copy import deepcopy
import numpy as np
import warnings
import time
import json


# Some variables


class village(object):
    def __init__(self, level=1):
        self.level = level
    
    def init_village(self, level, royal):
        with open("src/init/level" + str(level) + ".json", "r") as f:
            init = json.load(f)

        self.level = level
        self.set_dimensions(init["village_dimensions"][0], init["village_dimensions"][1])
        self.grid = [["| "] + ["  " for i in range(self.length)] + [" |"] for j in range(self.breadth)]
        self.grid = [["--"] * (self.length + 2)] + self.grid + [["--"] * (self.length + 2)]
        self.back_grid = [['bd' if i != "  " else "" for i in row] for row in self.grid]
        self.dist_grid = [[(np.inf, np.inf) for i in row] for row in self.grid]
        self.dist_grid_b = [[(np.inf, np.inf) for i in row] for row in self.grid]
        self.barbarian_list = []
        self.archer_list = []
        self.balloon_list = []
        self.time_step = 0.1
        self.num_heals = 5
        self.rage_spell = Rage()
        self.eagle = np.inf
        self.set_town_hall(init['town_hall_pos'][0], init['town_hall_pos'][1])
        self.set_hut(init['hut_pos'])
        self.set_wall(init['wall_pos'])
        self.set_cannon(init['cannon_pos'])
        self.set_tower(init['tower_pos'])
        self.set_spawning_pos(init['spawning_pos'])
        self.set_num_troops(init['num_per_troop'])
        self.set_royal(init['royal_pos'][0], init['royal_pos'][1], royal)

    def set_dimensions(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def set_num_troops(self, num_troops):
        self.num_barbarians = num_troops
        self.num_archers = num_troops
        self.num_balloons = num_troops

    def set_town_hall(self, x, y):
        self.town_hall = town_hall(x, y)
        th_length = self.town_hall.get_length()
        th_breadth = self.town_hall.get_breadth()
        th_symbol = self.town_hall.get_symbol()
        self.set_dist_for_building(self.town_hall, self.dist_grid)
        for i in range(th_length):
            for j in range(th_breadth):
                self.grid[x + i][y + j] = self.town_hall.get_color() + th_symbol[i][j]
                self.back_grid[x + i][y + j] = 'th 0'

    def set_hut(self, hut_pos):
        self.huts = []
        for i in hut_pos:
            x = i[0]
            y = i[1]
            cur_hut = hut(x, y)
            self.huts.append(cur_hut)
            h_length = cur_hut.get_length()
            h_breadth = cur_hut.get_breadth()
            h_symbol = cur_hut.get_symbol()
            h_color = cur_hut.get_color()
            self.set_dist_for_building(cur_hut, self.dist_grid)
            for i in range(h_length):
                for j in range(h_breadth):
                    self.grid[i + x][j + y] = h_color + h_symbol[i][j]
                    self.back_grid[i + x][j + y] = 'h' + ' ' + str(len(self.huts) - 1)


    def set_wall(self, wall_pos):
        self.walls = []
        for i in wall_pos:
            x = i[0]
            y = i[1]
            cur_wall = wall(x, y)
            self.walls.append(cur_wall)
            w_length = cur_wall.get_length()
            w_breadth = cur_wall.get_breadth()
            w_symbol = cur_wall.get_symbol()
            w_color = cur_wall.get_color()
            for i in range(w_length):
                for j in range(w_breadth):
                    self.grid[i + x][j + y] = w_color + w_symbol[i][j]
                    self.back_grid[i + x][j + y] = 'w' + ' ' + str(len(self.walls) - 1)


    def set_cannon(self, cannon_pos):
        self.cannons = []
        for i in cannon_pos:
            x = i[0]
            y = i[1]
            cur_cannon = cannon(x, y)
            self.cannons.append(cur_cannon)
            c_length = cur_cannon.get_length()
            c_breadth = cur_cannon.get_breadth()
            c_symbol = cur_cannon.get_symbol()
            c_color = cur_cannon.get_color()
            self.set_dist_for_building(cur_cannon, self.dist_grid)
            for i in range(c_length):
                for j in range(c_breadth):
                    self.grid[i + x][j + y] = c_color + c_symbol[i][j]
                    self.back_grid[i + x][j + y] = 'c' + ' ' + str(len(self.cannons) - 1)

    def set_tower(self, tower_pos):
        self.towers = []
        for i in tower_pos:
            x = i[0]
            y = i[1]
            cur_tower = tower(x, y)
            self.towers.append(cur_tower)
            t_length = cur_tower.get_length()
            t_breadth = cur_tower.get_breadth()
            t_symbol = cur_tower.get_symbol()
            t_color = cur_tower.get_color()
            self.set_dist_for_building(cur_tower, self.dist_grid)
            for i in range(t_length):
                for j in range(t_breadth):
                    self.grid[i + x][j + y] = t_color + t_symbol[i][j]
                    self.back_grid[i + x][j + y] = 't' + ' ' + str(len(self.towers) - 1)


    def set_spawning_pos(self, spawning_pos):
        self.spawning_pos = spawning_pos

    
    def set_royal(self, x, y, royal):
        self.royal = royal
        self.king = King(x, y, royal, queen_damage) if royal == 'q' else King(x, y, royal, king_damage)
        k_length = self.king.get_length()
        k_breadth = self.king.get_breadth()
        k_symbol = self.king.get_symbol()
        for i in range(k_length):
            for j in range(k_breadth):
                self.grid[i + x][j + y] = k_symbol[i][j]
                # self.back_grid[i + x][j + y] = 'k 0'

    def get_time_step(self):
        return self.time_step
        
    def calc_dist(self, pos, cur_target, pot_target):
        x = pos[0]
        y = pos[1]
        x1 = cur_target[0]
        y1 = cur_target[1]
        x2 = pot_target[0]
        y2 = pot_target[1]
        # Manhattan distance
        if abs(x - x2) + abs(y - y2) < abs(x - x1) + abs(y - y1):
            return pot_target
        # Euclidean distance
        # if np.sqrt((x - x2) ** 2 + (y - y2) ** 2) < np.sqrt((x - x1) ** 2 + (y - y1) ** 2):
        #     return pot_target
        else:
            return cur_target


    def set_dist_for_building(self, b, grid):
        x1 = b.get_x()
        y1 = b.get_y()
        b_length = b.get_length()
        b_breadth = b.get_breadth()
        x2 = x1 + b_length - 1
        y2 = y1 + b_breadth - 1 
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i <= x1 and j <= y1:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (x1, y1))
                elif i <= x2 and j <= y1:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (i, y1))
                elif j <= y1:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (x2, y1))
                elif i <= x1 and j <= y2:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (x1, j))
                elif i <= x1:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (x1, y2))
                elif i <= x2 and j <= y2:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (i, j))
                elif i <= x2:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (i, y2))
                elif j <= y2:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (x2, j))
                else:
                    grid[i][j] = self.calc_dist((i, j), grid[i][j], (x2, y2))
                
    def set_dist(self):
        self.dist_grid = [[(np.inf, np.inf) for i in row] for row in self.grid]
        self.dist_grid_b = [[(np.inf, np.inf) for i in row] for row in self.grid]
        if self.town_hall is not None:
            self.set_dist_for_building(self.town_hall, self.dist_grid)
        for hut in self.huts:
            if hut is not None:
                self.set_dist_for_building(hut, self.dist_grid)
        for cannon in self.cannons:
            if cannon is not None:
                self.set_dist_for_building(cannon, self.dist_grid)
                self.set_dist_for_building(cannon, self.dist_grid_b)
        for tower in self.towers:
            if tower is not None:
                self.set_dist_for_building(tower, self.dist_grid)
                self.set_dist_for_building(tower, self.dist_grid_b)

    
    def update_building(self, b):
        b_x = b.get_x()
        b_y = b.get_y()
        b_length = b.get_length()
        b_breadth = b.get_breadth()
        b_color = b.get_color()
        b_symbol = b.get_symbol()
        for i in range(b_length):
                for j in range(b_breadth):
                    self.grid[i + b_x][j + b_y] = b_color + b_symbol[i][j]

    def update_royal(self, m):
        if self.king.isAlive():
            temp_king = deepcopy(self.king)
            self.king.move(m)
            x = self.king.get_x()
            y = self.king.get_y()
            k_length = self.king.get_length()
            k_breadth = self.king.get_breadth()
            for i in range(x, x + k_length):
                for j in range(y, y + k_breadth):
                    b = self.back_grid[i][j].split()[0] if len(self.back_grid[i][j]) > 0 else ''
                    if b == 'th' or b == 'h' or b == 'w' or b == 'c' or b == 'bd' or b == 't':
                        self.king = temp_king
                        return False
            self.delete_building(temp_king)
            self.update_building(self.king)

    def delete_building(self, b):
        b_x = b.get_x()
        b_y = b.get_y()
        b_length = b.get_length()
        b_breadth = b.get_breadth()
        for i in range(b_length):
                for j in range(b_breadth):
                    self.grid[i + b_x][j + b_y] = "  "
                    self.back_grid[i + b_x][j + b_y] = ""
        
    def royal_attack(self):
        if self.king.isAlive():
            x = self.king.get_x()
            y = self.king.get_y()
            if self.royal == 'q':
                if self.king.get_dir() == 'w':
                    for i in range(x - 10, x - 5):
                        for j in range(y - 2, y + 3):
                            self.take_hit(i, j, self.king.get_damage())
                elif self.king.get_dir() == 'a':
                    for i in range(x - 2, x + 3):
                        for j in range(y - 10, y - 5):
                            self.take_hit(i, j, self.king.get_damage())
                elif self.king.get_dir() == 's':
                    for i in range(x + 6, x + 11):
                        for j in range(y - 2, y + 3):
                            self.take_hit(i, j, self.king.get_damage())
                elif self.king.get_dir() == 'd':
                    for i in range(x - 2, x + 3):
                        for j in range(y + 6, y + 11):
                            self.take_hit(i, j, self.king.get_damage())
                else:
                    return False
            else:
                if self.king.get_dir() == 'w':
                    self.take_hit(x - 1, y, self.king.get_damage())
                elif self.king.get_dir() == 'a':
                    self.take_hit(x, y - 1, self.king.get_damage())
                elif self.king.get_dir() == 's':
                    self.take_hit(x + 2, y, self.king.get_damage())
                elif self.king.get_dir() == 'd':
                    self.take_hit(x, y + 2, self.king.get_damage())
                else:
                    return False

    def royal_attack_special(self):
        if self.king.isAlive():
            if self.royal == 'k':
                x = self.king.get_x()
                y = self.king.get_y()
                buildings_hit = []
                for i in range(x - 5, x + 6):
                    for j in range(y - 5, y + 6):
                        if self.back_grid[i][j] not in buildings_hit:
                            self.take_hit(i, j, self.king.get_damage())
                            buildings_hit.append(self.back_grid[i][j])
            elif self.royal == 'q':
                self.eagle = 1

    def eagle_attack(self):
        self.eagle -= self.time_step
        if self.eagle <= 0:
            self.eagle = np.inf
            x = self.king.get_x()
            y = self.king.get_y()
            if self.king.get_dir() == 'w':
                for i in range(x - 20, x - 15):
                    for j in range(y - 4, y + 5):
                        self.take_hit(i, j, self.king.get_damage())
            elif self.king.get_dir() == 'a':
                for i in range(x - 4, x + 5):
                    for j in range(y - 20, y - 15):
                        self.take_hit(i, j, self.king.get_damage())
            elif self.king.get_dir() == 's':
                for i in range(x + 15, x + 20):
                    for j in range(y - 4, y + 5):
                        self.take_hit(i, j, self.king.get_damage())
            elif self.king.get_dir() == 'd':
                for i in range(x - 4, x + 5):
                    for j in range(y + 15, y + 20):
                        self.take_hit(i, j, self.king.get_damage())
            else:
                return False

    def take_hit(self, x, y, damage):
        if not (1 <= x < self.length and 1 <= y < self.breadth):
            return
        if self.back_grid[x][y] == "":
            return
        b_type = self.back_grid[x][y].split()[0]
        b_num = int(self.back_grid[x][y].split()[1])
        if b_type == 'th':
            if self.town_hall.take_damage(damage):
                self.update_building(self.town_hall)
            else:
                self.delete_building(self.town_hall)
                self.town_hall = None
                self.set_dist()
        elif b_type == 'h':
            if self.huts[b_num].take_damage(damage):
                self.update_building(self.huts[b_num])
            else:
                self.delete_building(self.huts[b_num])
                self.huts[b_num] = None
                self.set_dist()
        elif b_type == 'w':
            if self.walls[b_num].take_damage(damage):
                self.update_building(self.walls[b_num])
            else:
                self.delete_building(self.walls[b_num])
                self.walls[b_num] = None
        elif b_type == 'c':
            if self.cannons[b_num].take_damage(damage):
                self.update_building(self.cannons[b_num])
            else:
                self.delete_building(self.cannons[b_num])
                self.cannons[b_num] = None
                self.set_dist()
        elif b_type == 't':
            if self.towers[b_num].take_damage(damage):
                self.update_building(self.towers[b_num])
            else:
                self.delete_building(self.towers[b_num])
                self.towers[b_num] = None
                self.set_dist()
        else:
            return
        
    def spawn_troop(self, k):
        if k < 3:
            if self.num_barbarians > 0:
                self.num_barbarians -= 1
                x = self.spawning_pos[k][0]
                y = self.spawning_pos[k][1]
                # self.grid[x][y] = "1 " if self.grid[x][y] == "  " else str(int(self.grid[x][y][0]) + 1) + " "
                # barb_damage = 5
                # barb_health = 50
                # barb = Barbarian(x, y, barb_health, barb_damage)
                barb = Barbarian(x, y)
                self.update_building(barb)
                self.barbarian_list.append(barb)
        elif k < 6:
            if self.num_archers > 0:
                # print(k)
                k -= 3
                self.num_archers -= 1
                x = self.spawning_pos[k][0]
                y = self.spawning_pos[k][1]
                # self.grid[x][y] = "2 " if self.grid[x][y] == "  " else str(int(self.grid[x][y][0]) + 1) + " "
                # archer_damage = 10
                # archer_health = 100
                # archer = Archer(x, y, archer_health, archer_damage)
                archer = Archer(x, y)
                self.update_building(archer)
                self.archer_list.append(archer)
        elif k < 9:
            if self.num_balloons > 0:
                k -= 6
                self.num_balloons -= 1
                x = self.spawning_pos[k][0]
                y = self.spawning_pos[k][1]
                # self.grid[x][y] = "3 " if self.grid[x][y] == "  " else str(int(self.grid[x][y][0]) + 1) + " "
                # balloon_damage = 20
                # balloon_health = 200
                # balloon = Balloon(x, y, balloon_health, balloon_damage)
                balloon = Balloon(x, y)
                self.update_building(balloon)
                self.balloon_list.append(balloon)

    def in_range(self, building_pos, troop_pos, range):
        if (building_pos[0] - troop_pos[0])**2 + (building_pos[1] - troop_pos[1])**2 <= range**2:
            return True
        return False

    # def barbarian_control(self):
    #     # moves = np.array(["w", "a", "s", "d", "wa", "wd", "sa", "sd"])
    #     moves = np.array(["w", "a", "s", "d"])
    #     for barbarian in self.barbarian_list:
    #         if barbarian.isAlive():
    #             x = barbarian.get_x()
    #             y = barbarian.get_y()
    #             building = self.dist_grid[x][y]
    #             if building in [(i, j) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)]:
    #                 self.take_hit(building[0], building[1], barbarian.get_damage())
    #             else:
    #                 mv = barbarian.next_move(self.back_grid, building)
    #                 warnings.simplefilter(action='ignore', category=FutureWarning)
    #                 if mv not in moves:
    #                     self.take_hit(mv[0], mv[1], barbarian.get_damage())
    #                 else:
    #                     self.delete_building(barbarian)
    #                     barbarian.move(mv)
    #                     self.update_building(barbarian)
    #         else:
    #             self.update_building(barbarian)

    def troop_control(self, troop_list):
        # moves = np.array(["w", "a", "s", "d", "wa", "wd", "sa", "sd"])
        moves = np.array(["w", "a", "s", "d"])
        for troop in troop_list:
            if troop.isAlive():
                x = troop.get_x()
                y = troop.get_y()
                building = self.dist_grid[x][y]
                r = troop.get_range()
                if self.in_range(building, (x, y), r):
                    self.take_hit(building[0], building[1], troop.get_damage())
                else:
                    mv = troop.next_move(self.back_grid, building)
                    warnings.simplefilter(action='ignore', category=FutureWarning)
                    if mv not in moves:
                        self.take_hit(mv[0], mv[1], troop.get_damage())
                    else:
                        self.delete_building(troop)
                        troop.move(mv)
                        # self.update_building(troop)
            # else:
            #     self.update_building(troop)
            self.update_building(troop)

    def balloon_control(self):
        # moves = np.array(["w", "a", "s", "d"])
        for balloon in self.balloon_list:
            if balloon.isAlive():
                x = balloon.get_x()
                y = balloon.get_y()
                d_building = self.dist_grid_b[x][y]
                if d_building == (x, y):
                    self.take_hit(x, y, balloon.get_damage())
                elif d_building == (np.inf, np.inf):
                    building = self.dist_grid[x][y]
                    if building == (x, y):
                        self.take_hit(x, y, balloon.get_damage())
                    else:
                        mv = balloon.next_move(self.back_grid, building)
                        self.delete_building(balloon)
                        balloon.move(mv)
                        # self.update_building(balloon)
                else:
                    mv = balloon.next_move(self.back_grid, d_building)
                    self.delete_building(balloon)
                    balloon.move(mv)
            #         self.update_building(balloon)
            # else:
            #     self.update_building(balloon)
            self.update_building(balloon)

    # def i


    def cannon_attack(self):
        if self.rage_spell.get_can() % self.rage_spell.get_mod() == 0:
            for c in range(len(self.cannons)):
                cannon = self.cannons[c]
                if cannon is not None:
                    c_range = cannon.get_range()
                    flag = True
                    for i in range(len(self.barbarian_list)):
                        barbarian = self.barbarian_list[i]
                        if barbarian.isAlive():
                            x = barbarian.get_x()
                            y = barbarian.get_y()
                            if (x, y) in c_range:
                                if barbarian.take_damage(cannon.get_damage()):
                                    self.update_building(barbarian)
                                else:
                                    self.barbarian_list[i].kill()
                                flag = False
                                break
                    if flag:
                        for i in range(len(self.archer_list)):
                            archer = self.archer_list[i]
                            if archer.isAlive():
                                x = archer.get_x()
                                y = archer.get_y()
                                if (x, y) in c_range:
                                    if archer.take_damage(cannon.get_damage()):
                                        self.update_building(archer)
                                    else:
                                        self.archer_list[i].kill()
                                    flag = False
                                    break
                    if flag and self.king.isAlive():
                        x = self.king.get_x()
                        y = self.king.get_y()
                        if (x, y) in c_range:
                            if not self.king.take_damage(cannon.get_damage()):
                                self.king.kill()
                                self.update_building(self.king)
                            flag = False
                    self.cannons[c].shooting(flag)
                    self.update_building(self.cannons[c])
        self.rage_spell.set_can((self.rage_spell.get_can() + 1) % self.rage_spell.get_mod())

    def tower_attack(self):
        if self.rage_spell.get_can() % self.rage_spell.get_mod() == 0:
            for c in range(len(self.towers)):
                tower = self.towers[c]
                if tower is not None:
                    c_range = tower.get_range()
                    flag = True
                    for i in range(len(self.balloon_list)):
                        balloon = self.balloon_list[i]
                        if balloon.isAlive():
                            x = balloon.get_x()
                            y = balloon.get_y()
                            if (x, y) in c_range:
                                self.aoe_damage(x, y, tower.get_damage())
                                flag = False
                                break
                    if flag:
                        for i in range(len(self.barbarian_list)):
                            barbarian = self.barbarian_list[i]
                            if barbarian.isAlive():
                                x = barbarian.get_x()
                                y = barbarian.get_y()
                                if (x, y) in c_range:
                                    self.aoe_damage(x, y, tower.get_damage())
                                    flag = False
                                    break
                    if flag:
                        for i in range(len(self.archer_list)):
                            archer = self.archer_list[i]
                            if archer.isAlive():
                                x = archer.get_x()
                                y = archer.get_y()
                                if (x, y) in c_range:
                                    self.aoe_damage(x, y, tower.get_damage())
                                    flag = False
                                    break
                    if flag and self.king.isAlive():
                        x = self.king.get_x()
                        y = self.king.get_y()
                        if (x, y) in c_range:
                            self.aoe_damage(x, y, tower.get_damage())
                            # if not self.king.take_damage(tower.get_damage()):
                            #     self.king.kill()
                            #     self.update_building(self.king)
                            flag = False
                    self.towers[c].shooting(flag)
                    self.update_building(self.towers[c])
        self.rage_spell.set_can((self.rage_spell.get_can() + 1) % self.rage_spell.get_mod())

    def aoe_damage(self, x, y, damage):
        d_range = [(i, j) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)]
        for i in range(len(self.barbarian_list)):
            barbarian = self.barbarian_list[i]
            if barbarian.isAlive():
                b_x = barbarian.get_x()
                b_y = barbarian.get_y()
                if (b_x, b_y) in d_range:
                    if barbarian.take_damage(damage):
                        self.update_building(barbarian)
                    else:
                        self.barbarian_list[i].kill()
        for i in range(len(self.archer_list)):
            archer = self.archer_list[i]
            if archer.isAlive():
                a_x = archer.get_x()
                a_y = archer.get_y()
                if (a_x, a_y) in d_range:
                    if archer.take_damage(damage):
                        self.update_building(archer)
                    else:
                        self.archer_list[i].kill()
        for i in range(len(self.balloon_list)):
            balloon = self.balloon_list[i]
            if balloon.isAlive():
                b_x = balloon.get_x()
                b_y = balloon.get_y()
                if (b_x, b_y) in d_range:
                    balloon.take_damage(damage)
                    if balloon.take_damage(damage):
                        self.update_building(balloon)
                    else:
                        self.balloon_list[i].kill()
        k_x = self.king.get_x()
        k_y = self.king.get_y()
        if (k_x, k_y) in d_range:
            if not self.king.take_damage(damage):
                self.king.kill()
                self.update_building(self.king)

    def heal_all(self):
        if self.num_heals:
            self.num_heals -= 1
            h = Heal()
            if self.king.isAlive():
                self.king.heal(h.get_heal_factor())
            for barbarian in self.barbarian_list:
                if barbarian.isAlive():
                    barbarian.heal(h.get_heal_factor())
            for archer in self.archer_list:
                if archer.isAlive():
                    archer.heal(h.get_heal_factor())
            for balloon in self.balloon_list:
                if balloon.isAlive():
                    balloon.heal(h.get_heal_factor())

    def rage(self):
        self.rage_spell.set_mod(2)
        self.time_step /= 2
        if self.king.isAlive():
            self.king.rage(self.rage_spell.get_damage_factor())
        for barbarian in self.barbarian_list:
            if barbarian.isAlive():
                barbarian.rage(self.rage_spell.get_damage_factor())

    def refresh_grid(self):
        if self.town_hall is not None:
            self.update_building(self.town_hall)
        for hut in self.huts:
            if hut is not None:
                self.update_building(hut) 
        for cannon in self.cannons:
            if cannon is not None:
                self.update_building(cannon)
        for tower in self.towers:
            if tower is not None:
                self.update_building(tower)
        for wall in self.walls:
            if wall is not None:
                self.update_building(wall)

        for barbarian in self.barbarian_list:
            if barbarian.isAlive():
                self.update_building(barbarian)
        for archer in self.archer_list:
            if archer.isAlive():
                self.update_building(archer)
        for balloon in self.balloon_list:
            if balloon.isAlive():
                self.update_building(balloon)

        self.update_building(self.king)

    def display_village(self):
        # self.barbarian_control()
        self.troop_control(self.barbarian_list)
        self.troop_control(self.archer_list)
        self.balloon_control()
        self.eagle_attack()
        self.update_building(self.king)
        self.cannon_attack()
        self.tower_attack()
        self.refresh_grid()
        print(self.king.health_bar())
        for row in self.grid:
            for char in row:
                print(char + Style.RESET_ALL, end="")
            print()

    def is_game_over(self):
        flag = True
        if self.town_hall is not None:
            flag = False
        if flag:
            for hut in self.huts:
                if hut is not None:
                    flag = False
                    break
        if flag:
            for cannon in self.cannons:
                if cannon is not None:
                    flag = False
                    break
        if flag:
            for tower in self.towers:
                if tower is not None:
                    flag = False
                    break


        flag2 = True
        if self.king.isAlive():
            flag2 = False

        if flag2:
            flag2 = self.num_barbarians == 0
        if flag2:
            for barbarian in self.barbarian_list:
                if barbarian.isAlive():
                    flag2 = False
                    break

        if flag2:
            flag2 = self.num_archers == 0
        if flag2:
            for archer in self.archer_list:
                if archer.isAlive():
                    flag2 = False
                    break

        if flag2:
            flag2 = self.num_balloons == 0
        if flag2:
            for balloon in self.balloon_list:
                if balloon.isAlive():
                    flag2 = False
                    break
        return self.game_over(flag, flag2, self.level)


    def game_over(self, flag1, flag2, level):
        if flag1:
            if level == 1:
                self.init_village(2, self.royal)
            elif level == 2:
                self.init_village(3, self.royal)
            elif level == 3:
                with open("src/utils/victory.txt", "r") as f:
                    print(f.read())
                return True
        elif flag2:
            with open("src/utils/defeat.txt", "r") as f:
                print(f.read())
            return True
        return False


        


        



            
        


