from math import *
import random

import pygame



##### COORDINATES #####

class PolarCoord:

    def __init__(self, rho, theta):
        self.rho = rho
        self.theta = theta

    def toCartesian(self):
        return CartesianCoord(self.rho * cos(self.theta) + 300, 300 - self.rho * sin(self.theta))


class CartesianCoord:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toPolar(self):
        return PolarCoord(sqrt(self.x * self.x + self.y * self.y), atan(self.y / self.x))

    def intX(self):
        return int(self.x)

    def intY(self):
        return int(self.y)


##### OTHERS #####

# Bullet list
# Enemy list
class SurroundedList:
    def __init__(self):
        self.list = []

    def append(self, x):
        self.list.append(x)

    def clear(self):
        self.list.clear()

    def remove(self, x):
        self.list.remove(x)


class Player:

    def __init__(self, windowSurface):
        self.reset()
        self.windowSurface = windowSurface
        self.speed = 0.005

        self.character = pygame.image.load("../media/img/character.png")
        self.characterW = pygame.image.load("../media/img/characterW.png")
        self.rect = self.character.get_rect()
        self.rect.center = (300, 300)

    def reset(self):
        self.coord = PolarCoord(0, pi / 2)
        self.lifes = 3

    def drawRotate(self):

        rot = (self.coord.theta - pi / 2) / pi * 180

        img = self.character.convert().copy()
        white = pygame.transform.rotate(self.characterW.convert().copy(), rot - .1)
        r = img.get_rect()
        r.center = (300, 300)

        self.windowSurface.blit(white, r)
        img = pygame.transform.rotate(img, rot)
        r = img.get_rect()
        r.center = (300, 300)
        self.windowSurface.blit(img, r)

    def turnLeft(self):
        self.coord.theta += self.speed
        if self.coord.theta >= 2 * pi:
            self.coord.theta = .01
        self.drawRotate()

    def turnRight(self):
        self.coord.theta -= self.speed
        if self.coord.theta <= 0:
            self.coord.theta = 2 * pi - .01
        self.drawRotate()

    def hurt(self, printHeart, heart, blackHeart, heart_rect, windowSurface):
        self.lifes -= 1
        printHeart(False, self.lifes, heart, blackHeart, heart_rect, windowSurface)
        pygame.mixer.Sound("../media/audio/hurt.wav").play()


class Bullet:

    def __init__(self, theta, bulletList, windowSurface):

        self.windowSurface = windowSurface
        self.coord = PolarCoord(25, theta)
        self.img = pygame.image.load("../media/img/bullet.png")
        self.imgW = pygame.image.load("../media/img/bulletW.png")
        self.rect = self.img.get_rect()

        cart = self.coord.toCartesian()
        self.rect.center = (cart.x, cart.y)

        bulletList.append(self)

    def erase(self):
        self.windowSurface.blit(self.imgW, self.rect)

    def draw(self, bulletList):

        self.erase()
        self.coord.rho += 1

        if self.coord.rho > 298:
            bulletList.remove(self)
        else:
            cart = self.coord.toCartesian()
            self.rect.center = (cart.x, cart.y)
            self.windowSurface.blit(self.img, self.rect)


class Enemy():

    def __init__(self, windowSurface, enemyList, categ=""):
        self.categ = categ
        self.windowSurface = windowSurface
        self.coord = PolarCoord(285, random.random() * 2 * pi)
        self.img = pygame.transform.rotate(
            pygame.image.load("../media/img/enemy.png"),
            (self.coord.theta - pi / 2) * 180 / pi + 180
        )
        self.imgW = pygame.transform.rotate(
            pygame.image.load("../media/img/enemyW.png"),
            (self.coord.theta - pi / 2) * 180 / pi + 180
        )
        self.rect = self.img.get_rect()
        cart = self.coord.toCartesian()
        self.rect.center = (cart.x, cart.y)
        enemyList.append(self)

    def erase(self):
        self.windowSurface.blit(self.imgW, self.rect)

    def draw(self, player, enemyList, printHeart, heart, blackHeart, heart_rect, windowSurface):

        self.erase()
        self.coord.rho -= .05

        if self.coord.rho < 25:
            player.hurt(printHeart, heart, blackHeart, heart_rect, windowSurface)
            enemyList.remove(self)
        else:
            cart = self.coord.toCartesian()
            self.rect.center = (cart.x, cart.y)
            self.windowSurface.blit(self.img, self.rect)
