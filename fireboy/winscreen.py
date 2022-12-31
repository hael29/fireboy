import pygame as p
#menu vítězné
def win(screen):
    #grafika
    font = p.font.SysFont('bookantiquatučnékurzíva', 73)
    font_smaller = p.font.SysFont('bookantiquatučnékurzíva', 40)
    win_text = font.render("Level complete!", True, "black")
    continue_text = font_smaller.render("Continue", True, "black")
    corner = p.transform.scale(p.image.load("corner.png"), (220, 220))
    bell = p.transform.rotate(p.transform.scale(p.image.load("bell.png"), (150, 150)), -25)

    p.draw.rect(screen, "dark green", (200, 200, 600, 400))
    p.draw.rect(screen, "gray", (200, 200, 600, 400), 5)
    p.draw.rect(screen, "green", (300, 425, 400, 100))
    continue_button = p.draw.rect(screen, "black", (300, 425, 400, 100), 5)
    
    screen.blit(win_text, (250, 300))
    screen.blit(continue_text, (425, 455))
    screen.blit(corner, (200, 200))
    screen.blit(bell, (650, 150))


    p.display.update()
    #Mi música no discrimina a nadie Así que vamo' a romper
    click = p.mixer.Sound("click.wav")
    click.set_volume(0.3)
    woo = p.mixer.Sound("trumpets.wav")
    woo.set_volume(0.25)
    woo.play()
    #hlavní cyklus
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                click.play()
                pos = p.mouse.get_pos()
                if continue_button.collidepoint(pos):
                    return "levels"
            if event.type == p.QUIT:
                p.quit()
                quit()