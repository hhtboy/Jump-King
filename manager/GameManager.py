import sys
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb
from core.Player import Player
from core.Joystick import Joystick
from core.InputController import Controller
from manager.SourceManager import SourceManager
from manager.LevelManager import LevelManager
from mapObject.Map import Map
from core.Singleton import Singleton


class GameManager(Singleton) :

    #생성자
    def __init__(self):
        self.inputController = Controller()
        self.joystick = Controller.joystick
        
        self.player_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/frog-fall.png")
        self.background_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/Background.png")
        self.background_src = self.background_src.resize((240,240))
        self.background = self.background_src.copy()
        self.wall_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/small-platform.png")

        self.myDraw = ImageDraw.Draw(self.background_src)


        self.joystick.disp.image(self.background_src)

        #player
        self.player = Player.instance()
        
        #level
        LevelManager.instance().level = 1
        LevelManager.instance().changeLevel(1)

        

    def update(self):
        command = self.inputController.getControllerInput()
        self.player.update()
        self.player.move(command)

        # Level change
        if self.player.center[1] < 10 :
            LevelManager.instance().changeLevel(2)
            self.player.position[1] = 240 - self.player.playerSize
            self.player.position[3] = 240 + self.player.playerSize

            

    def fixedUpdate(self):
        if self.player != None:
            self.player.fixedUpdate()

    def draw(self):
        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        self.player_src = self.player.animState
        #방향 전환
        if self.player.facing == "left": self.player_src = self.player_src.transpose(Image.FLIP_LEFT_RIGHT)
        drawPos = list(map((int), ((self.player.position[0] + self.player.position[2]) / 2, (self.player.position[1] + self.player.position[3]) / 2)))

        #background
        self.background_src.paste(self.background)

        #wall
        #self.background_src.paste(self.wall_src, (50, 100), self.wall_src)
        for wall in LevelManager.instance().walls:
            self.myDraw.rectangle((wall.x1, wall.y1, wall.x2, wall.y2),fill = (255,255,255,100))

        #player
        self.background_src.paste(self.player_src, (drawPos[0] - 25, drawPos[1] - 15), self.player_src)
        
        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        self.joystick.disp.image(self.background_src)


        
