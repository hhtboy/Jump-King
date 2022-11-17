from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb
from Player import Player
from Joystick import Joystick
from InputController import Controller
from SourceManager import SourceManager
import Player


class GameManager :

    #생성자
    def __init__(self):
        self.inputController = Controller()
        self.joystick = Controller.joystick

        self.frog_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/frog-fall.png")
        self.background_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/Background.png")
        self.background_src = self.background_src.resize((240,240))
        self.background = self.background_src.copy()

        #self.frog_src = self.frog_src.resize((50,50))
        #self.frog = ImageDraw.Draw(self.frog_src, "RGBA")
        #self.background = ImageDraw.Draw(self.background_src, "RGBA")

        self.joystick.disp.image(self.background_src)
        #self.joystick.disp.image(self.frog_src)

        self.player = Player.Player(self.joystick.width, self.joystick.height)
        

    def update(self):
        command = self.inputController.getControllerInput()
        self.player.update()
        self.player.move(command)
            

    def fixedUpdate(self):
        if self.player != None:
            self.player.fixedUpdate()

    def draw(self):
        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        self.frog_src = self.player.animState
        drawPos = list(map((int), self.player.center))
        self.background_src.paste(self.background)
        self.background_src.paste(self.frog_src, (drawPos[0], drawPos[1]), self.frog_src)
        
        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        self.joystick.disp.image(self.background_src)

        pass


        
