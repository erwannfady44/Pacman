from datetime import datetime, time
from time import sleep, time

import pygame
from Dot import Dot
from GameConfig import GameConfig, getGhostImg
from Ghost import Ghost
from Pacman import Pacman


class Game:
    def __init__(self):
        self.pacman = Pacman()
        blinky = Ghost("blinky", self.pacman, None)

        self.ghosts = [blinky, Ghost("pinky", self.pacman, None), Ghost("clyde", self.pacman, None), Ghost("inky", self.pacman, blinky)]
        #self.ghosts = [Ghost("clyde", self.pacman, None)]
        self.dots = []
        self.allDotsView = pygame.Surface((GameConfig.windowW, GameConfig.windowH))
        self.allDotsView.set_colorkey((0, 0, 0))
        self.dotsView = []
        self.initDots()
        self.gameOver = False
        self.life = 2
        self.level = 0
        self.score = 0
        self.date = time()
        self.stateDate = time()
        self.mode = 2

    def nextState(self):
        self.pacman.move()
        self.checkEatDot()
        self.moveGhost()

        if self.mode == 1 and (time() - self.stateDate) > 20.0:
            self.mode = 2
            for ghost in self.ghosts:
                ghost.scatterMode()
            self.stateDate = time()
        elif self.mode == 2 and (time() - self.stateDate) > 7.0:
            self.mode = 1
            for ghost in self.ghosts:
                ghost.chaseMode()
            self.stateDate = time()


    def initDots(self):
        y = 35

        while y < 630:
            x = 35
            i = 0
            if y != 35:
                i = round((y - 35) / 21)
            self.dots.append([])
            self.dotsView.append(pygame.Surface((GameConfig.mapSizeW, 21)))
            self.dotsView[i].set_colorkey((0, 0, 0))
            while x < 580:
                if GameConfig.imgDots.get_at((x, y)) == (255, 255, 255, 255):
                    if (x == 35 and y == 77) or (x == 560 and y == 77) or (x == 35 and y == 497) or (
                            x == 560 and y == 497):
                        self.dots[i].append(Dot(x, y, 1))
                    else:
                        self.dots[i].append(Dot(x, y, 0))
                x += 21
            self.drawDots(i)
            y += 21
        self.drawAllDots()

    def drawDots(self, i):
        self.dotsView[i].fill((0, 0, 0))
        for dot in self.dots[i]:
            if dot.value == 0:
                img = GameConfig.imgDot
                self.dotsView[i].blit(img, (dot.x, 0))
            else:
                img = GameConfig.imgBigDot
                self.dotsView[i].blit(img, (dot.x - 8,  - 8))



    def drawAllDots(self):
        i = 0
        self.allDotsView.fill((0, 0, 0))
        for dotView in self.dotsView:
            self.allDotsView.blit(dotView, (GameConfig.mapStartW, GameConfig.mapStartH + 35 + i * 21))
            i += 1

    def draw(self, window):
        window.fill(GameConfig.background)
        window.blit(GameConfig.imgMap, (GameConfig.mapStartW, GameConfig.mapStartH))
        window.blit(self.allDotsView, (0, 0))

        # Affichage Pac Man
        every: int = 270000  # Temps entre chaque fois que pacMan ferme la bouche en micro secondes
        duree = 200000  # durée pendant laquelle pacMan ferme sa bouche en micro secondes
        millis = datetime.now().microsecond
        currentPacManImage = GameConfig.imgPacMan
        if self.pacman.possibleMove(self.pacman.direction) and millis % every >= every - 1 * duree / 5:
            currentPacManImage = GameConfig.imgPacMan_state_2
        elif self.pacman.possibleMove(
                self.pacman.direction) and millis % every >= every - 2 * duree / 5:
            currentPacManImage = GameConfig.imgPacMan_state_3
        elif self.pacman.possibleMove(
                self.pacman.direction) and millis % every >= every - 3 * duree / 5:  # bouche fermée
            currentPacManImage = GameConfig.imgPacManClose
        elif self.pacman.possibleMove(self.pacman.direction) and millis % every >= every - 4 * duree / 5:
            currentPacManImage = GameConfig.imgPacMan_state_3
        elif self.pacman.possibleMove(self.pacman.direction) and millis % every >= every - 5 * duree / 5:
            currentPacManImage = GameConfig.imgPacMan_state_2
        window.blit(pygame.transform.rotate(currentPacManImage, self.pacman.direction * 90),
                    (GameConfig.mapStartW + self.pacman.x - round(GameConfig.pacManW / 2),
                     GameConfig.mapStartH + self.pacman.y - round(GameConfig.pacManH / 2)))

        # Affichage fantomes
        every: int = 200000  # Temps entre chaque fois que pacMan ferme la bouche en micro secondes
        duree = 100000  # durée pendant laquelle pacMan ferme sa bouche en micro secondes
        millis = datetime.now().microsecond
        for ghost in self.ghosts:
            currentGhostImg = getGhostImg(ghost.name, ghost.direction, False, ghost.state)
            if millis % every >= every - duree:
                currentGhostImg = getGhostImg(ghost.name, ghost.direction, True, ghost.state)
            window.blit(currentGhostImg,
                        (GameConfig.mapStartW + ghost.x - round(GameConfig.ghostW / 2),
                         GameConfig.mapStartH + ghost.y - round(GameConfig.ghostH / 2)))

        # Affichage vie
        for i in range(0, self.life):
            window.blit(pygame.transform.rotate(GameConfig.imgPacMan, 90),
                        (GameConfig.mapStartW + 50 + i * (GameConfig.pacManW + 10),
                         GameConfig.mapStartH + GameConfig.mapSizeH + 20))

        font = pygame.font.Font('resources/arcadeClassic.ttf', 20)
        img = font.render(str(self.score), True, GameConfig.white)
        displayRect = img.get_rect()
        displayRect.center = (GameConfig.mapStartW + 50, GameConfig.mapStartH - 25)
        window.blit(img, displayRect)
        window.blit(pygame.image.load('resources/bigDot.png'),
                    (GameConfig.mapStartW + 50 + i * (GameConfig.pacManW + 10),
                     GameConfig.mapStartH + GameConfig.mapSizeH + 20))

    def checkEatDot(self):
        if (self.pacman.x - 35) % 21 == 0 and (self.pacman.y - 35) % 21 == 0:
            for dots in self.dots:
                if dots and not self.pacman.y - 15 < dots[0].y < self.pacman.y + 15:
                    pass
                for dot in dots:
                    if self.pacman.x - 15 < dot.x < self.pacman.x + 15 and self.pacman.y - 15 < dot.y < self.pacman.y + 15:
                        dots.remove(dot)
                        self.drawDots(round((dot.y - 35) / 21))
                        self.drawAllDots()
                        if dot.value == 1:
                            self.initDate()
                            for ghost in self.ghosts:
                                ghost.scraredMode()
                        else:
                            self.score += 10
                        if self.checkNextLevel():
                            self.pacman.initialPosition()
                            self.pacman.setDirection("up")
                            for ghost in self.ghosts:
                                ghost.setup()
                            self.level += 1

                            self.initDots()
                        break

    def checkNextLevel(self):
        for dots in self.dots:
            if len(dots) != 0:
                return False
        return True

    def moveGhost(self):
        print()
        for ghost in self.ghosts:
            ghost.move()

            if ghost.state == 3 and time() - self.date > 7.0:
                ghost.state = 1
            if ghost.x - round(GameConfig.ghostW / 2) < self.pacman.x < ghost.x + round(GameConfig.ghostW / 2) \
                    and ghost.y - round(GameConfig.ghostW / 2) < self.pacman.y < ghost.y + round(GameConfig.ghostW / 2):
                if ghost.state != 3:
                    self.life -= 1
                    self.pacman.initialPosition()
                    for ghost in self.ghosts:
                        ghost.setup()
                    if self.life < 0:
                        self.gameOver = True
                    else:
                        sleep(1)
                else:
                    ghost.state = 0
                    ghost.eat()

    def initDate(self):
        self.date = time()
