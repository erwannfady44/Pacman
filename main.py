import pygame
from GameConfig import GameConfig
from Game import *


def gameLoop(window, clock):
    newDirection = ""
    game = Game()
    game.drawStart(window)
    pygame.display.update()
    sleep(1)
    changeDirection = False
    while not game.gameOver:
        if game.win or game.loose:
            game.loose = False
            game.drawStart(window)
            pygame.display.update()
            sleep(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                newDirection = 0
                changeDirection = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                newDirection = 1
                changeDirection = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                newDirection = 2
                changeDirection = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                newDirection = 3
                changeDirection = True

        if changeDirection:
            if game.pacman.possibleMove(newDirection):
                direction = newDirection
                game.pacman.setDirection(direction)

        game.nextState()
        game.draw(window)
        pygame.display.update()
        clock.tick(GameConfig.fps)
    game.drawGameOver(window)
    pygame.display.update()
    sleep(3)

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((GameConfig.windowW, GameConfig.windowH))
    pygame.display.set_caption("PacMan")
    clock = pygame.time.Clock()
    clock.tick(GameConfig.fps)
    gameLoop(window, clock)
    pygame.quit()
    quit()

