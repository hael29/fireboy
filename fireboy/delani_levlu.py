import os
import pygame as p

print(f"nejprve napis do konzole jmeno souboru s koncovkou .txt, do ktereho se novy level ulozi\nmuzes napsat i jmeno existujiciho souboru a ten upravit\npotom jezdi mysi v mrizce\npokud zmacnes leve tlacitko mysi, budou se delat cihly\npokud na klavesnici w-voda, f-ohen, p-poison,\n l-levy trojuhelnik, p-pravy trojuhelnik - fialova a ruzova barva\nb-spawn fireboye, g-spawn watergirl\npotom je treba jeste do text souboru manualne dopsat f g v mistech cile fireboye a watergirl")

name = input("zadej nazev souboru ")

#pole mapy, pokud soubor neexistuje vytvoří se nový prázdný, pokud existuje otevře se pro editaci
map_array = []
if not os.path.exists(name):
    for y in range(800//25):
        row = []
        for x in range(1000//25):
            row.append(None)
        map_array.append(row)
else:
    with open(name) as f:
        for line in f.readlines():
            row = []
            for letter in line:
                if letter == " ":
                    row.append(None)
                elif letter in ("\n", "\t"):
                    pass
                else:
                    row.append(letter)
            map_array.append(row)
#okno
p.init()
width = 1000
height = 800
screen = p.display.set_mode((width, height))

#nakreslí síť
def draw_net():
    screen.fill("black")
    for i in range(800//25):
        p.draw.line(screen, "grey", (0, i*25), (1000, i*25))
    for i in range(1000//25):
        p.draw.line(screen, "grey", (i*25, 0), (i*25, 800))
    p.display.update()

#vykreslí map array
def draw_map():
    color_dict = {"P":"green", "X":"grey", "W":"blue", "F":"red", "B":(250, 100, 100), "G":(100, 100, 250), None:"black","L":"pink", "R":"purple",\
                  "f":(250, 200, 200), "w":(200, 200, 250)}
    ypos = 0
    for y in map_array:
        xpos = 0
        for x in y:
            if not x is None:
                p.draw.rect(screen, color_dict[x], p.Rect((xpos*25, ypos*25), (25, 25)))
            xpos += 1
        ypos += 1
        
draw_net()
draw_map()
running = True
#hlavní cyklus
while running:
    p.display.update()
    for event in p.event.get():
        pressed = p.mouse.get_pressed()
        key_press = p.key.get_pressed()
        key_dict = {p.K_p:"P", p.K_w:"W", p.K_f:"F", p.K_n:None, p.K_b:"B", p.K_g:"G", p.K_l:"L", p.K_r:"R"}
        color_dict = {"P":"green", "X":"grey", "W":"blue", "F":"red", "B":(250, 50, 50), "G":(50, 50, 250), None:"black","L":"pink", "R":"purple"}

        if pressed[0]:
            pos = (p.mouse.get_pos()[0]//25, p.mouse.get_pos()[1]//25)
            p.draw.rect(screen, "grey", p.Rect((pos[0]*25, pos[1]*25), (25, 25)))
            map_array[pos[1]][pos[0]] = "X"
        for key in key_dict:
            if key_press[key]:
                pos = (p.mouse.get_pos()[0]//25, p.mouse.get_pos()[1]//25)
                p.draw.rect(screen, color_dict[key_dict[key]], p.Rect((pos[0]*25, pos[1]*25), (25, 25)))
                map_array[pos[1]][pos[0]] = key_dict[key]
                if key_dict[key] is None:
                    p.draw.rect(screen, "grey", p.Rect((pos[0]*25, pos[1]*25), (25, 25)), 1)    
        if event.type == p.QUIT:
            running = False
#zapisuje map array do souboru po ukončení hlavního cyklu
with open(name, "w") as f:
    for row in map_array:
        for letter in row:
            if letter is None:
                f.write(" ")
            else:
                f.write(letter)
        f.write("\n")
            
