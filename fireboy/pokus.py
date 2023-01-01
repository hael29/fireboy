#import knihoven a funkcí z ostatních souborů
import pygame as p
import math as m
from levels import levels_menu
from main_menu import main_menu
from deathscreen import die
from winscreen import win
from why import pausemenu

#definice okna
p.init()
width = 1000
height = 800
screen = p.display.set_mode((width, height))
p.display.set_caption("Fireboy & Watergirl")
menu = "main_menu"

#pomocné funkce pro kolizi bodu a trojúhelníků
def distance(point_a, point_b):
    a = abs(point_a[0] - point_b[0])
    b = abs(point_a[1] - point_b[1])
    return m.sqrt(a**2 + b**2)

def area(triangle):
    a = distance(triangle[0], triangle[1])
    b = distance(triangle[1], triangle[2])
    c = distance(triangle[0], triangle[2])
    s = (a + b + c)/2
    area = m.sqrt(s*(s-a)*(s-b)*(s-c))
    return area

def triangle_collision(point, triangle):
    area_1 = area((point, triangle[0], triangle[1]))
    area_2 = area((point, triangle[1], triangle[2]))
    area_3 = area((point, triangle[0], triangle[2]))
    area_total = area(triangle)
    return area_total-5 < (area_1 + area_2 + area_3) < area_total+5


#třída Cihla
class Brick:
    size = 25
    def __init__(self, width, pos, typ):
        self.width = width
        self.pos = pos
        self.type = typ

    def real_pos(self):
        return (self.pos[0]*self.size, self.pos[1]*self.size)


class Map:
    #načte mapu z text souboru, vrátí pole cihel
    def __init__(self, name):
        with open(name, "r") as f:
            map_array = []
            line_num = 0
            for line in f.readlines():
                row = []
                letter_num = 0
                prev_letter = None
                prev_brick = None
                for letter in line:
                    if letter in (" ", "\n", "\t"):
                        pass
                    elif prev_letter == letter:
                        prev_brick.width += 1
                    else:
                        type_dict = {"X":"brick", "W":"water", "F":"fire", "P":"poison", "L":"brick_left", "R":"brick_right",\
                                     "B":"f_spawn", "G":"w_spawn", "w":"w_portal", "f":"f_portal", "D":"door", "d":"button"}
                        brick = Brick(1, (letter_num, line_num), type_dict[letter])
                        row.append(brick)
                        prev_brick = brick
                    prev_letter = letter
                    letter_num += 1
                map_array.append(row)
                line_num += 1
        self.array = map_array
    #nakreslí mapu
    def draw_map(self):
        color_dict = {"poison":"green", "fire":"red", "water":"blue", "brick":"grey", "brick_left":"grey", "brick_right":"grey", \
                      "f_spawn":(250, 100, 100), "w_spawn":(100, 100, 250), "w_portal":(200, 200, 255), "f_portal":(255, 200, 200),\
                      "door":"brown", "button":"gold"}
        for line in self.array:
            index = 0
            for brick in line:
                if brick.type in ("poison", "fire", "water", "brick", "f_spawn", "w_spawn"):
                    brick_rect = p.Rect(brick.real_pos(), (brick.width*brick.size, brick.size))
                    p.draw.rect(screen,color_dict[brick.type], brick_rect)

                elif brick.type in ("f_portal", "w_portal"):
                    brick_rect = p.Rect(brick.real_pos(), (4*brick.size/5, brick.size))
                    p.draw.ellipse(screen, color_dict[brick.type],brick_rect)
                    
                elif brick.type == "brick_right":
                    p.draw.polygon(screen, color_dict[brick.type],\
                                   (brick.real_pos(), (brick.real_pos()[0], brick.real_pos()[1] + brick.size), (brick.real_pos()[0] + brick.size*brick.width, brick.real_pos()[1] + brick.size)))
                    next_brick = line[index+1]
                    if next_brick.type in ("poison", "fire", "water"):
                        p.draw.polygon(screen, color_dict[next_brick.type],\
                                   (brick.real_pos(), (brick.real_pos()[0]+brick.size*brick.width, brick.real_pos()[1]), (brick.real_pos()[0] + brick.size*brick.width, brick.real_pos()[1] + brick.size)))
                elif brick.type == "brick_left":
                    p.draw.polygon(screen, color_dict[brick.type],\
                                   ((brick.real_pos()[0], brick.real_pos()[1]+brick.size), (brick.real_pos()[0] + brick.size*brick.width, brick.real_pos()[1]+brick.size), (brick.real_pos()[0]+brick.size*brick.width, brick.real_pos()[1])))
                    prev_brick = line[index-1]
                    if prev_brick.type in ("poison", "fire", "water"):
                        p.draw.polygon(screen, color_dict[prev_brick.type],\
                                   (brick.real_pos(), (brick.real_pos()[0], brick.real_pos()[1]+brick.size), (brick.real_pos()[0] + brick.size*brick.width, brick.real_pos()[1])))
                index += 1
    #vrátí jestli je na dané souřadnici cihla nebo ne
    def brick_on_pos(self, pos):
        fake_pos = (pos[0]//25, pos[1]//25)
        index = 0
        for brick in self.array[fake_pos[1]]:
            if brick.pos[0] <= fake_pos[0] <= brick.pos[0]+brick.width-1:
                if brick.type in ("poison", "fire", "water", "brick"):
                    return brick
                if brick.type == "brick_right":
                    next_brick = self.array[fake_pos[1]][index+1]
                    if triangle_collision(pos, \
                            (brick.real_pos(),(brick.real_pos()[0], brick.real_pos()[1]+brick.size), (brick.real_pos()[0]+brick.width*brick.size, brick.real_pos()[1]+brick.size))):
                        return brick
                    if next_brick.type in ("water", "poison", "fire"):
                        return next_brick
                if brick.type == "brick_left":
                    prev_brick = self.array[fake_pos[1]][index-1]
                    if not triangle_collision(pos, \
                            (brick.real_pos(), (brick.real_pos()[0]+brick.width*brick.size, brick.real_pos()[1]), (brick.real_pos()[0], brick.real_pos()[1]+brick.size))):
                        return brick
                    if prev_brick.type in ("water", "poison", "fire"):
                        return prev_brick
            index += 1
        return False
#třída Hráčí
class Players:
    def __init__(self, width, height, x, y, x_speed, floatnum, fallnum, img, jumping, bool, name):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.floatnum = floatnum
        self.fallnum = fallnum
        self.img = img
        self.jumping = jumping
        self.bool = bool
        self.name = name
    #pohyb hráče
    def move(self, dir):
        point1 = mapa.brick_on_pos((self.x + self.width , self.y + self.height-10))
        point2 = mapa.brick_on_pos((self.x + self.width , self.y + self.height//2))
        point3 = mapa.brick_on_pos((self.x + self.width, self.y))
        
        point4 = mapa.brick_on_pos((self.x, self.y + self.height-10))
        point5 = mapa.brick_on_pos((self.x, self.y + self.height//2))
        point6 = mapa.brick_on_pos((self.x, self.y))

        if dir == "right":
            if (not point1 or point1.type in ("water", "fire", "poison"))\
               and (not point2 or point2.type in ("water", "fire", "poison"))\
               and (not point3 or point3.type in ("water", "fire", "poison")):
                self.x += self.x_speed

        else:
            if (not point4 or point4.type in ("water", "fire", "poison"))\
               and (not point5 or point5.type in ("water", "fire", "poison"))\
               and (not point6 or point6.type in ("water", "fire", "poison")):
                self.x -= self.x_speed

    #je hráč ve vzduchu?
    def inair(self):
        brick = mapa.brick_on_pos((self.x + self.width//2, (self.y + self.height)))
        if brick is False:
            return False
        if brick.type in ("water", "poison", "fire"):
            return False
        return mapa.brick_on_pos((self.x + self.width//2, (self.y + self.height))) 
    #má hráč cihlu nad hlavou?
    def above(self):
        return mapa.brick_on_pos((self.x + self.width//2, self.y))
    #padání hráče
    def fall(self):
        if self.y < height - self.height:
            self.y += self.fallnum
        if self.fallnum < 10:
            self.fallnum += 1
    #skok nahoru (hráče)
    def float(self):
        self.y -= self.floatnum
        if self.floatnum > 0:
            self.floatnum -= 1
#definice proměnných pro hru nezbytných
mapa = Map("level_1.txt")

for line in mapa.array:
    for brick in line:
        if brick.type == "f_spawn":
            f_spawn = brick.real_pos()
        elif brick.type == "w_spawn":
            w_spawn = brick.real_pos()
        elif brick.type == "w_portal":
            w_portal = brick.real_pos()
        elif brick.type == "f_portal":
            f_portal = brick.real_pos()

fireboy_img = p.image.load("fireboy.png")
fireboy = Players(32, 45, f_spawn[0], f_spawn[1], 5, 14, 0, fireboy_img, False, False, "fireboy")
fireboy_img = p.transform.scale(fireboy_img, (fireboy.width, fireboy.height))

watergirl_img = p.image.load("watergirl.png")
watergirl = Players(30, 45, w_spawn[0], w_spawn[1], 5, 14, 0, watergirl_img, False, False, "watergirl")
watergirl_img = p.transform.scale(watergirl_img, (watergirl.width, watergirl.height))

game =  True
level = "level_1.txt"

fireboy_left = p.transform.scale(p.image.load("fireboy left.png"), (fireboy.width, fireboy.height))
fireboy_right = p.transform.scale(p.image.load("fireboy right.png"), (fireboy.width, fireboy.height))

watergirl_left = p.transform.scale(p.image.load("watergirl left.png"), (watergirl.width, watergirl.height))
watergirl_right = p.transform.scale(p.image.load("watergirl right.png"), (watergirl.width, watergirl.height))
deathscreen = p.transform.scale(p.image.load("deathscreen.png"), (600, 400))

#zvuky
oof = p.mixer.Sound("roblox.wav")
click = p.mixer.Sound("click.wav")
click.set_volume(0.3)

#pohyb doleva doprava
def left_right(pressed, character):
    dic = {"fireboy":{"keys":(p.K_a, p.K_d),"imgs":(fireboy_img, fireboy_left, fireboy_right)}, "watergirl":{"keys":(p.K_LEFT, p.K_RIGHT), "imgs":(watergirl_img, watergirl_left, watergirl_right)}}
    if pressed[dic[character.name]["keys"][0]]: 
        character.move("left")
        character.img = dic[character.name]["imgs"][1]
    elif pressed[dic[character.name]["keys"][1]]:
        character.move("right")
        character.img = dic[character.name]["imgs"][2]
    else: 
        character.img = dic[character.name]["imgs"][0]
#pohyb nahoru dolu
def up_down(pressed, character):
    dic = {"fireboy":p.K_w, "watergirl":p.K_UP}
    if pressed[dic[character.name]] and character.jumping is False and character.bool  is False:
        character.jumping = True
                
    if character.jumping is True:
        if character.floatnum > 0:
            character.float() 
        else:
            character.fall() 
            
    if character.inair() is False and character.jumping is False:
        character.fall()
        character.bool = True

    if character.inair() is not False:
        character.floatnum = 14
        character.fallnum = 0
        character.jumping = False
        character.bool = False
        
    if character.above() is not False:
        character.floatnum = 0
def draw_pause():
    pause_menu = p.draw.rect(screen, "gray", (925, 0, 75, 75))
    p.draw.rect(screen, "brown", (925, 0, 75, 75), 5)
    p.draw.line(screen, "black", (950, 15), (950, 60), 20)
    p.draw.line(screen, "black", (975, 15), (975, 60), 20)
    return pause_menu
#zatemnění části obrazovky
def darkmode():
    size = 100
    rect_array = []
    if fireboy.y < watergirl.y:
        rect = p.Rect((0,0), (width, fireboy.y-size))
        rect2 = p.Rect((0, watergirl.y+size), (width, height-watergirl.y-size))
    else:
        rect = p.Rect((0,0), (width, watergirl.y-size))
        rect2 = p.Rect((0, fireboy.y+size), (width, height-fireboy.y-size))
    rect_array.append(rect)
    rect_array.append(rect2)
    if fireboy.x < watergirl.x:
        rect = p.Rect((0,0), (fireboy.x-size, height))
        rect2 = p.Rect((watergirl.x+size, 0), (width-watergirl.x-size, height))
    else:
        rect = p.Rect((0,0), (watergirl.x-size, height))
        rect2 = p.Rect((fireboy.x+size,0), (width-fireboy.x-size, height))
    rect_array.append(rect)
    rect_array.append(rect2)
    for rect in rect_array:
        p.draw.rect(screen, "black", rect)

#hlavní cyklus
while True:
    p.display.update()

    #vykreslování věcí na obrazovku
    screen.fill("black")
    mapa.draw_map()

    if level is not None and int(level[6]) >= 6:
        darkmode()
    screen.blit(fireboy.img, (fireboy.x, fireboy.y))
    screen.blit(watergirl.img, (watergirl.x, watergirl.y))

    pause_menu = draw_pause()
    #ovládání postav klávesnicí
    pressed = p.key.get_pressed()
    up_down(pressed, fireboy)
    up_down(pressed, watergirl)
    left_right(pressed, fireboy)
    left_right(pressed, watergirl)

    #kontrola smrti postav
    brick_f = mapa.brick_on_pos((fireboy.x + fireboy.width//2, fireboy.y + fireboy.height))
    brick_w = mapa.brick_on_pos((watergirl.x + watergirl.width//2, watergirl.y + watergirl.height))
        
    if brick_f is not False:
        if brick_f.type in ("poison", "water"):
            oof.play()
            menu = die(screen)
    if brick_w is not False:
        if brick_w.type in ("poison", "fire"):
            oof.play()
            menu = die(screen)
                
    #kontrola vítězství
    if (f_portal[0]-12 < (fireboy.x+fireboy.width//2) < f_portal[0]+12 and f_portal[1]-12 < (fireboy.y+fireboy.height//2) < f_portal[1]+12) and \
         (w_portal[0]-12 < (watergirl.x+watergirl.width//2) < w_portal[0]+12 and w_portal[1]-12 < (watergirl.y+watergirl.height//2) < w_portal[1]+12):
        menu = "win"
        fireboy = Players(32, 45, f_spawn[0], f_spawn[1], 5, 14, 0, fireboy_img, False, False, "fireboy") 
        watergirl = Players(30, 45, w_spawn[0], w_spawn[1], 5, 14, 0, watergirl_img, False, False, "watergirl")
        
    #zařizuje aby hra běžela na 60 snímcích za sekundu 
    p.time.Clock().tick(60)

    #pohyb mezi menu
    for event in p.event.get():
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            pos = p.mouse.get_pos()
            click.play()
            if pause_menu.collidepoint(pos):
                menu = "pause"                
        if event.type == p.QUIT: #unkončení hry
            p.quit()
            quit()
        if event.type == p.KEYDOWN: 
            if event.key == p.K_ESCAPE:
                menu = "levels"
                print("entered the levels menu")
    if menu == "levels":
        menu, level = levels_menu(screen)
    elif menu == "main_menu":
        menu = main_menu(screen)
    elif menu == "win":
        menu = win(screen)
    elif menu == "pause":
        menu = pausemenu(screen)
    elif menu == "level":
        menu = None
        mapa = Map(level)
        for line in mapa.array: #definování nových proměnných
            for brick in line:
                if brick.type == "f_spawn":
                    f_spawn = brick.real_pos()
                elif brick.type == "w_spawn":
                    w_spawn = brick.real_pos()
                elif brick.type == "w_portal":
                    w_portal = brick.real_pos()
                elif brick.type == "f_portal":
                    f_portal = brick.real_pos()

        fireboy = Players(32, 45, f_spawn[0], f_spawn[1], 5, 14, 0, fireboy_img, False, False, "fireboy")
        watergirl = Players(30, 45, w_spawn[0], w_spawn[1], 5, 14, 0, watergirl_img, False, False, "watergirl")


    
    
         

    
