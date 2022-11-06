import sys
import pygame
from pygame.locals import *
import random

from math import *

pygame.init()  # Pygame set up.

################################################## MEASURES ##################################################

(windowWidth, windowHeight) = (800, 600)
boundary = 600


mainClock = pygame.time.Clock()  # Reference to the clock.
pygame.mixer.pre_init(44100, 16, 2, 4096)  # Frequency, size, channels, buffersize.

windowSurface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN) # Main window.

font = pygame.font.SysFont("arial", 36, bold=True)
fontMinor = pygame.font.SysFont("arial", 24, bold=True)


leftBool = False
rightBool = False

posList = [0, 0, 0]
posPos = 0

letters = ["_", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X" , "Y", "Z"]
abcLen = len(letters)

speed = 0.005


def terminate():  # Ends the game
    pygame.quit()  # Closes the pygame
    sys.exit()  # Closes the programme


def waitFor(t, mode=""):
    mainClock.tick()
    counter = 0
    while counter < t:
        checkEvents(mode)
        counter += mainClock.tick()

def checkEvents(mode=""):

    global leftBool
    global rightBool
    
    for event in pygame.event.get():
        
        if event.type == QUIT: # Recognises the ESC key pressed and terminates the game.
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
                    shoot()

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
                        posList[posPos] = abcLen-1
                    else:
                        posList[posPos] -= 1
                    printLet(posPos, letters[posList[posPos]])
                elif event.key == K_DOWN:
                    if posList[posPos] == abcLen-1:
                        posList[posPos] = 0
                    else:
                        posList[posPos] += 1
                    printLet(posPos, letters[posList[posPos]])
                elif event.key == K_RETURN:
                    return False

    return True



class PolarCoord:

    def __init__(self, rho, theta):
        self.rho = rho
        self.theta = theta

    def toCartesian(self):
        return CartesianCoord(self.rho*cos(self.theta)+300,300-self.rho*sin(self.theta))


class CartesianCoord:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toPolar(self):
        return PolarCoord(sqrt(self.x*self.x+self.y*self.y), atan(self.y/self.x))

    def intX(self):
        return int(self.x)

    def intY(self):
        return int(self.y)


class Player:

    def __init__(self):
        self.reset()
        
        self.character = pygame.image.load("media/img/character.png")
        self.characterW = pygame.image.load("media/img/characterW.png")
        self.rect=self.character.get_rect()
        self.rect.center = (300,300)

    def reset(self):
        self.coord = PolarCoord(0, pi/2)
        self.lifes = 3

    def drawRotate(self):

        rot = (self.coord.theta - pi/2)/pi * 180

        img = self.character.convert().copy()
        white = pygame.transform.rotate(self.characterW.convert().copy(), rot-.1)
        r = img.get_rect()
        r.center = (300,300)

        windowSurface.blit(white, r)
        img = pygame.transform.rotate(img, rot)
        r = img.get_rect()
        r.center = (300, 300)
        windowSurface.blit(img,r)


    def turnLeft(self):
        self.coord.theta += speed
        if self.coord.theta >= 2*pi:
            self.coord.theta = .01
        self.drawRotate()

    def turnRight(self):
        self.coord.theta -= speed
        if self.coord.theta <= 0:
            self.coord.theta = 2*pi-.01
        self.drawRotate()

    def hurt(self):
        player.lifes -= 1
        printHeart(False, player.lifes)
        pygame.mixer.Sound("media/audio/hurt.wav").play()



        

bulletList = []

class Bullet:

    def __init__(self, theta):
        self.coord = PolarCoord(25, theta)
        self.img = pygame.image.load("media/img/bullet.png")
        self.imgW = pygame.image.load("media/img/bulletW.png")
        self.rect = self.img.get_rect()

        cart = self.coord.toCartesian()
        self.rect.center = (cart.x, cart.y)

        global bulletList
        bulletList.append(self)

    def erase(self):
        windowSurface.blit(self.imgW,self.rect)

    def draw(self):
        self.erase()
        
        self.coord.rho += 1
        if self.coord.rho > 298:
            global bulletList
            bulletList.remove(self)
        else:
            cart = self.coord.toCartesian()
            self.rect.center = (cart.x, cart.y)
            windowSurface.blit(self.img, self.rect)





def shoot():
    Bullet(player.coord.theta)
    pygame.mixer.Sound("media/audio/laser.wav").play()


def dist(a,b):
    (x1, x2) = (a.coord.toCartesian().x, a.coord.toCartesian().y)
    (y1, y2) = (b.coord.toCartesian().x, b.coord.toCartesian().y)
    return sqrt( (x1-y1)*(x1-y1) + (x2-y2)*(x2-y2) )


enemyList = []

class Enemy():

    def __init__(self, categ=""):
        self.categ = categ
        self.coord = PolarCoord(285, random.random()*2*pi)
        self.img = pygame.transform.rotate(pygame.image.load("media/img/enemy.png"), (self.coord.theta-pi/2)*180/pi+180)
        self.imgW = pygame.transform.rotate(pygame.image.load("media/img/enemyW.png"), (self.coord.theta-pi/2)*180/pi+180)
        self.rect = self.img.get_rect()

        cart = self.coord.toCartesian()
        self.rect.center = (cart.x, cart.y)

        global enemyList
        enemyList.append(self)

    def erase(self):
        windowSurface.blit(self.imgW,self.rect)

    def draw(self):
        self.erase()
        
        self.coord.rho -= .05
        if self.coord.rho < 25:
            player.hurt()
            global bulletList
            enemyList.remove(self)
            
        else:
            cart = self.coord.toCartesian()
            self.rect.center = (cart.x, cart.y)
            windowSurface.blit(self.img, self.rect)
        





player = Player()




heart = pygame.image.load("media/img/heart.png")
blackHeart = pygame.image.load("media/img/blackHeart.png")

heart_rect = heart.get_rect()
heart_rect.y = 50


def printHeart(isRed, i):
    img = heart if isRed else blackHeart
    if i == 0:
        heart_rect.x = 620
    elif i == 1:
        heart_rect.x = 655
    else:
        heart_rect.x = 690

    windowSurface.blit(img, heart_rect)




def printNum(n):
    textobj = font.render(str(n), 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (730, 40)
    pygame.draw.rect(windowSurface, (0, 0, 255), (730, 40, 70, 50))
    windowSurface.blit(textobj,textrect)
    pygame.display.update()


def printLet(pos, letter):
    x = 0
    if pos == 0:
        x = 300
    elif pos == 1:
        x = 330
    else:
        x = 360

    pygame.draw.rect(windowSurface, (0,0,0), (x, 340, 30, 30))
        
    textobj = fontMinor.render(letter, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, 340)
    windowSurface.blit(textobj,textrect)

    pygame.display.update()


def over(n):
    textobj = font.render("GAME OVER", 1, (0,0,0))
    textrect = textobj.get_rect()
    textrect.topleft = (190, 280)
    windowSurface.blit(textobj,textrect)
    pygame.display.update()
    pygame.mixer.Sound("media/audio/over.wav").play()

    pygame.draw.rect(windowSurface, (0,0,0), (200, 320, 200, 70))
    textobj = fontMinor.render("NAME:", 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (210, 340)
    windowSurface.blit(textobj,textrect)

    pygame.display.update()

    global posList
    posList = [0,0,0]
    posPos = 0

    printLet(0, "_")
    printLet(1, "_")
    printLet(2, "_")

    keepWaiting = True
    while keepWaiting:
        keepWaiting = checkEvents("over")

    file = open("ranking.txt", 'a')
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
                
            for b in bulletList:
                b.draw()
            for e in enemyList:
                for b in bulletList:
                    if dist(e,b) <= 10:
                        b.erase()
                        bulletList.remove(b)
                        e.erase()
                        enemyList.remove(e)
                        break
                else:
                    e.draw()

            if counter >= 1000:
                Enemy()
                counter = 0
                n = n+1
                printNum(n)
            else:
                counter += mainClock.tick()
        
            pygame.display.update()

        else:
            over(n)
            break


while True:

    enemyList.clear()

    mainClock.tick()

    pygame.draw.rect(windowSurface, (0,0,255), (boundary,0,windowWidth-boundary,windowHeight))
    pygame.draw.ellipse(windowSurface, (255,255,255), (0, 0, windowHeight, windowHeight))

    player.reset()
    player.drawRotate()

    printHeart(True, 0)
    printHeart(True, 1)
    printHeart(True, 2)

    textobj = font.render("RANKING", 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (620, 100)
    windowSurface.blit(textobj,textrect)

    file = open("ranking.txt", "r+")
    ranking = file.readlines()
    file.close()

    print(ranking)

    ranking.sort(key=lambda x: list(range(1000000)).index(int(x.split(" ")[1][:-1])), reverse=True)

    for i in range(min(10, len(ranking))):
        textobj = fontMinor.render(ranking[i][:-1], 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.topleft = (620, 150 + 30*i)
        windowSurface.blit(textobj, textrect)

    printNum(0)

    mainLoop()

terminate()
