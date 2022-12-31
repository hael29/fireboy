import pygame as p
#pauza menu
def pausemenu(screen):
    #grafika
    retry = p.transform.scale(p.image.load("retry.png"), (200, 200))
    exit =  p.transform.scale(p.image.load("exit.png"), (200, 200))

    p.draw.rect(screen, "dark green", (200, 200, 600, 400))
    p.draw.rect(screen, "gray", (200, 200, 600, 400), 5)
    resume_button = p.draw.rect(screen, "black", (266, 300, 200, 200), 5)
    quit_button = p.draw.rect(screen, "black", (533, 300, 200, 200), 5)
    screen.blit(retry, (266, 300))
    screen.blit(exit, (533, 300))
    p.display.update()
    #zvuk
    click = p.mixer.Sound("click.wav")
    click.set_volume(0.3)
    #hlavní cyklus
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                pos = p.mouse.get_pos()
                click.play()
                if resume_button.collidepoint(pos):
                    return "level"
                if quit_button.collidepoint(pos):
                    return "levels"
            if event.type == p.QUIT:
                p.quit()
                quit()