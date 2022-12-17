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
import time


class GameManager(Singleton) :

    #생성자
    def __init__(self):
        self.gameOver = False
        self.inputController = Controller()
        self.joystick = Controller.joystick
        
        #기초 이미지 소스 가져오기
        self.player_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/frog-fall.png")
        self.background_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/Background.png")
        self.background_src = self.background_src.resize((240,240))
        self.background = self.background_src.copy()
        self.wall_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/small-platform.png")
        self.starting_src = Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/small-platform.png")

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

            

    def fixedUpdate(self):
        if self.player != None:
            self.player.fixedUpdate()

    def draw(self):
        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        self.player_src = self.player.animState
        self.dust_src = self.player.anim_dust[self.player.anim_dustCount]
        #방향 전환
        if self.player.facing == "left": self.player_src = self.player_src.transpose(Image.FLIP_LEFT_RIGHT)
        drawPos = list(map((int), ((self.player.position[0] + self.player.position[2]) / 2, (self.player.position[1] + self.player.position[3]) / 2)))

        #background
        self.background_src.paste(self.background)

        #wall
        #self.background_src.paste(self.wall_src, (50, 100), self.wall_src)
        for wall in LevelManager.instance().walls:
            self.myDraw.rectangle((wall.x1, wall.y1, wall.x2, wall.y2),fill = (255,255,255,100))

        #dust
        if self.player.dustFlag:
            self.background_src.paste(self.dust_src, (self.player.dustPos[0] - 15, self.player.dustPos[1]), self.dust_src)
            
        #player
        self.background_src.paste(self.player_src, (drawPos[0] - 15, drawPos[1] - 15), self.player_src)

        #score 이미지 폰트를 사용해서 점수를 표시합니다. 점수는 높이로 환산돼서 표시합니다.
        fontsize = 15
        fnt = ImageFont.truetype("DejaVuSans-BoldOblique.ttf", fontsize, encoding="UTF-8")
        score = round(((240 - self.player.position[1] -50) + (LevelManager.instance().level - 1) * 240) / 10, 1)
        text = "Score : " + str(score) + " m"
        tw, th = fnt.getsize(text)
        self.myDraw.text((70-tw/2, 10-int(fnt.size/2)), text, font=fnt, fill="red")
        self.myDraw = ImageDraw.Draw(self.background_src)

        
        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        self.joystick.disp.image(self.background_src)

    #게임 시작시 호출합니다. 사용자가 키 입력을 하면 메인 루프가 실행됩니다.
    def gameStart(self):
        self.joystick.disp.image(self.starting_src)
        count = 0
        flag = 0
        text = "press A to start"
        fontsize = 20
        fnt = ImageFont.truetype("DejaVuSans-BoldOblique.ttf", fontsize, encoding="UTF-8")
        tw, th = fnt.getsize(text)
        while True:
            if count > 4:
                count = 0
                if flag: flag = 0
                else: flag = 1
            else:
                count = count + 1

            if flag:
                self.background_src.paste(self.background)
            else:
                self.myDraw.text((120-tw/2, 120-int(fnt.size/2)), text, font=fnt, fill="red")
                self.myDraw = ImageDraw.Draw(self.background_src)

            self.joystick.disp.image(self.background_src)

            #키 입력을 탐지합니다
            input = self.inputController.getControllerInput()
            if input["a_pressed"]:
                break

        sceneChange(self)
        
        
    def gameEnding(self):
        size = 240
        #줌 인
        for i in range (20):
            time.sleep(0.01)
            self.background_src = self.background_src.crop((0,0,size - 1, size - 1)).resize((240,240))
            size = size - 1
            self.joystick.disp.image(self.background_src)
        print(self.background_src.size)

        sceneChange(self)

        # 엔딩 글자 띄우기
        fontsize = 18
        fnt = ImageFont.truetype("DejaVuSans-BoldOblique.ttf", fontsize, encoding="UTF-8")
        text = "Thank you for playing!!"
        tw, th = fnt.getsize(text)
        draw = ImageDraw.Draw(self.background_src)
        draw.text((120-tw/2, 120-int(fnt.size/2)), text, font=fnt, fill="red")
        self.joystick.disp.image(self.background_src)
        time.sleep(1)

        exit(0)

#게임 시작 시, 종료 시 씬 바꾸기
def sceneChange(self):
    draw = ImageDraw.Draw(self.background_src)
    for i in range (1, 21):
        time.sleep(0.1)
        draw.rectangle((0,0,240,i * 12), fill =(0, 0, 0,100))
        self.joystick.disp.image(self.background_src)

        
