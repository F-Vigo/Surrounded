import pygame
from pygame.locals import *

pygame.init()  # Pygame set up.

from src.classes import *
from src.functions import *


##### VARIABLES #####

(windowWidth, windowHeight) = (800, 600)
boundary = 600

mainClock = pygame.time.Clock()  # Reference to the clock.
pygame.mixer.pre_init(44100, 16, 2, 4096)  # Frequency, size, channels, buffersize.

windowSurface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)  # Main window.

font = pygame.font.SysFont("arial", 36, bold=True)
fontMinor = pygame.font.SysFont("arial", 24, bold=True)

leftBool = False
rightBool = False

posList = [0, 0, 0]
posPos = 0

letters = ["_", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
           "V", "W", "X", "Y", "Z"]
abcLen = len(letters)

player = Player(windowSurface)

heart = pygame.image.load("../media/img/heart.png")
blackHeart = pygame.image.load("../media/img/blackHeart.png")

heart_rect = heart.get_rect()
heart_rect.y = 50

bulletList = SurroundedList()
enemyList = SurroundedList()



##### AUX #####
def createBullet(theta):
    Bullet(theta, bulletList, windowSurface)






##### MAIN FUNCTIONS #####

def checkEvents(mode=""):
    global leftBool
    global rightBool

    for event in pygame.event.get():

        if event.type == QUIT:  # Recognises the ESC key pressed and terminates the game.
            terminate()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()

        if mode == "play":

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    leftBool = False
                elif event.key == K_RIGHT:
                    rightBool = False
                elif event.key == K_SPACE:
                    shoot(createBullet, player)

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    leftBool = True
                elif event.key == K_RIGHT:
                    rightBool = True

        elif mode == "over":
            global posPos
            if event.type == KEYUP:
                if event.key == K_LEFT and posPos > 0:
                    posPos -= 1
                elif event.key == K_RIGHT and posPos < 2:
                    posPos += 1
                elif event.key == K_UP:
                    if posList[posPos] == 0:
                        posList[posPos] = abcLen - 1
                    else:
                        posList[posPos] -= 1
                    printLet(posPos, letters[posList[posPos]], windowSurface, fontMinor)
                elif event.key == K_DOWN:
                    if posList[posPos] == abcLen - 1:
                        posList[posPos] = 0
                    else:
                        posList[posPos] += 1
                    printLet(posPos, letters[posList[posPos]], windowSurface, fontMinor)
                elif event.key == K_RETURN:
                    return False

    return True






def over(n, windowSurface, fontMinor):
    textobj = font.render("GAME OVER", 1, (0, 0, 0))
    textrect = textobj.get_rect()
    textrect.topleft = (190, 280)
    windowSurface.blit(textobj, textrect)
    pygame.display.update()
    pygame.mixer.Sound("../media/audio/over.wav").play()

    pygame.draw.rect(windowSurface, (0, 0, 0), (200, 320, 200, 70))
    textobj = fontMinor.render("NAME:", 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (210, 340)
    windowSurface.blit(textobj, textrect)

    pygame.display.update()

    global posList
    posList = [0, 0, 0]
    global posPos
    posPos = 0

    printLet(0, "_", windowSurface, fontMinor)
    printLet(1, "_", windowSurface, fontMinor)
    printLet(2, "_", windowSurface, fontMinor)

    keepWaiting = True
    while keepWaiting:
        keepWaiting = checkEvents("over")

    file = open("../ranking.txt", 'a')
    file.write(
        letters[posList[0]] +
        letters[posList[1]] +
        letters[posList[2]] +
        " " + str(n) + "\n"
    )
    file.close()


def mainLoop():
    counter = 0
    n = 0

    while True:
        if player.lifes > 0:
            checkEvents("play")

            if leftBool:
                player.turnLeft()
            elif rightBool:
                player.turnRight()

            for b in bulletList.list:
                b.draw(bulletList)
            for e in enemyList.list:
                for b in bulletList.list:
                    if dist(e, b) <= 10:
                        b.erase()
                        bulletList.remove(b)
                        e.erase()
                        enemyList.remove(e)
                        break
                else:
                    e.draw(player, enemyList, printHeart, heart, blackHeart, heart_rect, windowSurface)

            if counter >= 1000:
                Enemy(windowSurface, enemyList)
                counter = 0
                n = n + 1
                printNum(n, font, windowSurface)
            else:
                counter += mainClock.tick()

            pygame.display.update()

        else:
            over(n, windowSurface, fontMinor)
            break


while True:

    enemyList.clear()

    mainClock.tick()

    pygame.draw.rect(windowSurface, (0, 0, 255), (boundary, 0, windowWidth - boundary, windowHeight))
    pygame.draw.ellipse(windowSurface, (255, 255, 255), (0, 0, windowHeight, windowHeight))

    player.reset()
    player.drawRotate()

    printHeart(True, 0, heart, blackHeart, heart_rect, windowSurface)
    printHeart(True, 1, heart, blackHeart, heart_rect, windowSurface)
    printHeart(True, 2, heart, blackHeart, heart_rect, windowSurface)

    textobj = font.render("RANKING", 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (620, 100)
    windowSurface.blit(textobj, textrect)

    file = open("../ranking.txt", "r+")
    ranking = file.readlines()
    file.close()

    ranking.sort(key=lambda x: list(range(1000000)).index(int(x.split(" ")[1][:-1])), reverse=True)

    for i in range(min(10, len(ranking))):
        textobj = fontMinor.render(ranking[i][:-1], 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.topleft = (620, 150 + 30 * i)
        windowSurface.blit(textobj, textrect)

    printNum(0, font, windowSurface)

    mainLoop()

terminate()