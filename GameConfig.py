import pygame


class GameConfig:
    windowW = 800
    windowH = 800
    white = (255, 255, 255)
    background = (0, 0, 0)
    wall = (32, 32, 255)
    pacManW = 30
    pacManH = 30
    imgPacMan = pygame.image.load('resources/pacMan.png')
    imgPacMan_state_2 = pygame.image.load('resources/pacman_state_2.png')
    imgPacMan_state_3 = pygame.image.load('resources/pacman_state_3.png')
    imgPacManClose = pygame.image.load('resources/pacMan_close.png')
    imgMap = pygame.image.load('resources/map.png')
    imgMove = pygame.image.load('resources/move.png')
    imgDots = pygame.image.load('resources/dots.png')
    imgNodes = pygame.image.load('resources/nodes.png')
    imgDot = pygame.image.load('resources/dot.png')
    imgBigDot = pygame.image.load('resources/bigDot.png')
    mapW = 26
    mapH = 29
    mapSizeW = 597
    mapSizeH = 662
    mapStartW = 100
    mapStartH = 68
    ghostW = 30
    ghostH = 30
    font = 'ressources/arcadeClassic.ttf'
    fps = 60


def getGhostImg(name, direction, variation, state):
    if state == 3:
        sheet = pygame.image.load('resources/blueGhost.png')
        if not variation:
            img = sheet.subsurface(0, 0, 16, 16)  # gauche
        else:
            img = sheet.subsurface(16, 0, 16, 16)
    else:
        sheet = pygame.image.load('resources/' + name + '.png')
        if direction == 0:
            if not variation:
                img = sheet.subsurface(64, 0, 16, 16)  # haut
            else:
                img = sheet.subsurface(80, 0, 16, 16)
        elif direction == 1:
            if not variation:
                img = sheet.subsurface(0, 0, 16, 16)  # gauche
            else:
                img = sheet.subsurface(16, 0, 16, 16)
        elif direction == 2:
            if not variation:
                img = sheet.subsurface(96, 0, 16, 16)  # bas
            else:
                img = sheet.subsurface(112, 0, 16, 16)
        elif direction == 3:
            if not variation:
                img = sheet.subsurface(32, 0, 16, 16)  # droite
            else:
                img = sheet.subsurface(48, 0, 16, 16)

    return pygame.transform.scale(img, (30, 30))


def ghostSetup(name):
    if name == "clyde":
        return 344, 314, 0, 17
    elif name == "blinky":
        return 297, 245, 2, 0
    elif name == "pinky":
        return 297, 314, 0, -1
    elif name == "inky":
        return 249, 314, 0, 10


def getScatterTarget(name):
    if name == "clyde":
        return 35, 623
    if name == "blinky":
        return 560, 35
    elif name == "pinky":
        return 35, 35
    elif name == "inky":
        return 560, 623
