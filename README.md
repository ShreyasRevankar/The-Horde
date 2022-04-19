# The Horde

### A python CLI game with the gameplay as attacking of a village as in Clash of Clans.

Satisfy your urge of destroying buildings using strategy and tactics. 
Each success makes the next village more powerful.
Complete each level succesfully and become a Legen...wait for it..dary master of the Horde.
Lose and you'll be the laughing stock of your group.

## How to play

Open your terminal in this folder and type:

```
python3 game.py 
```
(Make sure you have python3.x pre-installed)
Follow instructions and enjoy the game.

## Buildings

1. **Town Hall** - The main building of the village. The most interior and well protected building.
```
/\  /\
||/\||
||__||
||∏∏||
```
2. **Hut** - A small building that is just there.
```
//\\
|__|
```
3. **Cannon** - A building that can shoot at your ground troops if you come within its range.
```
  /O
 //
====
```
4. **Wizard Tower** - A building that can shoot at your ground as well as air troops if you come within its range. Be careful as its one shot will affect all of your troops within the vicinity.
```
 /\
 ||
 ||
```
5. **Wall** - A building that can protect your village from attacks.
```
[]
```

Buildings change their background color as they incur damage - going from initially green to yellow to red - and finally getting destroyed.

Cannon and Wrizard tower become red when they are shooting at your troops.

## Troops

1. **Barbarian** - A simple ground troop that can attack buildings. It has to reach a building to attack it.
```
O/
```
2. **Archer** - A ground troop that can shoot at buildings. It can shoot at buildings from a distance.
```
D-
```
3. **Balloon** - A flying troop that can attack buildings. It will prioritize attacking defensive buildings. Cannons cannot shoot at balloons.
```
∫O
```

Troops are automated characters that will move around the map and attack buildings.

Troops will change their brightness as they take damage - going from initially bright to normal to dim - finally turning into tombstones when dead.

### Royal Troops

1. **King** - A ground troop that can attack buildings. It has to reach a building to attack it. It has a special ability of using its *Leviathan Axe*. This will cause all buildings within its vicinity to be damaged.
```
👑
🗡 
```
2. **Queen** - A ground troop that can attack buildings. It can shoot at buildings in an area of effect from a distance. It has a special ability of using its *Eagle Arrow*. This increases the range as well as area of effect of its arrows.
```
👑
🏹
```

Royal troops are playable characters. Their health is diplayed as a bar on top of the screen.

## Spells

1. **Rage** - A spell that increases the movement speed and damage of all living troops.
2. **Heal** - A spell that heals all living troops.

## Gameplay

1. **Movement** - W/A/S/D to move the royal troops around the map. Other ground troops have automated movement by moving to the nearest non-wall building and destroying it. If a wall comes in the way, the troop will first destroy the wall and then move to the nearest non-wall building.
2. **Attack** - *Space* to attack a building. 
3. **Special Ability** - *l* to use special ability
4. **Spawn** - *1-3* to spawn a new barbarian. *4-6* to spawn a new archer. *7-9* to spawn a new balloon.
5. **Spells** - *r* to use rage. *h* to use heal.
6. **Quit** - *q* to quit the game.

## Replay

All completed games are saved in replays/replay.json.

Run the following command to see a replay of your desired game:
```
python3 replay.py
```
And enter the game number of the replay you want to see.