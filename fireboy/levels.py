import pygame as p
#menu s levely
def levels_menu(screen):
    class Level:
        def __init__(self, x, y, size, width, num, rect, completed, file):
            self.x = x
            self.y = y
            self.size = size
            self.width = width
            self.num = num
            self.rect = rect
            self.completed = completed
            self.file = file
        #vykreslí levely
        def draw(self):
            p.draw.rect(screen, "green", (self.x, self.y, self.size, self.size))
            self.rect = p.draw.rect(screen, "black", (self.x, self.y, self.size, self.size), self.width)
            screen.blit(font.render(str(self.num), True, "black"), (self.x + 10 + (self.size - fontsize)//2, self.y + (self.size - fontsize)//2))
    
    #grafika
    screen.fill("dark green")
    fontsize = 60
    font = p.font.SysFont('bookantiquatučnékurzíva', fontsize)
    levels_text = font.render("Levels", True, "black")
    border = p.transform.scale(p.image.load("border.png"), (1000, 800))
    ud_border = p.transform.rotate(border, 180)
    screen.blit(border, (0, -100))
    screen.blit(ud_border, (0, 100))
    screen.blit(levels_text, (425, 50))
    #zvuky
    click = p.mixer.Sound("click.wav")
    click.set_volume(0.3)
    #vykreslí levely
    levels = []
    y = 175
    a = 0
    for i in range(2):
        x = 25
        for o in range(1,6):
            level = Level(x, y, 150, 5, o+a*5, None, False, f"level_{o+a*5}.txt")
            x += 200
            level.draw()
            levels.append(level)
        y += 300
        a += 1


    p.display.update()
    #hlavní cyklus
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                pos = p.mouse.get_pos()
                click.play()
                for level in levels:
                    if level.rect.collidepoint(pos):
                        return "level", level.file
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    return "main_menu", None
            if event.type == p.QUIT:
                p.quit()
                quit()
