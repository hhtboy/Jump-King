from mapObject.Wall import Wall
from core.Singleton import Singleton
from mapObject.Map import Map

class LevelManager(Singleton):

    level_1 = [Wall(0,240,220,240), Wall(0, 60, 150, 220), Wall(220, 240, 0, 240), Wall(150, 180, 100, 120)]
    level_2 = []
    level_3 = []
    level_4 = []
    level_5 = []

    def __init__(self):
        self.map = Map().map
        self.level = 1
        self.walls = self.level_1

    def changeLevel(self, newLevel):
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

        self.fillMap()

    # walls로 map을 채웁니다.
    def fillMap(self):
        for wall in self.walls:
            for x in range(wall.x1, wall.x2):
                #맨 위에만 1로 채웁니다.
                for y in range(wall.y1, wall.y2):
                    self.map[y][x] = 1
