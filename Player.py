import numpy as np
from SourceManager import SourceManager

class Player:
    def __init__(self, width, height):
        self.appearance = 'circle'
        #컨트롤러의 command 상태
        self.commandState = None

        #캐릭터 위치
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])

        #캐릭터가 받는 힘의 방향
        self.direction = np.zeros(2)

        self.facing = "left"
        self.jumpGauge = 0
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"
        
        self.anim = SourceManager.importSrc()
        self.stateList = ["idle", "charge", "jumping", "falling"]

        #캐릭터의 움직임 상태 
        self.state = self.stateList[0]
        self.animCount = 0
        self.animState = self.anim[self.animCount]


        self.isJumping = False

    #상태 변화
    def update(self):
        self.checkGround()
        self.defineAnim()

    #물리 변화
    def fixedUpdate(self):
        self.gravity()
        self.updateDirection()
        

    def move(self, command = None):
        if command['move'] == False:
            self.commandState = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.commandState = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5
                self.facing = "left"
                
            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5
                self.facing = "right"
                

            if command['a_pressed']:
                self.jumpGauge += 1
                print(self.jumpGauge)
            
            if command['a_released']:
                if self.jumpGauge > 0:
                    self.jump(self.jumpGauge)
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 

    # 땅을 밟고 있지 않을 때, 중력을 받습니다.
    def gravity(self):
        if self.isJumping:
            self.direction[1] += 2

            
                

    def jump(self, gauge):
        if self.isJumping:
            return
        print("jump!!")
        self.direction[1] -= min(gauge * 5 + 10, 30)
        self.isJumping = True
        if self.facing == "left":
            print("left jump")
            self.direction[0] -= 5
        else:
            print("right jump")
            self.direction[0] += 5
        self.jumpGauge = 0

    #player가 땅을 밟고 있는지 확인합니다.
    def checkGround(self):
        if self.position[1] >= 200:
            self.isJumping = False
            self.state = "idle"
            self.resetYPos()
        else:
            self.isJumping = True

    def resetYPos(self):
        self.position[1] = 200
        self.position[3] = 240

        self.direction[0] = 0
        self.direction[1] = 0


    def updateDirection(self):
        #점프 
        if self.direction[1] < 0:
            self.direction[1] += 2


        self.position[0] += self.direction[0]
        self.position[2] += self.direction[0]
        self.position[1] += self.direction[1]
        self.position[3] += self.direction[1]

    def defineAnim(self):
        if self.isJumping :
            if self.direction[1] <= 0 : self.state = "jumping"
            else : self.state = "falling"

        if self.state == "idle":
            self.animState = self.anim[self.animCount]
            if self.animCount >= 7:
                self.animCount = 0
            else: self.animCount += 1

        elif self.state == "jumping":
            self.animState = self.anim[8]
        
        else : self.animState = self.anim[9]

        print(self.state)

    def min(a,b):
        if a<b: return a
        else: return b
            
        
