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

        self.ghosts = [blinky, Ghost("pinky", self.pacman, None), Ghost("clyde", self.pacman, None),
                       Ghost("inky", self.pacman, blinky)]

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
        self.win = False
        self.loose = False

    def nextState(self):
        self.pacman.move()
        self.checkEatDot()
        self.moveGhost()

        if self.mode == 1 and (time() - self.stateDate) > 60.0:
            print("scatterMode")
            self.mode = 2
            for ghost in self.ghosts:
                if ghost.state != 3:
                    ghost.scatterMode()
            self.stateDate = time()
        elif self.mode == 2 and (time() - self.stateDate) > 10.0:
            print("chasseMode")
            self.mode = 1
            for ghost in self.ghosts:
                if ghost.state != 3:
                    ghost.chaseMode()
            self.stateDate = time()

        else:
            for ghost in self.ghosts:
                if ghost.state == 3 and (time() - self.date) > 15:
                    ghost.state = 1

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
                self.dotsView[i].blit(img, (dot.x - 8, - 8))

    def drawAllDots(self):
        i = 0
        self.allDotsView.fill((0, 0, 0))
        for dotView in self.dotsView:
            self.allDotsView.blit(dotView, (GameConfig.mapStartW, GameConfig.mapStartH + 35 + i * 21))
            i += 1

    def drawStart(self, window):
        self.win = False
        self.draw(window)
        font = pygame.font.Font('resources/arcadeClassic.ttf', 40)
        img = font.render("READY!", True, GameConfig.yellow)
        displayRect = img.get_rect()
        displayRect.center = (405, 440)
        window.blit(img, displayRect)

    def drawGameOver(self, window):
        window.fill(GameConfig.background)
        window.blit(GameConfig.imgMap, (GameConfig.mapStartW, GameConfig.mapStartH))
        window.blit(self.allDotsView, (0, 0))

        font = pygame.font.Font('resources/arcadeClassic.ttf', 20)
        img = font.render(str(self.score), True, GameConfig.white)
        displayRect = img.get_rect()
        displayRect.center = (GameConfig.mapStartW + 50, GameConfig.mapStartH - 25)
        window.blit(img, displayRect)

        self.draw(window)
        font = pygame.font.Font('resources/arcadeClassic.ttf', 35)
        img = font.render("GAME        OVER", True, GameConfig.red)
        displayRect = img.get_rect()
        displayRect.center = (400, 440)
        window.blit(img, displayRect)

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
        window.blit(pygame.transform.rotate(currentPacManImage, int(self.pacman.direction * 90)),
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

    def checkEatDot(self):
        for dots in self.dots:
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
                        self.pacman.setDirection(0)
                        for ghost in self.ghosts:
                            ghost.setup()
                        self.level += 1

                        self.initDots()
                        self.win = True
                    break

    def checkNextLevel(self):
        for dots in self.dots:
            if len(dots) != 0:
                return False
        return True

    def moveGhost(self):
        for ghost in self.ghosts:
            ghost.move()
            if ghost.x - round(GameConfig.ghostW / 2) < self.pacman.x < ghost.x + round(GameConfig.ghostW / 2) \
                    and ghost.y - round(GameConfig.ghostW / 2) < self.pacman.y < ghost.y + round(GameConfig.ghostW / 2):
                if ghost.state != 3 and ghost.state != 0:
                    self.life -= 1
                    self.pacman.initialPosition()
                    self.mode = 2
                    self.initDate()
                    self.loose = True
                    self.pacman.direction = 3
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
