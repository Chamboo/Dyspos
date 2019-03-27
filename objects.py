import math
import random

class Player:
    width = 64
    height = 128
    screenX = (1920 - width) / 2
    screenY = (1080 - height) / 2
    x = 960
    y = 540
    maxHealth = 100
    health = 100
    maxMana = 100
    mana = 100

    def __init__(self):
        pass


class Camera:
    x = 0
    y = 0

    def __init__(self):
        pass


class Projectile:
    width, height = 32, 32
    time = 0

    def __init__(self, playerX, playerY, clickX, clickY):
        self.x = -playerX*64 + 1920/2
        self.y = -playerY*64 + 1080/2
        diffX = clickX - self.x
        diffY = clickY - self.y
        n = 1000
        if diffX < 0:
            n *= -1
            angle = math.atan(diffY / diffX)
            self.xSpeed = (math.cos(angle)) * n
            self.ySpeed = (math.sin(angle)) * n
        elif diffX == 0:
            if diffY < 0:
                self.xSpeed = 0
                self.ySpeed = -1
            if diffY > 0:
                self.xSpeed = 0
                self.ySpeed = 1
        else:
            angle = math.atan(diffY / diffX)
            self.xSpeed = (math.cos(angle)) * n
            self.ySpeed = (math.sin(angle)) * n


class Enemy:
    width, height = 64, 64
    xSpeed, ySpeed = 0, 0
    Dcooldown = 0
    health = 10


    def __init__(self, x, y, health):
        self.maxHealth = health
        self.health = health
        self.x = x*64
        self.y = y*64
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def changeDirection(self, playerX, playerY):
        diffX = -playerX*64 + 1920/2 - self.x
        diffY = -playerY*64 + 1080/2 - self.y

        n = 80
        if (diffX**2 + diffY**2)**0.5 <= 12*64:
            if diffX < 0:
                n *= -1
                angle = math.atan(diffY / diffX)
                self.xSpeed = (math.cos(angle)) * n
                self.ySpeed = (math.sin(angle)) * n

            elif diffX == 0:
                if diffY < 0:
                    self.xSpeed = 0
                    self.ySpeed = -1
                if diffY > 0:
                    self.xSpeed = 0
                    self.ySpeed = 1
            else:
                angle = math.atan(diffY / diffX)
                self.xSpeed = (math.cos(angle)) * n
                self.ySpeed = (math.sin(angle)) * n
        else:
            self.xSpeed = 0
            self.ySpeed = 0
