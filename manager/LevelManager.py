from mapObject.Wall import Wall
from core.Singleton import Singleton
from mapObject.Map import Map
from PIL import Image
import time

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

        self.level_1_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/level1.png").resize((240,240))
        self.level_2_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/level2.png").resize((240,240))
        self.level_3_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/level3.png").resize((240,240))
        self.level_4_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/level4.png").resize((240,240))
        self.level_5_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/level5.png").resize((240,240))
        self.level_6_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/level6.png").resize((240,240))

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

    # walls??? map??? ????????????.
    def fillMap(self):
        for wall in self.walls:
            for x in range(wall.x1, wall.x2 + 1):
                for y in range(wall.y1, wall.y2 + 1):
                    self.map[y][x] = 1

    # ????????? map??? 0?????? ?????????????????????.
    def clearMap(self):
        for wall in self.walls:
                    for x in range(wall.x1, wall.x2 + 1):
                        for y in range(wall.y1, wall.y2 + 1):
                            self.map[y][x] = 0

                            
    def get_background(self):
        if self.level == 1:
            return self.level_1_src
        elif self.level == 2:
            return self.level_2_src
        elif self.level == 3:
            return self.level_3_src
        elif self.level == 4:
            return self.level_4_src
        elif self.level == 5:
            return self.level_5_src
        else:
            return self.level_6_src
            

    def gameOver():
        print("gameOver")

        from manager.GameManager import GameManager
        GameManager.instance().gameEnding()
        GameManager.instance().gameOver = True
