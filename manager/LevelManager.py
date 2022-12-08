from mapObject.Wall import Wall
from core.Singleton import Singleton
from mapObject.Map import Map
from GameManager import GameManager

class LevelManager(Singleton):

    level_1 = [Wall(0,10,0,240), Wall(230, 240, 0, 240), Wall(0,240,220,240), Wall(0, 50, 140, 220), Wall(190, 240, 140, 220), Wall(90, 150, 60, 90)]
    level_2 = [Wall(0,10,0,240), Wall(230, 240, 0, 240), Wall(200, 240, 220, 240), Wall(0,40, 220, 240), Wall(110, 160, 140, 160), Wall(50, 80, 80,100), Wall(200, 230, 50, 70) ]
    level_3 = [Wall(0,10,0,240), Wall(230, 240, 0, 240), Wall(10,70,200,220), Wall(100, 130, 0, 130), Wall(10, 40, 120, 140), Wall(85, 100, 40, 60) ]
    level_4 = [Wall(0,10,0,240), Wall(230, 240, 0, 240), Wall(100,130, 140, 240), Wall(0, 35, 160, 175), Wall(0, 40, 60, 80)]
    level_5 = [Wall(0,10,0,240), Wall(230, 240, 0, 240), Wall(70, 100, 180, 200), Wall(165,195, 170, 190), Wall(50, 80, 110, 130), Wall(200, 230, 50, 70) ]
    level_6 = [Wall(0,10,0,240), Wall(230, 240, 0, 240), Wall(10, 90, 195, 215), Wall(185, 230, 130, 150), Wall(10, 100, 60, 100)]

    def __init__(self):
        self.map = Map().map
        self.level = 1
        self.walls = self.level_1

    def changeLevel(self, newLevel):
        self.clearMap()
        self.level = newLevel

        if newLevel == 1:
            self.walls = self.level_1
            print("Level : 1")
        elif newLevel == 2:
            self.walls = self.level_2
            print("Level : 2")
        elif newLevel == 3:
            self.walls = self.level_3
            print("Level : 3")
        elif newLevel == 4:
            self.walls = self.level_4
            print("Level : 4")
        elif newLevel == 5:
            self.walls = self.level_5
            print("Level : 5")
        elif newLevel == 6:
            self.walls = self.level_6
            print("Level : 6")
        self.fillMap()

    def levelUp(self):
        if self.level < 6:
            self.changeLevel(self.level + 1)

    def levelDown(self):
        if self.level > 1:
            self.changeLevel(self.level - 1)

    # walls로 map을 채웁니다.
    def fillMap(self):
        for wall in self.walls:
            for x in range(wall.x1, wall.x2 + 1):
                for y in range(wall.y1, wall.y2 + 1):
                    self.map[y][x] = 1

    # 채워진 map을 0으로 초기화시킵니다.
    def clearMap(self):
        for wall in self.walls:
                    for x in range(wall.x1, wall.x2 + 1):
                        for y in range(wall.y1, wall.y2 + 1):
                            self.map[y][x] = 0

    def gameOver():
        print("gameOver")
        GameManager.instance().gameOver = True
