from math import sqrt
from queue import Queue
from random import randint, choice

from GameConfig import GameConfig, ghostSetup, getScatterTarget
from Node import Node


class Ghost:
    def __init__(self, name, pacman, blinky):
        self.x = 0
        self.y = 0
        self.targetX = 0
        self.targetY = 0
        self.direction = 0
        self.name = name
        self.state = 3
        self.timeBeforeExit = 0
        self.nodes = []
        self.initNodes()
        self.setup()
        self.pacman = pacman
        self.blinky = blinky
        self.nextDirection = 0
        self.nextState = 2
        if self.state != 0:
            self.direction = self.bfs()
            self.setNextDirection()

    def move(self):
        # Si il est sorti du centre
        if self.state != 0:
            if self.possibleMove(self.nextDirection, False):
                if not (self.direction % 2 == self.nextDirection % 2 and self.nextDirection != self.direction):
                    self.direction = self.nextDirection

            self.setNextDirection()
        else:
            # Si il est au centre
            if self.state == 0:
                if self.timeBeforeExit > 0:
                    # Si on est rendu en haut de la prison est qu'on peut pas monter plus, on descend
                    if self.direction == 0 and not self.possibleMove(self.direction, False):
                        self.direction = 2
                        self.timeBeforeExit -= 1
                    # Si on est rendu en bas de la prison est qu'on peut pas monter plus, on monte
                    elif self.direction == 2 and not self.possibleMove(self.direction, False):
                        self.direction = 0
                # Si on sors
                elif self.timeBeforeExit == 0:
                    if self.possibleMove(1, False):
                        self.timeBeforeExit = -1
                        self.direction = 1
                    elif self.possibleMove(3, False):
                        self.timeBeforeExit = -1
                        self.direction = 3
                    if self.x == 297 and self.y == 246:
                        self.state = self.nextState

                if self.timeBeforeExit == -1:
                    if self.x == 297 and self.possibleMove(0, False):
                        self.direction = 0
                    if self.x == 297 and self.y == 246:
                        self.state = self.nextState
                        self.setNextDirection()

        # Déplacement du fantome
        if self.possibleMove(self.direction, True):
            if self.direction == 0:
                self.y -= 1
            elif self.direction == 1:
                self.x += 1
            elif self.direction == 2:
                self.y += 1
            elif self.direction == 3:
                self.x -= 1

    def possibleMove(self, direction, move):
        if self.state != 0:
            if direction == 0:
                if GameConfig.imgMove.get_at((self.x, self.y - 1)) == (255, 255, 255, 255):
                    return True
            elif direction == 1:
                # Si on est dans le tunel qui traverse la map
                if 150 < self.y < 320 and self.x > 570 and move:
                    self.x = 5
                    return True
                elif GameConfig.imgMove.get_at((self.x + 1, self.y)) == (255, 255, 255, 255):
                    return True
            elif direction == 2:
                if GameConfig.imgMove.get_at((self.x, self.y + 1)) == (255, 255, 255, 255):
                    return True
            elif direction == 3:
                # Si on est dans le tunel qui traverse la map
                if 150 < self.y < 320 and self.x < 5 and move:
                    self.x = 580
                    return True
                elif GameConfig.imgMove.get_at((self.x - 1, self.y)) == (255, 255, 255, 255):
                    return True
        else:
            if direction == 0:
                if GameConfig.imgMove.get_at((self.x, self.y - 1)) == (255, 0, 0, 255):
                    return True
            elif direction == 1:
                if GameConfig.imgMove.get_at((self.x + 1, self.y)) == (255, 0, 0, 255):
                    return True
            elif direction == 2:
                if GameConfig.imgMove.get_at((self.x, self.y + 1)) == (255, 0, 0, 255):
                    return True
            elif direction == 3:
                if GameConfig.imgMove.get_at((self.x - 1, self.y)) == (255, 0, 0, 255):
                    return True

    def setDirection(self):
        self.setTarget()
        self.direction = self.bfs()
        # self.direction = 1

    def randomDirection(self):
        directions = self.getPossibleDirection()
        newDirection = choice(directions)
        while newDirection % 2 == self.direction % 2 and self.direction != newDirection:
            newDirection = choice(directions)
        return newDirection

    def setNextDirection(self):
        # Mode chasse ou repli
        if self.state == 1 or self.state == 2:
            # Mode chasse
            if self.state == 1:
                self.setTarget()
            # Mode repli
            elif self.state == 2:
                self.targetX, self.targetY = getScatterTarget(self.name)
            if self.targetX - 21 < self.x < self.targetX + 21 and self.targetY - 21 < self.y < self.targetY + 21:
                directions = self.getPossibleDirection()
                newDirection = choice(directions)
                while newDirection % 2 == self.direction % 2 and self.direction != newDirection:
                    newDirection = choice(directions)
                self.direction = newDirection
            else:
                self.nextDirection = self.bfs()
        # Mode fuite
        elif self.state == 3:
            directions = self.getPossibleDirection()
            newDirection = choice(directions)
            while newDirection % 2 == self.direction % 2 and self.direction != newDirection:
                newDirection = choice(directions)
            self.nextDirection = newDirection

    def setTarget(self):
        if self.name == "blinky":
            self.targetX = self.pacman.x
            self.targetY = self.pacman.y
        elif self.name == "clyde":
            if abs(self.targetX - self.pacman.x) / 21 <= 8 or abs(self.targetY - self.pacman.y) / 21 <= 8:
                self.targetX, self.targetY = getScatterTarget(self.name)
            else:
                self.targetX = self.pacman.x
                self.targetY = self.pacman.y
        elif self.name == "pinky":
            if self.pacman.direction == 0:
                if self.pacman.x > 95:
                    self.targetX = self.pacman.x - 60
                else:
                    self.targetX = 35
                if self.pacman.y < 563:
                    self.targetY = self.pacman.y + 60
                else:
                    self.targetY = 623
            elif self.pacman.direction == 1:
                if self.pacman.x < 500:
                    self.targetX = self.pacman.x + 60
                else:
                    self.targetX = 560
                self.targetY = self.pacman.y
            elif self.pacman.direction == 2:
                self.targetX = self.pacman.x
                if self.pacman.y < 563:
                    self.targetY = self.pacman.y + 60
                else:
                    self.targetY = 623
            elif self.pacman.direction == 3:
                if self.pacman.x > 95:
                    self.targetX = self.pacman.x - 60
                else:
                    self.targetX = 35
                self.targetY = self.pacman.y
        elif self.name == "inky":
            if self.pacman.direction == 0:
                if self.pacman.x > 65:
                    self.symX = self.pacman.x - 30
                else:
                    self.symX = 35
                if self.pacman.y < 593:
                    self.symY = self.pacman.y + 30
                else:
                    self.symY = 623
            elif self.pacman.direction == 1:
                if self.pacman.x < 530:
                    self.symX = self.pacman.x + 30
                else:
                    self.symX = 560
                self.symY = self.pacman.y
            elif self.pacman.direction == 2:
                self.symX = self.pacman.x
                if self.pacman.y < 593:
                    self.symY = self.pacman.y + 30
                else:
                    self.symY = 623
            elif self.pacman.direction == 3:
                if self.pacman.x > 65:
                    self.symX = self.pacman.x - 30
                else:
                    self.symX = 35
                self.symY = self.pacman.y
            if self.blinky.x < self.pacman.x:
                self.targetX = self.pacman.x + self.pacman.x - self.blinky.x
            else:
                self.targetX = self.pacman.x - self.blinky.x + self.pacman.x
            if self.blinky.y < self.pacman.y:
                self.targetY = self.pacman.y + self.pacman.y - self.blinky.y
            else:
                self.targetY = self.pacman.y - self.blinky.y + self.pacman.y
            if self.targetX < 35:
                self.targetX = 35
            elif self.targetX > 560:
                self.targetX = 560
            if self.targetY < 35:
                self.targetY = 35
            elif self.targetY > 623:
                self.targetY = 623

    def getPossibleDirection(self):
        possibleDirection = []
        for i in range(0, 4):
            if self.possibleMove(i, False):
                possibleDirection.append(i)
        return possibleDirection

    def getPossibleMoveBFS(self, x, y):
        directions = []
        if (y - 35) % 21 == (x - 35) % 21 == 0:
            if GameConfig.imgNodes.get_at((x, y - 21)) == (255, 255, 255, 255):
                directions.append(0)
            # Si on est dans le tunel qui traverse la map
            if 150 < y < 320 and x > 570:
                directions.append(1)
            elif GameConfig.imgNodes.get_at((x + 21, y)) == (255, 255, 255, 255):
                directions.append(1)
            if GameConfig.imgNodes.get_at((x, y + 21)) == (255, 255, 255, 255):
                directions.append(2)
            # Si on est dans le tunel qui traverse la map
            if 150 < y < 320 and x < 5:
                directions.append(3)
            elif GameConfig.imgNodes.get_at((x - 21, y)) == (255, 255, 255, 255):
                directions.append(3)
            return directions
        else:
            directions.append(self.direction)
            return directions

    def bfs(self):
        startX = self.x
        startY = self.y

        while (startX - 35) % 21 != 0:
            if startX > 560:
                startX = 560
            elif startX < 35:
                startX = 35
            elif self.direction == 1:
                startX += 1
            elif self.direction == 3:
                startX -= 1
            else:
                if (startX - 35) % 21 < 11:
                    startX -= 1
                else:
                    startX += 1

        while (startY - 35) % 21 != 0:
            if startY > 560:
                startY = 560
            elif startY < 35:
                startY = 35
            elif self.direction == 0:
                startY -= 1
            elif self.direction == 2:
                startY += 1
            else:
                if (startY - 35) % 21 < 11:
                    startY -= 1
                else:
                    startY += 1

        while (self.targetX - 35) % 21 != 0:
            if self.targetX > 560:
                self.targetX = 35
            elif self.targetX < 35:
                self.targetX = 560
            else:
                if (self.targetX - 35) % 21 < 11:
                    self.targetX -= 1
                else:
                    self.targetX += 1

        while (self.targetY - 35) % 21 != 0:
            if self.targetY > 560:
                self.targetY = 560
            elif self.targetY < 35:
                self.targetY = 35
            else:
                if (self.targetY - 35) % 21 < 11:
                    self.targetY -= 1
                else:
                    self.targetY += 1

        start = self.nodes[round((startY - 35) / 21)][round((startX - 35) / 21)]
        target = self.nodes[round((self.targetY - 35) / 21)][round((self.targetX - 35) / 21)]
        start.visited = True
        queue = Queue()
        queue.put(start)
        try:
            while not queue.empty():
                curNode = queue.get()
                poosibleDirection = self.getPossibleMoveBFS(curNode.x, curNode.y)

                neighbors = []
                for direction in poosibleDirection:
                    x = curNode.x
                    y = curNode.y
                    if direction == 0:
                        y -= 21
                    elif direction == 1:
                        if x >= 560:
                            x = 35
                        else:
                            x += 21
                    elif direction == 2:
                        y += 21
                    elif direction == 3:
                        if x <= 35:
                            x = 560
                        else:
                            x -= 21
                    neighbors.append(self.nodes[round((y - 35) / 21)][round((x - 35) / 21)])

                if curNode == target:
                    while curNode.parent.parent is not None and not (
                            curNode.parent.x == startX and curNode.parent.y == startY) and not (
                            curNode.x == curNode.parent.parent.x and curNode.y == curNode.parent.parent.y):
                        curNode = curNode.parent
                    # curNode = curNode.parent
                    ghostDirection = 0
                    if curNode.y < startY:
                        ghostDirection = 0
                    elif curNode.x > startX:
                        ghostDirection = 1
                    elif curNode.y > startY:
                        ghostDirection = 2
                    elif curNode.x < startX:
                        ghostDirection = 3
                    self.resetNode()
                    if ghostDirection % 2 == self.direction % 2 and self.direction != ghostDirection:
                        return self.shorterDistanceWithPythagore(start, target)
                    else:
                        return ghostDirection
                else:
                    for neighbor in neighbors:
                        if not neighbor.visited:
                            neighbor.visited = True
                            neighbor.parent = curNode
                            queue.put(neighbor)
        except Exception:
            return self.shorterDistanceWithPythagore(start, target)
        self.resetNode()

    def shorterDistanceWithPythagore(self, start, target):
        if not (150 < start.y < 320 and start.x > 570):
            distance = []
            for direction in self.getPossibleMoveBFS(start.x, start.y):
                if not (direction % 2 == self.direction % 2 and direction != self.direction):
                    positionX = 0
                    positionY = 0
                    if direction == 0:
                        positionY -= 21
                    elif direction == 1:
                        if positionX >= 560:
                            positionX = 35
                        else:
                            positionX += 21
                    elif direction == 2:
                        positionY += 21
                    elif direction == 3:
                        if positionX <= 35:
                            positionX = 560
                        else:
                            positionX -= 21
                    distance.append(
                        (sqrt((positionX - target.x) ** 2 + (positionY - target.y) ** 2), direction))

            dmin = distance[0]
            i = 0
            for d in distance:
                if d[0] < dmin[0]:
                    dmin = d
            return dmin[1]
        else:
            return self.randomDirection()

    def resetNode(self):
        for nodes in self.nodes:
            for node in nodes:
                if node is not None:
                    node.visited = False
                    node.parent = None

    def initNodes(self):
        y = 35

        while y < 630:
            x = 35
            i = 0
            if y != 35:
                i = round((y - 35) / 21)
            self.nodes.append([])
            while x < 580:
                if GameConfig.imgNodes.get_at((x, y)) == (255, 255, 255, 255):
                    self.nodes[i].append(Node(x, y))
                else:
                    self.nodes[i].append(None)
                x += 21
            y += 21

    def setup(self):
        self.x, self.y, self.state, self.timeBeforeExit = ghostSetup(self.name)
        self.targetX, self.targetY = getScatterTarget(self.name)
        if self.name == 'blinky':
            self.direction = 1

    def scraredMode(self):
        if self.state != 0:
            self.state = 3
            self.direction = choice(self.getPossibleDirection())
            self.setNextDirection()

    def scatterMode(self):
        if self.state == 0:
            self.nextState = 2
        else:
            self.state = 2

    def chaseMode(self):
        if self.state == 0:
            self.nextState = 1
        else:
            self.state = 1

    def turnArround(self):
        self.direction = (self.direction + 2) % 4

    def eat(self):
        if self.name != 'blinky':
            self.setup()
        else:
            self.x, self.y, self.state, self.timeBeforeExit = ghostSetup("pinky")
            self.targetX, self.targetY = getScatterTarget("pinky")
