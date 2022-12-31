import pygame as p
#menu smrti
def die(screen):
    #grafika
    deathscreen = p.transform.scale(p.image.load("deathscreen.png"), (600, 400))
    p.draw.rect(screen, "gray", (190, 190, 620, 420), 10)
    screen.blit(deathscreen, (200, 200))
    p.display.update()
    respawn_button = p.draw.rect(screen, "black", (265, 387, 480, 70), 1)
    leave_button = p.draw.rect(screen, "black", (265, 477, 480, 70), 1)
    #zvuk
    click = p.mixer.Sound("click.wav")
    click.set_volume(0.3)
    #hlavní cyklus
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                pos = p.mouse.get_pos()
                click.play()
                if respawn_button.collidepoint(pos):
                    return "level"
                if leave_button.collidepoint(pos):
                    return "levels"
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    return "levels"
            if event.type == p.QUIT:
                p.quit()
                quit()
