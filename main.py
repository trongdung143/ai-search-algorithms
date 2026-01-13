import pygame
import random
import numpy as np
import copy
import queue
from queue import PriorityQueue


class GameAI:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1300, 820))
        pygame.display.set_caption("Game AI")
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.dx = 45
        self.dy = 20
        self.menu = True
        self.createMap = False
        self.isDragging = False
        self.mouseThroughRect = []
        self.rectMenu = [
            pygame.Rect(500, 100, 200, 100),
            pygame.Rect(500, 300, 200, 100),
            pygame.Rect(500, 500, 200, 100),
        ]
        self.textMenu = ["Start", "Create Map", "Exit"]
        self.textCreateMap = [
            "Press and drag the mouse to",
            "            select the region",
            "Press 1 to set the start position",
            "Press 2 to set the end position",
            "Press 3 to create a wall",
            "Press 4 to delete",
            "Press s to start game",
        ]
        self.sizeMap = [29, 29]
        self.rectMap = []
        self.running = True
        self.time = 0
        self.speed = [1, pygame.rect.Rect(950, 200, 0, 0)]
        self.start = False
        self.end = False
        self.map = np.ones((self.sizeMap[0], self.sizeMap[1]), dtype=int)
        self.graph = {}
        self.sizeImage = [27, 27]
        self.posStart = (5, 5)
        self.posEnd = (26, 19)
        self.movePlayer = 0
        self.skipPlayer = pygame.rect.Rect(
            self.sizeImage[0] * self.sizeMap[0] + 320, 147, 0, 0
        )
        self.endGame = False
        self.player = [5, 5]
        self.textPlayer = "Player"
        self.vec = [0, 0]
        self.playerFinish = False
        self.activeAllBots = [pygame.rect.Rect(870, 200, 20, 20), (255, 0, 0), False]
        self.pathG = {}
        self.info = {
            "dfs": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/dfs.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 1 * 80 + 170, 20, 20),
                False,
                "Dfs",
                0,
            ],
            "bfs": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/bfs.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 2 * 80 + 170, 20, 20),
                False,
                "Bfs",
                0,
            ],
            "hillclimbing": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/hillclimbing.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 3 * 80 + 170, 20, 20),
                False,
                "Hcb",
                0,
            ],
            "aStar": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/astar.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 4 * 80 + 170, 20, 20),
                False,
                "A*",
                0,
            ],
            "greedy": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/greedy.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 5 * 80 + 170, 20, 20),
                False,
                "Greedy",
                0,
            ],
            "ucs": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/ucs.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 6 * 80 + 170, 20, 20),
                False,
                "Ucs",
                0,
            ],
            "beam": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/beam.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 7 * 80 + 170, 20, 20),
                False,
                "Beam",
                0,
            ],
        }
        self.allPath = {
            "dfs": [[], (95, 87, 78, 130)],
            "bfs": [[], (174, 174, 255, 130)],
            "hillclimbing": [[], (70, 94, 86, 130)],
            "aStar": [[], (16, 102, 114, 130)],
            "greedy": [[], (255, 105, 180, 130)],
            "ucs": [[], (58, 58, 58, 130)],
            "beam": [[], (153, 102, 255, 130)],
        }

        self.intersections = {"aStar": [[], [], []], "greedy": [], "ucs": [[], [], []]}
        self.images = [
            pygame.transform.scale(
                pygame.image.load("images/finish.png"),
                (self.sizeImage[0], self.sizeImage[1]),
            ),
            pygame.transform.scale(
                pygame.image.load("images/wall.png"),
                (self.sizeImage[0], self.sizeImage[1]),
            ),
            pygame.transform.scale(
                pygame.image.load("images/player.png"),
                (self.sizeImage[0], self.sizeImage[1]),
            ),
            pygame.transform.scale(pygame.image.load("images/bg.png"), (1320, 840)),
            pygame.transform.scale(
                pygame.image.load("images/wall.png"),
                (self.sizeImage[0], self.sizeImage[1] + 20),
            ),
            pygame.transform.rotate(
                pygame.transform.scale(
                    pygame.image.load("images/t.png"),
                    (50, 25),
                ),
                -90,
            ),
        ]

    # Algorithms
    def checkPosition(self, current, visited=None):
        if visited is None:
            visited = set()
        return (
            0 <= current[0] < self.sizeMap[0]
            and 0 <= current[1] < self.sizeMap[1]
            and self.map[current[0]][current[1]] == 0
            and current not in visited
        )

    def Herwinning(self, current, parents):
        path = []
        while current is not None:
            path.append(current)
            current = parents[current]
        return path[::-1]

    def Heuristic(self, current):
        return abs(current[0] - self.posEnd[0]) + abs(current[1] - self.posEnd[1])

    def Dfs(self):
        self.info["dfs"][0].append(self.posStart)
        self.allPath["dfs"][0].append((self.posStart, 0))
        stack = [self.posStart]
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        visited = set()
        visited.add(self.posStart)
        count = 1
        while self.info["dfs"][0][-1] != self.posEnd:
            current = self.info["dfs"][0][-1]
            foundMove = False
            random.shuffle(moves)

            for direction in moves:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if self.checkPosition(neighbor, visited):
                    visited.add(neighbor)
                    self.info["dfs"][0].append(neighbor)
                    self.allPath["dfs"][0].append((neighbor, count))
                    stack.append(neighbor)
                    foundMove = True
                    count += 1
                    break

            if not foundMove:
                if stack:
                    stack.pop()
                if stack:
                    self.info["dfs"][0].append(stack[-1])
                    self.allPath["dfs"][0].append((stack[-1], count))
                    count += 1
                else:
                    break

    def Bfs(self):
        openList = queue.Queue()
        openList.put(self.posStart)

        visited = set()
        visited.add(self.posStart)
        parents = {self.posStart: None}
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        count = 1
        self.allPath["bfs"][0] = [(self.posStart, 0)]
        while not openList.empty():
            current = openList.get()

            if current == self.posEnd:
                break

            random.shuffle(moves)
            for direction in moves:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if self.checkPosition(neighbor, visited):
                    visited.add(neighbor)
                    openList.put(neighbor)
                    self.allPath["bfs"][0].append((neighbor, count))
                    parents[neighbor] = current
                    count += 1

        current = self.posEnd
        self.allPath["bfs"][0].append((self.posEnd, count))
        while current:
            self.info["bfs"][0].append(current)
            try:
                current = parents[current]
            except:
                return False
        self.info["bfs"][0].reverse()
        return True

    def AStar(self):
        openList = PriorityQueue()
        openList.put((0, self.posStart))
        visited = set()
        gnList = {self.posStart: 0}
        fnList = {self.posStart: self.Heuristic(self.posStart)}
        parents = {self.posStart: None}
        count = 1
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while not openList.empty():
            _, current = openList.get()
            visited.add(current)
            self.allPath["aStar"][0].append((current, count))
            count += 1
            if current == self.posEnd:
                self.info["aStar"][0] = self.Herwinning(current, parents)
                return

            for direction in moves:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if self.checkPosition(neighbor):
                    nextGn = gnList[current] + 1

                    if neighbor not in gnList or nextGn < gnList[neighbor]:
                        gnList[neighbor] = nextGn
                        fnList[neighbor] = nextGn + self.Heuristic(neighbor)
                        parents[neighbor] = current
                        openList.put((fnList[neighbor], neighbor))

    def Hillclimbing(self):
        current = self.posStart
        path = [current]
        count = 1
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while current != self.posEnd:
            neighbors = []
            for direction in moves:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if self.checkPosition(neighbor):
                    neighbors.append(neighbor)

            if not neighbors:
                break

            for i in neighbors:
                if self.Heuristic(current) > self.Heuristic(i):
                    current = i

            if current in path:
                break
            path.append(current)
            self.allPath["hillclimbing"][0].append((current, count))
            count += 1

        if path[-1] == self.posEnd:
            self.info["hillclimbing"][0] = path
        else:
            self.info["hillclimbing"][0] = [self.posStart]

    def Greedy(self):
        openList = PriorityQueue()
        visited = set()
        openList.put((self.Heuristic(self.posStart), self.posStart))
        visited.add(self.posStart)
        parents = {self.posStart: None}

        count = 1
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while not openList.empty():
            _, current = openList.get()
            self.allPath["greedy"][0].append((current, count))
            count += 1
            if current == self.posEnd:
                self.info["greedy"][0] = self.Herwinning(current, parents)
                return

            for direction in moves:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if self.checkPosition(neighbor):

                    if neighbor not in visited:
                        parents[neighbor] = current
                        openList.put((self.Heuristic(neighbor), neighbor))
                        visited.add(neighbor)

    def Ucs(self):
        openList = PriorityQueue()
        openList.put((0, self.posStart))

        gnList = {self.posStart: 0}
        parents = {self.posStart: None}

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        count = 1
        while not openList.empty():
            cost, current = openList.get()
            self.allPath["ucs"][0].append((current, count))
            count += 1
            if current == self.posEnd:
                self.info["ucs"][0] = self.Herwinning(current, parents)
                return

            for direction in moves:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if self.checkPosition(neighbor):
                    nextGn = cost + 1
                    if neighbor not in gnList or nextGn < gnList[neighbor]:
                        gnList[neighbor] = nextGn
                        parents[neighbor] = current
                        openList.put((nextGn, neighbor))

    def Beam(self):
        openList = PriorityQueue()
        openList.put((self.Heuristic(self.posStart), self.posStart))

        visited = set()
        visited.add(self.posStart)
        parents = {self.posStart: None}
        count = 1
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while not openList.empty():

            currentBeam = []
            for _ in range(3):
                if openList.empty():
                    break
                _, current = openList.get()
                currentBeam.append(current)
                self.allPath["beam"][0].append((current, count))
                count += 1

                if current == self.posEnd:
                    self.info["beam"][0] = self.Herwinning(current, parents)
                    return

            neighbors = []
            for state in currentBeam:
                for direction in moves:
                    neighbor = (state[0] + direction[0], state[1] + direction[1])
                    if self.checkPosition(neighbor) and neighbor not in visited:
                        visited.add(neighbor)
                        parents[neighbor] = state
                        neighbors.append((self.Heuristic(neighbor), neighbor))

            neighbors.sort()

            for heuristic, neighbor in neighbors[:3]:
                openList.put((heuristic, neighbor))
        self.info["beam"][0] = [self.posStart]

    ## Stactic Display
    def CreateMap(self):
        moves = [(0, -2), (-2, 0), (0, 2), (2, 0)]
        stack = []
        self.map[self.posStart[0]][self.posStart[1]] = 0
        self.map[self.posEnd[0]][self.posEnd[1]] = 0
        random.shuffle(moves)
        for dx, dy in moves:
            nx, ny = self.posStart[0] + dx, self.posStart[1] + dy
            if 1 <= nx < self.sizeMap[0] - 1 and 1 <= ny < self.sizeMap[1] - 1:
                self.map[nx][ny] = 0
                self.map[self.posStart[0] + dx // 2][self.posStart[1] + dy // 2] = 0
                stack.append([nx, ny])

        self.map[self.posStart[0] + 3][self.posStart[1]] = 0
        self.map[self.posStart[0] - 3][self.posStart[1]] = 0

        while stack:
            random.shuffle(moves)
            random.shuffle(moves)
            x, y = stack[-1]
            for i in moves:
                nx, ny = x + i[0], y + i[1]
                if nx == self.posEnd[0] and ny == self.posEnd[1]:

                    return

                if (
                    1 <= nx < self.sizeMap[0] - 1
                    and 1 <= ny < self.sizeMap[1] - 1
                    and self.map[nx][ny] == 1
                ):
                    self.map[nx][ny] = 0
                    self.map[x + (i[0] // 2)][y + (i[1] // 2)] = 0
                    stack.append([nx, ny])
                    break
            else:
                stack.pop()

    def CheckCreateMap(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.isDragging:
                self.isDragging = True
                mousePos = pygame.mouse.get_pos()
                for row in self.rectMap:
                    for rect in row:
                        if (
                            rect.collidepoint(mousePos)
                            and rect not in self.mouseThroughRect
                        ):
                            self.mouseThroughRect.append(rect)

            elif event.type == pygame.MOUSEBUTTONUP and self.isDragging:
                self.isDragging = False

            elif event.type == pygame.MOUSEMOTION and self.isDragging:
                mousePos = pygame.mouse.get_pos()
                for row in self.rectMap:
                    for rect in row:
                        if (
                            rect.collidepoint(mousePos)
                            and rect not in self.mouseThroughRect
                        ):
                            self.mouseThroughRect.append(rect)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self.Bfs():
                        self.Dfs()
                        self.Hillclimbing()
                        self.AStar()
                        self.Greedy()
                        self.Ucs()
                        self.Beam()
                        self.menu = False
                        self.createMap = False
                    else:
                        font = pygame.font.Font(None, 80)
                        font.bold = True
                        textRender = font.render("No Way", True, (255, 0, 0))
                        self.win.blit(
                            textRender,
                            (
                                (self.win.get_size()[0] - textRender.get_size()[0])
                                // 2,
                                400,
                            ),
                        )
                        pygame.display.update()
                        pygame.time.delay(2000)
                elif event.key == pygame.K_ESCAPE and self.createMap:
                    self.__init__()

                elif (
                    event.key == pygame.K_1
                    and not self.isDragging
                    and len(self.mouseThroughRect) == 1
                ):
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] == self.mouseThroughRect[0]:
                                self.map[self.posStart[0]][self.posStart[1]] = 0
                                self.posStart = (i, j)
                                self.player[0] = j
                                self.player[1] = i
                                self.map[self.posStart[0]][self.posStart[1]] = 0
                                self.start = False
                                self.mouseThroughRect.clear()
                                return

                elif (
                    event.key == pygame.K_2
                    and not self.isDragging
                    and len(self.mouseThroughRect) == 1
                ):
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] == self.mouseThroughRect[0]:
                                self.map[self.posEnd[0]][self.posEnd[1]] = 0
                                self.posEnd = (i, j)
                                self.map[self.posEnd[0]][self.posEnd[1]] = 0
                                self.end = False
                                self.mouseThroughRect.clear()
                                return

                elif (
                    event.key == pygame.K_3
                    and not self.isDragging
                    and len(self.mouseThroughRect) > 0
                ):
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] in self.mouseThroughRect:
                                self.map[i][j] = 1
                    self.mouseThroughRect.clear()
                elif (
                    event.key == pygame.K_4
                    and not self.isDragging
                    and len(self.mouseThroughRect) > 0
                ):
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] in self.mouseThroughRect:
                                self.map[i][j] = 0
                    self.mouseThroughRect.clear()

    def RenderMenu(self):
        self.win.blit(self.images[3], (0, 0))
        for i in range(0, len(self.rectMenu)):
            font = pygame.font.Font(None, 46)
            textRender = font.render(self.textMenu[i], True, (0, 0, 0))
            size = textRender.get_size()
            self.rectMenu[i].x = self.win.get_size()[0] / 2 - size[0] / 2
            self.rectMenu[i].width = size[0]
            self.rectMenu[i].height = size[1]
            self.win.blit(
                textRender,
                (
                    self.win.get_size()[0] / 2 - size[0] / 2,
                    self.rectMenu[i].centery - textRender.get_size()[1] // 2,
                ),
            )

    def RenderText(self):
        rect = pygame.rect.Rect(
            self.dx + self.sizeImage[0] * self.sizeMap[0] + 20,
            0,
            self.win.get_size()[0]
            - (55 + self.dx + self.sizeImage[0] * self.sizeMap[0]),
            820,
        )
        pygame.draw.rect(self.win, (0, 0, 0), rect, 5, 10)
        if not self.endGame:
            self.font.bold = False
            textRender = self.font.render(
                "Time: " + str(self.time // 60) + "s", True, (0, 0, 0)
            )
            self.win.blit(
                textRender, (rect.centerx - textRender.get_size()[0] // 2, self.dy)
            )
            pygame.draw.rect(
                self.win, (self.activeAllBots[1]), self.activeAllBots[0], 10, 4
            )
            textRender = self.font.render(
                "X" + str(self.speed[0]) + "   " + "Speed", True, (0, 0, 0)
            )
            self.win.blit(textRender, (950, 200))
            # pygame.draw.rect(
            #     self.win,
            #     (0, 100, 0),
            #     pygame.rect.Rect(850 + self.dx, 65, 325, 65),
            #     2,
            #     10,
            # )
            # textRender = self.font.render("  22119054 LuuTrongDung", True, (0, 0, 0))
            # self.win.blit(textRender, (860 + self.dx, 70))
            # textRender = self.font.render(
            #     "22110062 DaoNguyenPhuc",
            #     True,
            #     (0, 0, 0),
            # )
            # self.win.blit(textRender, (860 + self.dx, 100))
            self.speed[1].width = textRender.get_size()[0]
            self.speed[1].height = textRender.get_size()[1]
            dy = 0
            textRender = self.font.render(self.textPlayer, True, (0, 0, 0))
            self.win.blit(
                textRender, (self.sizeImage[0] * self.sizeMap[0] + 130, dy + 147)
            )
            if not self.playerFinish:
                self.win.blit(
                    self.images[2],
                    (self.sizeImage[0] * self.sizeMap[0] + 270, dy + 145),
                )
                textRender = self.font.render("Skip", True, (0, 0, 0))
                self.skipPlayer.width = textRender.get_size()[0]
                self.skipPlayer.height = textRender.get_size()[1]
                self.win.blit(
                    textRender, (self.sizeImage[0] * self.sizeMap[0] + 320, dy + 147)
                )
        dy = 20

        for i, j in self.info.items():
            dy += 80
            textRender = self.font.render(self.info[i][7], False, (0, 0, 0))
            self.win.blit(
                textRender, (self.sizeImage[0] * self.sizeMap[0] + 150, dy + 148)
            )
            if not self.info[i][2]:
                pygame.draw.rect(self.win, self.info[i][4], self.info[i][5], 0, 4)
                pygame.draw.rect(self.win, self.allPath[i][1], self.info[i][5], 2, 4)
                self.win.blit(
                    self.info[i][3],
                    (self.sizeImage[0] * self.sizeMap[0] + 270, dy + 145),
                )

    def RenderTextCreateMap(self):
        rect = pygame.rect.Rect(
            self.dx + self.sizeImage[0] * self.sizeMap[0] + 20,
            0,
            self.win.get_size()[0]
            - (55 + self.dx + self.sizeImage[0] * self.sizeMap[0]),
            820,
        )
        pygame.draw.rect(self.win, (0, 0, 0), rect, 5, 10)
        font = pygame.font.Font(None, 28)
        pygame.draw.rect(
            self.win, (0, 0, 0), pygame.rect.Rect(900, 120, 310, 320), 5, 5
        )
        for i in range(0, len(self.textCreateMap)):
            textRender = font.render(self.textCreateMap[i], False, (0, 0, 0))
            if i > 1:
                self.win.blit(textRender, (910, i * 40 + 170))
            else:
                self.win.blit(textRender, (910, i * 20 + 130))
            if i == 1:
                self.win.blit(self.images[5], (1040, 180))

        textRender = font.render("Start Position", True, (0, 0, 0))
        pygame.draw.rect(
            self.win, (100, 149, 237), pygame.rect.Rect(900, 350 + 170, 20, 20), 0, 5
        )
        self.win.blit(textRender, (950, 350 + 170))
        textRender = font.render("End Position", True, (0, 0, 0))
        pygame.draw.rect(
            self.win, (0, 105, 148), pygame.rect.Rect(900, 400 + 170, 20, 20), 0, 5
        )
        self.win.blit(textRender, (950, 400 + 170))
        textRender = font.render("Wall", True, (0, 0, 0))
        pygame.draw.rect(
            self.win, (255, 0, 0), pygame.rect.Rect(900, 450 + 170, 20, 20), 0, 5
        )
        self.win.blit(textRender, (950, 450 + 170))
        textRender = font.render("Selected", True, (0, 0, 0))
        pygame.draw.rect(
            self.win, (0, 255, 0), pygame.rect.Rect(900, 500 + 170, 20, 20), 0, 5
        )
        self.win.blit(textRender, (950, 500 + 170))

    def CheckMouseMenu(self, mousePos, click):
        cursorHand = False
        for i in range(0, len(self.rectMenu)):
            if self.rectMenu[i].collidepoint(mousePos) and click:
                if i == 0:
                    self.map = np.ones((self.sizeMap[0], self.sizeMap[1]), dtype=int)
                    self.menu = False
                    self.CreateMap()
                    self.Dfs()
                    self.Bfs()
                    self.Hillclimbing()
                    self.AStar()
                    self.Greedy()
                    self.Ucs()
                    self.Beam()

                elif i == 1:
                    self.map = np.zeros((self.sizeMap[0], self.sizeMap[1]), dtype=int)
                    self.createMap = True
                    for i in range(0, self.sizeMap[0]):
                        temp = []
                        for j in range(0, self.sizeMap[1]):
                            temp.append(
                                pygame.Rect(
                                    j * self.sizeImage[0] + self.dx,
                                    i * self.sizeImage[1] + self.dy,
                                    self.sizeImage[1],
                                    self.sizeImage[1],
                                )
                            )
                        self.rectMap.append(temp)
                    return
                elif i == 2:
                    self.running = False

            if self.rectMenu[i].collidepoint(mousePos):
                self.font.bold = True
                cursorHand = True
                font = pygame.font.Font(None, 46)
                textRender = font.render(self.textMenu[i], True, (255, 165, 0))
                size = textRender.get_size()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.win.blit(
                    textRender,
                    (
                        self.win.get_size()[0] / 2 - size[0] / 2,
                        self.rectMenu[i].centery - textRender.get_size()[1] // 2,
                    ),
                )

        if not cursorHand:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    ## Logic
    def MovePlayer(self, mousePos, click):
        if self.skipPlayer.collidepoint(mousePos) and not self.playerFinish and click:
            self.player[0] = self.posEnd[1]
            self.player[1] = self.posEnd[0]
            self.playerFinish = True
            return

        if (
            0 <= self.player[1] + self.vec[1] < self.sizeMap[0]
            and 0 <= self.player[0] + self.vec[0] < self.sizeMap[1]
            and self.map[self.player[1] + self.vec[1]][self.player[0] + self.vec[0]]
            == 0
            and (self.vec[0] != 0 or self.vec[1] != 0)
        ):
            self.movePlayer += 1
            self.player[0] += self.vec[0]
            self.player[1] += self.vec[1]

        if (
            self.player[0] == self.posEnd[1]
            and self.player[1] == self.posEnd[0]
            and not self.playerFinish
        ):
            self.textPlayer += "  STEP: " + str(self.movePlayer)
            self.playerFinish = True

    def CheckWinBot(self):
        for i, j in self.info.items():
            if self.info[i][1] == len(self.info[i][0]) - 1 and not self.info[i][2]:
                if self.info[i][0][-1] == self.posEnd:
                    self.info[i][7] += " YES STEP: " + str(len(self.info[i][0]) - 1)
                    self.info[i][2] = True
                else:
                    self.info[i][7] += " NO STEP: " + str(len(self.info[i][0]) - 1)
                    self.info[i][2] = True

    def CheckOnBot(self, mousePos):
        if self.speed[1].collidepoint(mousePos):
            if self.speed[0] < 5:
                self.speed[0] += 1
            elif self.speed[0] == 5:
                self.speed[0] = 1
            return

        if self.activeAllBots[0].collidepoint(mousePos):
            if self.activeAllBots[2]:
                self.activeAllBots[1] = (255, 0, 0)
                self.activeAllBots[2] = False
                for i, j in self.info.items():
                    self.info[i][4] = (255, 0, 0)
                    self.info[i][6] = False

            elif not self.activeAllBots[2]:
                self.activeAllBots[1] = (0, 255, 0)
                self.activeAllBots[2] = True
                for i, j in self.info.items():
                    self.info[i][4] = (0, 255, 0)
                    self.info[i][6] = True
            return
        for i, j in self.info.items():
            if self.info[i][5].collidepoint(mousePos):
                if self.info[i][6]:
                    self.info[i][4] = (255, 0, 0)
                    self.info[i][6] = False
                elif not self.info[i][6]:
                    self.info[i][4] = (0, 255, 0)
                    self.info[i][6] = True

    def MoveBots(self):
        for i, j in self.info.items():
            if not self.info[i][2] and self.info[i][6]:
                self.info[i][8] += self.speed[0]
                if self.info[i][8] // 10 > self.info[i][1]:
                    self.info[i][1] += 1

    def CheckEndGame(self):
        if self.playerFinish:
            for i, j in self.info.items():
                if not self.info[i][2]:
                    return False
            self.win.fill((255, 255, 255))
            self.DrawMap()
            self.RenderText()
            self.BotsColor()
            self.DrawMap()
            textRender = self.font.render("End Game", True, (255, 0, 0))
            self.win.blit(
                textRender,
                (
                    (self.win.get_size()[0] - textRender.get_size()[0]) // 2,
                    (self.win.get_size()[1] - textRender.get_size()[1]) // 2,
                ),
            )
            pygame.display.update()
            return True
        return False

    ## Dynamic Display
    def BotsColor(self):
        dy = 0
        color = 0
        for i, j in self.info.items():
            dy += 100
            pygame.draw.rect(self.win, self.allPath[i][1], self.info[i][5], 10, 4)
            color += 1

    def DrawRectMap(self):
        pygame.draw.rect(
            self.win,
            (0, 0, 0),
            (self.dx - 10, 0, self.sizeMap[0] * self.sizeImage[0] + 20, 820),
            5,
            10,
        )
        for i in range(0, len(self.rectMap)):
            for j in range(0, len(self.rectMap)):
                if self.rectMap[i][j] in self.mouseThroughRect:
                    pygame.draw.rect(self.win, (50, 205, 50), self.rectMap[i][j], 0, 2)

                elif not self.start and (i, j) == self.posStart:
                    pygame.draw.rect(
                        self.win, (100, 149, 237), self.rectMap[i][j], 0, 2
                    )

                elif not self.end and (i, j) == self.posEnd:
                    pygame.draw.rect(self.win, (0, 105, 148), self.rectMap[i][j], 0, 2)

                elif self.map[i][j] == 1:
                    pygame.draw.rect(self.win, (178, 34, 34), self.rectMap[i][j], 0, 2)

                pygame.draw.rect(self.win, (0, 0, 0), self.rectMap[i][j], 1, 2)

    def DrawMap(self, wall=True):
        pygame.draw.rect(
            self.win,
            (0, 0, 0),
            (self.dx - 10, 0, self.sizeMap[0] * self.sizeImage[0] + 20, 820),
            5,
            10,
        )
        self.win.blit(
            self.images[0],
            (
                self.posEnd[1] * self.sizeImage[0] + self.dx,
                self.posEnd[0] * self.sizeImage[1] + self.dy,
            ),
        )
        self.win.blit(
            self.images[0],
            (
                self.posStart[1] * self.sizeImage[0] + self.dx,
                self.posStart[0] * self.sizeImage[1] + self.dy,
            ),
        )
        for i in range(0, self.sizeMap[0]):
            for j in range(0, self.sizeMap[1]):
                if self.map[i][j] == 1 and wall:
                    self.win.blit(
                        self.images[4],
                        (
                            j * self.sizeImage[0] + self.dx,
                            i * self.sizeImage[1] + self.dy - 20,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.win,
                        (0, 0, 0),
                        pygame.rect.Rect(
                            j * self.sizeImage[0] + self.dx,
                            i * self.sizeImage[1] + self.dy,
                            self.sizeImage[0],
                            self.sizeImage[1],
                        ),
                        1,
                        2,
                    )

    def DrawPlayer(self):
        if not self.playerFinish:
            self.win.blit(
                self.images[2],
                (
                    self.player[0] * self.sizeImage[0] + self.dx,
                    self.player[1] * self.sizeImage[1] + self.dy,
                ),
            )

    def DrawBot(self):
        for i, j in self.info.items():
            if (j[0][j[1]][0], j[0][j[1]][1]) != self.posEnd:
                self.win.blit(
                    j[3],
                    (
                        j[0][j[1]][1] * self.sizeImage[0] + self.dx,
                        j[0][j[1]][0] * self.sizeImage[1] + self.dy,
                    ),
                )

    def DrawAllPathBots(self):
        self.win.fill((255, 255, 255))
        self.DrawMap()
        self.RenderText()
        self.BotsColor()
        pygame.display.update()
        temp = []
        for i, j in self.allPath.items():
            rect = copy.deepcopy(self.info[i][5])
            rect.x -= 10
            rect.y -= 10
            rect.width = 394
            rect.height = 40
            temp.append(([rect, i]))

            pygame.draw.rect(self.win, (0, 0, 0), rect, 2, 10)
            self.BotsColor()

        while True:
            textRender = self.font.render("Click to see how it works", False, (0, 0, 0))
            self.win.blit(
                textRender,
                (
                    860 + self.dx,
                    70,
                ),
            )
            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEBUTTONDOWN and temp is not None:
                    for i, j in self.info.items():
                        if j[5].collidepoint(mousePos):
                            rect = copy.deepcopy(self.info[i][5])
                            rect.x -= 5
                            rect.y -= 5
                            rect.width = 30
                            rect.height = 30

                            prevX = j[0][0][1] * self.sizeImage[0] + self.dx
                            prevY = j[0][0][0] * self.sizeImage[1] + self.dy

                            for x in j[0]:
                                targetX = x[1] * self.sizeImage[0] + self.dx
                                targetY = x[0] * self.sizeImage[1] + self.dy
                                currentX, currentY = prevX, prevY

                                while currentX != targetX or currentY != targetY:
                                    if abs(currentX - targetX) > 1:
                                        stepX = 2 if abs(currentX - targetX) >= 2 else 1
                                        currentX += (
                                            stepX if currentX < targetX else -stepX
                                        )
                                    else:
                                        currentX = targetX

                                    if abs(currentY - targetY) > 1:
                                        stepY = 2 if abs(currentY - targetY) >= 2 else 1
                                        currentY += (
                                            stepY if currentY < targetY else -stepY
                                        )
                                    else:
                                        currentY = targetY

                                    self.win.fill((255, 255, 255))
                                    pygame.draw.rect(
                                        self.win, self.allPath[i][1], rect, 0, 4
                                    )
                                    pygame.draw.rect(self.win, (0, 0, 0), rect, 2, 4)
                                    self.win.blit(j[3], (currentX, currentY))
                                    self.DrawMap()
                                    self.RenderText()
                                    self.BotsColor()
                                    pygame.display.update()

                                prevX = targetX
                                prevY = targetY

                            self.win.fill((255, 255, 255))
                            self.win.blit(
                                j[3],
                                (
                                    j[0][-1][1] * self.sizeImage[0] + self.dx,
                                    j[0][-1][0] * self.sizeImage[1] + self.dy,
                                ),
                            )
                            self.DrawMap()
                            self.RenderText()
                            self.BotsColor()
                            for x in j[0]:
                                pygame.draw.rect(
                                    self.win,
                                    self.allPath[i][1],
                                    pygame.rect.Rect(
                                        x[1] * self.sizeImage[0] + self.dx,
                                        x[0] * self.sizeImage[1] + self.dy,
                                        self.sizeImage[0],
                                        self.sizeImage[1],
                                    ),
                                    0,
                                    2,
                                )
                                self.DrawMap()
                                pygame.display.update()
                            break
                    else:
                        for i in range(0, len(temp)):
                            if temp[i][0].collidepoint(mousePos):
                                overlaySurface = pygame.Surface(
                                    self.sizeImage, pygame.SRCALPHA
                                )
                                self.win.fill((255, 255, 255))
                                self.RenderText()
                                self.BotsColor()
                                for x in self.allPath[temp[i][1]][0]:
                                    pygame.draw.rect(
                                        self.win, (0, 0, 0), temp[i][0], 0, 10
                                    )
                                    textRender = self.font.render(
                                        self.info[temp[i][1]][7], True, (255, 255, 255)
                                    )
                                    self.win.blit(
                                        textRender,
                                        (
                                            self.sizeImage[0] * self.sizeMap[0] + 130,
                                            i * 80 + 247,
                                        ),
                                    )
                                    self.BotsColor()
                                    pygame.draw.rect(
                                        overlaySurface,
                                        self.allPath[temp[i][1]][1],
                                        pygame.Rect(
                                            0, 0, self.sizeImage[0], self.sizeImage[1]
                                        ),
                                        0,
                                        2,
                                    )
                                    self.win.blit(
                                        overlaySurface,
                                        (
                                            x[0][1] * self.sizeImage[0] + self.dx,
                                            x[0][0] * self.sizeImage[1] + self.dy,
                                        ),
                                    )
                                    self.DrawMap(False)
                                    pygame.display.update()
                                    if temp[i][1] in ["aStar", "ucs", "greedy"]:
                                        pygame.time.delay(20)
                                        continue
                                    pygame.time.delay(5)

                                for x in self.info[temp[i][1]][0]:
                                    pygame.draw.rect(
                                        self.win,
                                        (255, 0, 0),
                                        pygame.rect.Rect(
                                            x[1] * self.sizeImage[0] + self.dx,
                                            x[0] * self.sizeImage[1] + self.dy,
                                            self.sizeImage[0],
                                            self.sizeImage[1],
                                        ),
                                        0,
                                        2,
                                    )

                                    self.DrawMap(False)
                                    pygame.display.update()

                                for x in self.allPath[temp[i][1]][0]:
                                    font = pygame.font.Font(None, 20)
                                    textRender = font.render(str(x[1]), True, (0, 0, 0))
                                    self.win.blit(
                                        textRender,
                                        (
                                            x[0][1] * self.sizeImage[0]
                                            + self.dx
                                            + (
                                                self.sizeImage[0]
                                                - textRender.get_size()[0]
                                            )
                                            / 2,
                                            x[0][0] * self.sizeImage[1]
                                            + self.dy
                                            + (
                                                self.sizeImage[1]
                                                - textRender.get_size()[1]
                                            )
                                            / 2,
                                        ),
                                    )
                                    pygame.display.update()

            pygame.display.update()

    ##
    def Run(self):
        while self.running:
            if not self.menu:
                mousePos = pygame.mouse.get_pos()
                self.vec[0], self.vec[1] = 0, 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if not self.playerFinish:
                            if event.key == pygame.K_a:
                                self.vec[0] = -1
                            elif event.key == pygame.K_d:
                                self.vec[0] = 1
                            elif event.key == pygame.K_w:
                                self.vec[1] = -1
                            elif event.key == pygame.K_s:
                                self.vec[1] = 1

                        if event.key == pygame.K_ESCAPE and not self.menu:
                            self.__init__()
                            break

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.CheckOnBot(mousePos)
                        self.MovePlayer(mousePos, True)

                if self.menu:
                    continue

                if self.CheckEndGame():
                    self.endGame = True
                    self.DrawAllPathBots()
                    self.__init__()
                    continue

                self.win.fill((255, 255, 255))
                self.DrawBot()
                self.DrawPlayer()
                self.DrawMap()
                self.CheckWinBot()
                self.MovePlayer(mousePos, False)
                self.MoveBots()
                self.RenderText()
                self.fps.tick(60)
                self.time += 1 * self.speed[0]
            else:
                if self.createMap:
                    self.win.fill((255, 255, 255))
                    self.DrawRectMap()
                    self.RenderTextCreateMap()
                    self.CheckCreateMap()
                    pygame.display.update()
                    continue

                self.RenderMenu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    mousePos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.CheckMouseMenu(mousePos, True)
                self.CheckMouseMenu(mousePos, False)
            pygame.display.update()


if "__main__" == __name__:
    run = GameAI()
    run.Run()
