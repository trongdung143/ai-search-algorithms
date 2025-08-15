import pygame
import random
import numpy as np
from collections import deque
import copy
import queue
from heapq import heappush, heappop
from queue import PriorityQueue


class GameAI:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1300, 820))
        pygame.display.set_caption("22119054_LuuTrongDung, . . ._DaoNguyenPhuc")
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
            "select the region",
            "After selected a region",
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
        self.posStart = [5, 5]
        self.posEnd = [26, 19]
        self.movePlayer = 0
        self.skipPlayer = pygame.rect.Rect(
            self.sizeImage[0] * self.sizeMap[0] + 320, 147, 0, 0
        )
        self.pathG = {}
        self.endGame = False
        self.player = [5, 5]
        self.textPlayer = "Player"
        self.vec = [0, 0]
        self.playerFinish = False
        self.activeAllBots = [pygame.rect.Rect(870, 200, 20, 20), (255, 0, 0), False]
        self.info = {
            # "dfs": [
            #     [],
            #     0,
            #     False,
            #     pygame.transform.scale(
            #         pygame.image.load("images/dfs.png"),
            #         (self.sizeImage[0], self.sizeImage[1]),
            #     ),
            #     (255, 0, 0),
            #     pygame.rect.Rect(870, 1 * 100 + 150, 20, 20),
            #     False,
            #     "Dfs",
            #     0,
            # ],
            "bfs": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/bfs.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 2 * 100 + 150, 20, 20),
                True,
                "Bfs",
                0,
            ],
            # "hillclimbing": [
            #     [],
            #     0,
            #     False,
            #     pygame.transform.scale(
            #         pygame.image.load("images/hillclimbing.png"),
            #         (self.sizeImage[0], self.sizeImage[1]),
            #     ),
            #     (255, 0, 0),
            #     pygame.rect.Rect(870, 3 * 100 + 150, 20, 20),
            #     False,
            #     "Hcb",
            #     0,
            # ],
            "aStar": [
                [],
                0,
                False,
                pygame.transform.scale(
                    pygame.image.load("images/astar.png"),
                    (self.sizeImage[0], self.sizeImage[1]),
                ),
                (255, 0, 0),
                pygame.rect.Rect(870, 4 * 100 + 150, 20, 20),
                True,
                "A*",
                0,
            ],
            # "greedy": [
            #     [],
            #     0,
            #     False,
            #     pygame.transform.scale(
            #         pygame.image.load("images/greedy.png"),
            #         (self.sizeImage[0], self.sizeImage[1]),
            #     ),
            #     (255, 0, 0),
            #     pygame.rect.Rect(870, 5 * 100 + 150, 20, 20),
            #     False,
            #     "Greedy",
            #     0,
            # ],
            # "ucs": [
            #     [],
            #     0,
            #     False,
            #     pygame.transform.scale(
            #         pygame.image.load("images/ucs.png"),
            #         (self.sizeImage[0], self.sizeImage[1]),
            #     ),
            #     (255, 0, 0),
            #     pygame.rect.Rect(870, 6 * 100 + 150, 20, 20),
            #     False,
            #     "Ucs",
            #     0,
            # ],
        }
        self.allPath = {
            # "dfs": [[], (95, 87, 78, 130)],
            "bfs": [[], (174, 174, 255, 130)],
            # "hillclimbing": [[], (70, 94, 86, 130)],
            "aStar": [[], (16, 102, 114, 130)],
            # "greedy": [[], (255, 105, 180, 130)],
            # "ucs": [[], (58, 58, 58, 130)],
        }
        self.heuristics = {
            "hillclimbing": [],
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
        ]

    def Heuristic(self, current):
        return abs(current[0] - self.posEnd[0]) + abs(current[1] - self.posEnd[1])

    def Bfs(self):
        que = queue.Queue()
        que.put(tuple(self.posStart))
        visited = set()
        visited.add(tuple(self.posStart))
        parent = {}
        parent[tuple(self.posStart)] = None
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        allPath = [tuple(self.posStart)]
        while not que.empty():
            x, y = que.get()
            if (x, y) == tuple(self.posEnd):

                break
            random.shuffle(moves)
            for d in moves:
                nx, ny = x + d[0], y + d[1]

                if 0 <= nx < self.sizeMap[0] and 0 <= ny < self.sizeMap[1]:
                    if (nx, ny) not in visited and self.map[nx][ny] == 0:
                        visited.add((nx, ny))
                        que.put((nx, ny))
                        allPath.append((nx, ny))
                        parent[(nx, ny)] = (x, y)

        current = tuple(self.posEnd)
        allPath.append(tuple(self.posEnd))
        self.allPath["bfs"][0] = allPath
        while current:
            self.info["bfs"][0].append(current)
            try:
                current = parent[current]
            except:
                return False
        self.info["bfs"][0].reverse()
        return True

    def Graph(self):
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        que = queue.Queue()
        que.put(tuple(self.posStart))
        visited = set()
        while not que.empty():
            current = que.get()
            visited.add(current)
            temp = []
            g = []
            tempVisited = set()
            for d in moves:
                x, y = current[0] + d[0], current[1] + d[1]
                if (
                    0 <= x < self.sizeMap[0]
                    and 0 <= y < self.sizeMap[1]
                    and self.map[x][y] == 0
                    # and (x, y) not in visited
                ):
                    temp.append((x, y))
                    tempVisited.add((x, y))

            for i in temp:
                path = [i]
                count = None

                while count != 0:
                    x, y = path[-1]
                    count = 0
                    nextMove = None
                    for d in moves:
                        nx, ny = x + d[0], y + d[1]
                        if (
                            0 <= nx < self.sizeMap[0]
                            and 0 <= ny < self.sizeMap[1]
                            and self.map[nx][ny] == 0
                            and (nx, ny) not in tempVisited
                            and (nx, ny) not in visited
                        ):
                            count += 1
                            nextMove = (nx, ny)

                    if [x, y] == self.posEnd:
                        que.put((x, y))
                        g.append((x, y))
                        break

                    if count >= 2:
                        if (x, y) not in visited:
                            tempVisited.add((x, y))
                            que.put((x, y))
                            g.append((x, y))
                        break

                    elif count == 1:
                        path.append(nextMove)
                        tempVisited.add((nextMove))
            self.graph[current] = g

    def FindGn(self):
        for i, j in self.graph.items():
            que = queue.Queue()
            que.put(tuple(self.posStart))
            visited = set()
            visited.add(tuple(self.posStart))
            parent = {}
            parent[tuple(self.posStart)] = None
            moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            allPath = [tuple(self.posStart)]
            while not que.empty():
                x, y = que.get()
                if (x, y) == i:
                    break
                random.shuffle(moves)
                for d in moves:
                    nx, ny = x + d[0], y + d[1]

                    if 0 <= nx < self.sizeMap[0] and 0 <= ny < self.sizeMap[1]:
                        if (nx, ny) not in visited and self.map[nx][ny] == 0:
                            visited.add((nx, ny))
                            que.put((nx, ny))
                            allPath.append((nx, ny))
                            parent[(nx, ny)] = (x, y)

            current = i
            temp = []
            while current:
                temp.append(current)
                current = parent[current]
            temp.reverse()
            self.pathG[i] = temp

    def CheckWinBot(self):
        for i, j in self.info.items():
            if self.info[i][1] == len(self.info[i][0]) - 1 and not self.info[i][2]:
                if self.info[i][0][-1] == tuple(self.posEnd):
                    self.info[i][7] += " YES STEP: " + str(len(self.info[i][0]) - 1)
                    self.info[i][2] = True
                else:
                    self.info[i][7] += " NO STEP: " + str(len(self.info[i][0]) - 1)
                    self.info[i][2] = True

    def FindIntersection(self):
        openList = []
        closedList = set()
        heappush(
            openList,
            (
                self.Heuristic(self.posStart) + 0,
                0,
                tuple(self.posStart),
                (-1, -1),
                [self.posStart],
            ),
        )
        dic = {
            tuple(self.posStart): [(-1, -1), [self.posStart]],
        }
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        while openList:
            fn, gn, current, (px, py), path = heappop(openList)
            if current == tuple(self.posEnd):
                a = tuple(self.posEnd)
                while a != (-1, -1):
                    a, path = dic[a]
                    path.reverse()
                    for i in path:
                        if i not in self.info["aStar"][0]:
                            self.info["aStar"][0].append(tuple(i))
                self.info["aStar"][0].reverse()
                return
            visited = set()
            visited.add(current)
            closedList.add(current)
            temp = []
            for d in moves:
                x, y = current[0] + d[0], current[1] + d[1]
                if (
                    0 <= x < self.sizeMap[0]
                    and 0 <= y < self.sizeMap[1]
                    and self.map[x][y] == 0
                    and (x, y) not in visited
                    and (x, y) not in closedList
                ):
                    temp.append([x, y])
                    visited.add((x, y))

            for i in temp:
                p = [i]
                count = None
                end = False
                while count != 0 and not end:
                    x, y = p[-1]
                    count = 0
                    nextMove = []

                    for d in moves:
                        nx, ny = x + d[0], y + d[1]
                        if (
                            0 <= nx < self.sizeMap[0]
                            and 0 <= ny < self.sizeMap[1]
                            and self.map[nx][ny] == 0
                            and (nx, ny) not in visited
                            and (x, y) not in closedList
                        ):
                            if [nx, ny] == self.posEnd:
                                p.append([nx, ny])
                                heappush(
                                    openList,
                                    (
                                        gn + len(p) + 0,
                                        gn + len(p),
                                        tuple(self.posEnd),
                                        current,
                                        p,
                                    ),
                                )
                                end = True
                                dic[tuple(self.posEnd)] = (current, p)
                                break
                            count += 1
                            nextMove.append([nx, ny])

                    if count >= 2 and (x, y) not in closedList:
                        for c in openList:
                            if c[2] == (x, y) and c[0] > (
                                self.Heuristic([x, y]) + c[1] + len(p)
                            ):
                                c[0] = self.Heuristic([x, y]) + gn + len(p)
                                c[1] = len(p) + gn
                                c[3] = current
                                c[4] = p
                                dic[(x, y)] = (current, p)
                        else:
                            heappush(
                                openList,
                                (
                                    len(p) + gn + self.Heuristic([x, y]),
                                    len(p) + gn,
                                    (x, y),
                                    current,
                                    p,
                                ),
                            )
                            dic[(x, y)] = (current, p)
                        break

                    elif count == 1:
                        p.append(tuple(nextMove[0]))
                        visited.add(tuple(nextMove[0]))

    def AStar(self):
        open_list = PriorityQueue()
        open_list.put((0, tuple(self.posStart)))

        g_cost = {tuple(self.posStart): 0}
        f_cost = {tuple(self.posStart): self.Heuristic(self.posStart)}
        parents = {tuple(self.posStart): None}

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while not open_list.empty():
            _, current = open_list.get()

            if current == tuple(self.posEnd):
                path = []
                while current is not None:
                    path.append(current)
                    current = parents[current]
                self.info["aStar"][0] = path[::-1]
                return

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if (
                    0 <= neighbor[0] < self.sizeMap[0]
                    and 0 <= neighbor[1] < self.sizeMap[1]
                    and self.map[neighbor[0]][neighbor[1]] == 0
                ):
                    tentative_g_cost = g_cost[current] + 1

                    if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                        g_cost[neighbor] = tentative_g_cost
                        f_cost[neighbor] = tentative_g_cost + self.Heuristic(neighbor)
                        parents[neighbor] = current
                        open_list.put((f_cost[neighbor], neighbor))

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

    def DrawMap(self):
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
        for i in range(0, self.sizeMap[0]):
            for j in range(0, self.sizeMap[1]):
                if self.map[i][j] == 1:
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

    def DrawBot(self):
        for i, j in self.info.items():
            if (j[0][j[1]][0], j[0][j[1]][1]) != tuple(self.posEnd):
                self.win.blit(
                    j[3],
                    (
                        j[0][j[1]][1] * self.sizeImage[0] + self.dx,
                        j[0][j[1]][0] * self.sizeImage[1] + self.dy,
                    ),
                )

    def MoveBots(self):
        for i, j in self.info.items():
            if not self.info[i][2] and self.info[i][6]:
                self.info[i][8] += self.speed[0]
                if self.info[i][8] // 10 > self.info[i][1]:
                    self.info[i][1] += 1

    def Run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.win.fill((255, 255, 255))
            self.DrawMap()
            self.DrawBot()
            self.MoveBots()
            self.fps.tick(60)
            pygame.display.update()


if "__main__" == __name__:
    run = GameAI()
    run.CreateMap()
    # run.FindIntersection()
    run.Bfs()
    # print(run.info["aStar"][0])
    # run.Graph()
    # run.FindGn()
    run.AStar()
    # for i, j in run.graph.items():
    #     if j != []:
    #         print(j)
    run.Run()
