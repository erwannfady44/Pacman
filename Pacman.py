import pygame

from GameConfig import GameConfig


class Pacman:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.initialPosition()
        self.direction = 1

    def move(self):
        if self.possibleMove(self.direction):
            if self.direction == 0:
                self.y -= 1
            elif self.direction == 1:
                self.x -= 1
            elif self.direction == 2:
                self.y += 1
            elif self.direction == 3:
                self.x += 1


    def possibleMove(self, direction):
        if direction == 0:
            if GameConfig.imgMove.get_at((self.x, self.y - 1)) == (255, 255, 255, 255):
                return True
        elif direction == 1:
            # Si on est dans le tunel qui traverse la map
            if 300 < self.y < 320 and self.x < GameConfig.pacManW:
                self.x = 580
            elif GameConfig.imgMove.get_at((self.x - 1, self.y)) == (255, 255, 255, 255):
                return True
        elif direction == 3:
            # Si on est dans le tunel qui traverse la map
            if 300 < self.y < 320 and self.x > 570:
                self.x = 5
            elif GameConfig.imgMove.get_at((self.x + 1, self.y)) == (255, 255, 255, 255):
                return True
        elif direction == 2:
            if GameConfig.imgMove.get_at((self.x, self.y + 1)) == (255, 255, 255, 255):
                return True

    def initialPosition(self):
        self.x = 297
        self.y = 497

    def setDirection(self, direction):
        self.direction = direction