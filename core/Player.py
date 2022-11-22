import numpy as np
from core.Singleton import Singleton
from manager.SourceManager import SourceManager
from manager.LevelManager import LevelManager

class Player(Singleton):
    def __init__(self):
        self.appearance = 'circle'
        #컨트롤러의 command 상태
        self.commandState = None

        #캐릭터 위치
        self.playerSize = 50
        self.position = np.array([(240 - self.playerSize) /2, (220 - self.playerSize) , (240 + self.playerSize) / 2, (220) ], dtype=np.int64)

        #캐릭터가 받는 힘의 방향
        self.direction = np.zeros(2)

        self.facing = "left"
        self.jumpGauge = 0
        self.center = np.array([(self.position[0] + self.position[2]) / 2, self.position[1]],dtype=np.int64)
        self.outline = "#FFFFFF"
        
        sourceManager = SourceManager()
        self.anim_idle = sourceManager.importIdel()
        self.anim_jump = sourceManager.importJump()
        self.anim_idleCount = 0
        self.anim_jumpCount = 0
        self.animState = self.anim_idle[0]
        self.stateList = ["idle", "charging", "jumping", "falling"]

        #캐릭터의 움직임 상태 
        self.state = self.stateList[0]

        self.isJumping = False
        self.isWalking = False

        self.levelMap = LevelManager.instance().map

    #상태 변화
    def update(self):
        self.defineAnim()
        #self.bounceCheck()
        self.checkGround()

    #물리 변화
    def fixedUpdate(self):
        #self.gravity()
        self.updateDirection()
        

    def move(self, command = None):
        if command['move'] == False:
            self.commandState = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.commandState = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                pass
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                pass
                self.position[1] += 1
                self.position[3] += 1

            if command['left_pressed']:
                if self.isJumping: return
                self.position[0] -= 5
                self.position[2] -= 5
                self.facing = "left"
                self.walk()

            if command['right_pressed']:
                if self.isJumping: return
                self.position[0] += 5
                self.position[2] += 5
                self.facing = "right"
                self.walk()
                

            if command['a_pressed']:
                self.jumpGauge += 1
                self.state = "charging"
            
            if command['a_released']:
                if self.jumpGauge > 0:
                    self.jump(self.jumpGauge)
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2], dtype=np.int64) 

    # 땅을 밟고 있지 않을 때, 중력을 받습니다.
    def gravity(self):
        #if self.isJumping:
            self.direction[1] += 2

    def walk(self):
        self.isWalking = True

    def jump(self, gauge):
        if self.isJumping:
            return
        print("jump!!")
        self.direction[1] -= min(gauge * 5 + 10, 30)
        self.isJumping = True
        if self.facing == "left":
            self.direction[0] -= 6
        else:
            self.direction[0] += 6
        self.jumpGauge = 0

    #player가 땅을 밟고 있는지 확인합니다.
    def checkGround(self):
        x,y = self.collisionCheck()
        if y <=  -1: #is ground
            self.isJumping = False
        elif y >= 0: #is jumping
            self.isJumping = True




    #발판을 뚫지 않게 캐릭터의 y좌표를 재설정합니다.
    def resetYPos(self, height):
        self.position[1] = height - self.playerSize - 1
        self.position[3] = height - 1

        self.direction[0] = 0
        self.direction[1] = 0
        self.state = "idle"



    def updateDirection(self):
        #점프 
        if self.direction[1] < 0:
            self.direction[1] += 2


        self.position[0] += self.direction[0]
        self.position[2] += self.direction[0]
        self.position[1] += self.direction[1]
        self.position[3] += self.direction[1]

    #상태에 따른 애니메이션을 정의합니다.
    def defineAnim(self):
        if self.isJumping :
            if self.direction[1] <= 0 : self.state = "jumping"
            elif self.direction[1] > 0 : self.state = "falling"

        if self.state == "idle":
            self.animState = self.anim_idle[self.anim_idleCount]
            if self.anim_idleCount >= 7:
                self.anim_idleCount = 0
            else: self.anim_idleCount += 1

        elif self.state == "jumping":
            self.animState = self.anim_jump[3]
        
        elif self.state == "falling":
            self.animState = self.anim_jump[7]

        elif self.state == "charging":
            self.animState = self.anim_jump[1]

    #Wall과의 collision을 체크합니다.
    #player가 얼마나 벽에 겹쳤는지에 대한 정보인 top, bottom, left, right를 반환합니다.
    def collisionCheck(self):
        resultX = resultY = 0
        top = bottom = self.position[1]
        left = right = self.position[0]
        flag = 0
        setFlag = 0 #top / left를 처음 세팅하기 위한 flag
        for y in range(self.position[1], self.position[3]):
            flag = 0
            for x in range(self.position[0], self.position[2]):
                if self.levelMap[y][x] == 1: # 충돌함
                    flag = 1
                    break
            #라인이 전부 0이 아닐 때 -> 
            if flag == 0:
                if top == self.position[1]: #top이 초기값이면 top 갱신
                    if setFlag == 0:
                        setFlag = 1
                        top = y
                        continue
                if setFlag == 1:
                    bottom = y + 1 #top이 이미 갱신됐다면 bottom 갱신

        setFlag = 0
        for x in range(self.position[0], self.position[2]):
            flag = 0
            for y in range(self.position[1], self.position[3]):
                if self.levelMap[y][x] == 1:
                    flag = 1
                    break
            if flag == 0:
                if left == self.position[0]:
                    if setFlag == 0:
                        setFlag = 1
                        left = x
                        continue
                if setFlag == 1:
                    right = x + 1

        print("top : "+str(top)+" / bottom : "+str(bottom) + " / left : "+str(left)+" / right : "+str(right))
        print("player pos : "+str(self.position[1]) + " / " + str(self.position[3]) + " / " + str(self.position[0]) + " / " + str(self.position[2]))

        #case 나누기
        #아래 충돌
        if self.position[1] == top:
            #왼쪽 top과 오른쪽 top을 비교해서 어느 모양인지 판별
            leftTop = bottom
            rightTop = bottom
            while self.levelMap[leftTop][self.position[0]] == 0 and leftTop <= self.position[3]:
                leftTop = leftTop + 1
            while self.levelMap[rightTop][self.position[2]] == 0 and rightTop <= self.position[3]:
                rightTop = rightTop + 1

            print(leftTop, rightTop)

            if leftTop < rightTop : # ⌞ 모양
                print(" 니은 ")
                x = self.position[0]
                y = bottom
                while self.levelMap[bottom][x] == 1:
                    x = x + 1
                resultX = x - self.position[0]

                while self.levelMap[y][x] == 0:
                    y = y + 1
                resultY = y -1 - self.position[3]
                print("result X : "+str(resultX) + " / result Y : " + str(resultY))

                
            elif leftTop > rightTop : # ⌟ 모양
                print("니은 대칭")
                x = right
                y = bottom
                while self.levelMap[y][x] == 0:
                    x = x + 1
                resultX = x - 1 - self.position[2]
                while self.levelMap[y][x - 1] == 0:
                    y = y + 1
                resultY = y -1 - self.position[3]
                print("result X : "+str(resultX) + " / result Y : " + str(resultY))

            else : # 1자 평지
                print("일자")
                resultX = 0
                resultY = bottom -1 - self.position[3]
                print("result X : "+str(resultX) + " / result Y : " + str(resultY))
        else: #천장 충돌
            pass

        self.resetPos(resultX, resultY + 1)

        return resultX, resultY




    #전달받은 위치만큼 player의 position을 수정합니다.
    def resetPos(self,x, y):
        self.position[0] = self.position[0] + x
        self.position[2] = self.position[2] + x

        self.position[1] = self.position[1] + y
        self.position[3] = self.position[3] + y
        
        
        
        
    # 벽과 부딫이는지 확인합니다.
    def bounceCheck(self):
        for y in range(self.position[1], self.position[3]):
            if self.facing == "left":
                for x in range(self.position[2] - 1, self.position[0], -1):
                    if self.levelMap[y][x] == 2:
                        self.resetXPos(x)
                        self.bounce()
                    else: self.bouncing = False
            else:
                for x in range(self.position[0], self.position[2]):
                    if self.levelMap[y][x] == 2:
                        self.resetXPos(x)
                        self.bounce()
                    else: self.bouncing = False

    def resetXPos(self, xPos):
        if self.facing == "left":
            self.position[0] = xPos
            self.position[2] = xPos + self.playerSize
        else :
            self.position[2] = xPos
            self.position[0] = xPos - self.playerSize
                
    def bounce(self):
        self.bouncing = True
        if self.isJumping:
            self.direction[0] = - (self.direction[0])
                


    def min(a,b):
        if a<b: return a
        else: return b
            
        
