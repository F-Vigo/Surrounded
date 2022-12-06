import sys
from math import sqrt

import pygame

##### GENERAL #####

def terminate():  # Ends the game
    pygame.quit()  # Closes the pygame
    sys.exit()  # Closes the programme

def waitFor(t, mainClock, checkEvents, mode=""):
    mainClock.tick()
    counter = 0
    while counter < t:
        checkEvents(mode)
        counter += mainClock.tick()

def shoot(createBullet, player):
    createBullet(player.coord.theta)
    pygame.mixer.Sound("../media/audio/laser.wav").play()

def dist(a, b):
    (x1, x2) = (a.coord.toCartesian().x, a.coord.toCartesian().y)
    (y1, y2) = (b.coord.toCartesian().x, b.coord.toCartesian().y)
    return sqrt((x1 - y1) * (x1 - y1) + (x2 - y2) * (x2 - y2))



##### PRINTING #####

def printHeart(isRed, i, heart, blackHeart, heart_rect, windowSurface):
    img = heart if isRed else blackHeart
    if i == 0:
        heart_rect.x = 620
    elif i == 1:
        heart_rect.x = 655
    else:
        heart_rect.x = 690
    windowSurface.blit(img, heart_rect)


def printNum(n, font, windowSurface):
    textobj = font.render(str(n), 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (730, 40)
    pygame.draw.rect(windowSurface, (0, 0, 255), (730, 40, 70, 50))
    windowSurface.blit(textobj, textrect)
    pygame.display.update()


def printLet(pos, letter, windowSurface, fontMinor):
    x = 0
    if pos == 0:
        x = 300
    elif pos == 1:
        x = 330
    else:
        x = 360

    pygame.draw.rect(windowSurface, (0, 0, 0), (x, 340, 30, 30))

    textobj = fontMinor.render(letter, 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, 340)
    windowSurface.blit(textobj, textrect)

    pygame.display.update()
