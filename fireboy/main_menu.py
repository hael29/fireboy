import pygame as p
#menu hlavního menu
def main_menu(screen):
    x1 = 200
    y1 = 400
    xsize = 200
    ysize = 200

    x2 = 600
    y2 = 400
    #grafika
    font2 = p.font.SysFont('bookantiquatučnékurzíva', 80)
    font = p.font.Font('freesansbold.ttf', 32)
    quit_text = font.render("quit", True, "black")
    screen.fill("dark green")
    p.draw.rect(screen, "green", (x1, y1, xsize, ysize))
    fireboy_text = font2.render("Fireboy", True, "orange")
    watergirl_text = font2.render("Watergirl", True, "blue")
    and_text = font2.render("&", True, "black")
    play_button = p.draw.rect(screen, "black", (x1, y1, xsize, ysize), 4)
    p.draw.polygon(screen, "black", [(x1 + 0.2*xsize, y1 + 0.2*ysize), (x1 + 0.2*xsize, y1 + 0.8*ysize), (x1 + 0.8*xsize, y1 + 0.5*ysize)])
    p.draw.rect(screen, "green", (x2, y2, xsize, ysize))    
    quit_button = p.draw.rect(screen, "black", (x2, y2, xsize, ysize), 4)
    watergirl = p.transform.rotate(p.image.load("watergirl.png"), 25)
    fireboy = p.transform.scale(p.transform.rotate(p.image.load("fireboy.png"), -20), (350, 550))
    border = p.transform.scale(p.image.load("border.png"), (1000, 800))

    screen.blit(quit_text, (x2 -32 + xsize/2, y2 + (ysize - 32)/2))
    screen.blit(fireboy_text, (150, 125))
    screen.blit(watergirl_text, (575, 225))
    screen.blit(and_text, (475, 175))
    screen.blit(watergirl, (700, 400))
    screen.blit(fireboy, (-100, 450))
    screen.blit(border, (0, -100))
    #zvuky
    click = p.mixer.Sound("click.wav")
    click.set_volume(0.3)

    p.display.update()
    #hlavní cyklus
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                pos = p.mouse.get_pos()
                click.play()
                if play_button.collidepoint(pos):
                    return "levels"
                if quit_button.collidepoint(pos):
                    p.quit()
                    quit()
            if event.type == p.QUIT:
                p.quit()
                quit()