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
        self.playerSize = 30
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
        self.anim_dust = sourceManager.importDust()
        self.anim_idleCount = 0
        self.anim_jumpCount = 0
        self.anim_dustCount = 0
        #dust animation flag
        self.dustFlag = False
        self.dustPos = self.center
        self.animState = self.anim_idle[0]
        self.stateList = ["idle", "charging", "jumping", "falling"]

        #캐릭터의 움직임 상태 
        self.state = self.stateList[0]

        self.isJumping = False
        self.isWalking = False


        self.levelMap = LevelManager.instance().map

    #상태 변화
    def update(self):
        pass

    #물리 변화
    def fixedUpdate(self):
        if LevelManager.instance().level == 6 and self.position[3] < 70 and self.position[0] < 40:
            LevelManager.gameOver()
        if self.position[1] < 5:
            self.anim_dustCount = 0
            self.dustFlag = False
            LevelManager.instance().levelUp()
            self.position[3] = 240  - (5 - self.position[1])
            self.position[1] = 240 - self.playerSize  - (5 - self.position[1])

        elif self.position[3] > 240:
            self.anim_dustCount = 0
            self.dustFlag = False
            LevelManager.instance().levelDown()
            self.position[1] = 5  
            self.position[3] = 5 + self.playerSize 

        else :
            self.gravity()
            self.updateDirection()
            self.updateCollision()
            self.defineAnim()
        

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
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                if self.isJumping or (self.state == "charging"): return
                self.position[0] -= 5
                self.position[2] -= 5
                self.facing = "left"
                self.walk()

            if command['right_pressed']:
                if self.isJumping or (self.state == "charging"): return
                self.position[0] += 5
                self.position[2] += 5
                self.facing = "right"
                self.walk()
                

            if command['a_pressed']:
                if not self.isJumping :
                    self.jumpGauge += 1
                    self.state = "charging"
            
            if command['a_released']:
                if self.jumpGauge > 0:
                    self.jump(self.jumpGauge)
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2], dtype=np.int64) 

    # 땅을 밟고 있지 않을 때, 중력을 받습니다.
    def gravity(self):
        if self.isJumping:
            #중력 가속도의 상한을 설정합니다.
            if self.direction[1] >= 15:
                return
            self.direction[1] += 2
            #print(self.direction[1])

    def walk(self):
        self.isWalking = True

    def jump(self, gauge):
        if self.isJumping:
            return
        #print("jump!!")
        self.dustFlag = True
        self.dustPos = self.center
        self.direction[1] -= min(gauge * 5 + 10, 30)
        self.isJumping = True
        if self.facing == "left":
            self.direction[0] -= 10
        else:
            self.direction[0] += 10
        self.jumpGauge = 0

    #player의 collision을 체크하고 위치를 reset시킵니다.
    def updateCollision(self):
        if self.position[1] < 5: return
        x,y = self.collisionCheck()
        if (x == 100) and (y == 100): return
        self.resetPos(x,y)
        #print(str(x) + " / " + str(y))
        #print("player 좌표 : " + str(self.position[0]) + " , " + str(self.position[3]))
        if y <=  -1: #is ground
            self.isJumping = False
            self.direction[0] = 0
            self.direction[1] = 0
            if not self.state == "charging":
                self.state = "idle"
        elif y >= 0: #is jumping
            self.isJumping = True

            if y > 0 : #천장과 충돌
                self.direction[1] = 0

        if x != 0: #벽 충돌로 튕겨야 함
            self.direction[0] = -int(self.direction[0] * 0.6)




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
        #dust
        if self.dustFlag:
            if self.anim_dustCount >= 4:
                self.anim_dustCount = 0
                self.dustFlag = False
            else:
                self.anim_dustCount = self.anim_dustCount + 1
        
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
        if self.position[3] > 240: return 100, 100
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
            if x > 240: x = 240
            flag = 0
            for y in range(self.position[1], self.position[3]):
                if y > 240 : y = 240
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


        #case 나누기
        #천장 ㄱ / 대칭 ㄱ
        if (self.position[1] == top) and (self.position[1] == bottom) and (self.position[0] == left) and (self.position[0] == right): #ㄱ / ㄴ
            isCeiling = False
            x = self.position[0]
            y = self.position[1]
            while self.levelMap[y][x] == 1 and x <= self.position[2]:
                x = x + 1
            if x == self.position[2] + 1:
                isCeiling = True
            if isCeiling == True:
                # 대칭 ㄱ
                if self.levelMap[self.position[0]][self.position[3]] == 1:
                    #print("완전 대칭 ㄱ")
                    x = self.position[2]
                    y = self.position[1]
                    while self.levelMap[y][x] == 1:
                        y = y + 1
                    x = self.position[0]
                    while self.position[y][x] == 1:
                        x = x + 1
                    resultX = x - self.position[0]
                    resultY = y - self.position[1]
                    return resultX, resultY
                        

                # ㄱ
                else:
                    #print("완전 ㄱ")
                    x = self.position[0]
                    y = self.position[1]
                    while self.levelMap[y][x] == 1:
                        y = y + 1
                        if y == 241: # index 초과 방지
                            y = 0
                            break
                    while self.levelMap[y][x] == 1:
                        x = x + 1
                        if x == 241: # index 초과 방지
                            x = 0
                            break
                    resultX = x - 1 - self.position[2]
                    resultY = y - self.position[1]
                    return resultX, resultY

        #아래 충돌
        if (self.position[1] == top) :
            #왼쪽 top과 오른쪽 top을 비교해서 어느 모양인지 판별
            leftTop = bottom
            rightTop = bottom
            if self.position[2] > 240: 
                self.position[0] = 240 -self.playerSize
                self.position[2] = 240
            while self.levelMap[leftTop][self.position[0]] == 0 and leftTop <= self.position[3] and leftTop < 240:
                leftTop = leftTop + 1
            while self.levelMap[rightTop][self.position[2]] == 0 and rightTop <= self.position[3] and rightTop < 240:
                rightTop = rightTop + 1


            if leftTop == top and rightTop == self.position[3] + 1: # ㅣ 모양(왼쪽)
                #print("왼쪽 일자")
                x = self.position[0]
                y = bottom
                while self.levelMap[y][x] == 1:
                    x = x + 1
                resultX = x - self.position[0]
                resultY = 0

            elif rightTop == top and leftTop == self.position[3] + 1: # ㅣ 모양(오른쪽)
                #print("오른쪽 일자")
                x = self.position[2]
                y = bottom
                while self.levelMap[y][x] == 1:
                    x = x - 1
                resultX = x - self.position[2]
                resultY = 0
                
            elif leftTop < rightTop : # ⌞ 모양
                x = self.position[0]
                y = self.position[3]
                while self.levelMap[leftTop][x] == 1:
                    x = x + 1
                if self.levelMap[self.position[3]][x] != 0:  #끝까지 없으면 ㄴ 모양 아님
                    
                    #print(" 니은 ")
                    
                    x = self.position[0]
                    y = bottom
                    while self.levelMap[bottom][x] == 1:
                        x = x + 1
                    resultX = x - self.position[0]

                    while self.levelMap[y][x] == 0:
                        y = y + 1
                    resultY = y -1 - self.position[3]
                else:
                    # print("왼쪽 절벽")
                    while self.levelMap[y][self.position[0]] == 1:
                        y = y - 1
                    if x - 1 - self.position[0] > self.playerSize / 3:
                        resultY = y  - self.position[3]
                        resultX = 0
                    else:
                        x = x - 1 - self.position[0]
                        resultY = 0
                        resultX = x

                
            elif leftTop > rightTop : # ⌟ 모양
                x = self.position[2]
                while self.levelMap[rightTop][x] == 1:
                    x = x - 1
                if self.levelMap[self.position[3]][x] != 0:
                    print("니은 대칭")
                    x = right
                    y = bottom
                    while self.levelMap[y][x] == 0:
                        x = x + 1
                    resultX = x - 1 - self.position[2]
                    while self.levelMap[y][x - 1] == 0:
                        y = y + 1
                    resultY = y - 1 - self.position[3]
                else:
                    #print("오른쪽 절벽")
                    if self.position[2] - x - 1 > self.playerSize / 3:
                        resultY = y - self.position[3]
                        resultX = 0
                    else:
                        x = x + 1 - self.position[2]
                        resultY = 0
                        resultX = x


            elif leftTop == rightTop and leftTop == self.position[3] + 1: #공중
                
                #print("공중")
                resultX = 0
                resultY = 0

            else : # 1자 평지
                #print("일자")
                resultX = 0
                resultY = bottom -1 - self.position[3]

        else: #천장 충돌 
            if self.levelMap[self.position[1]][self.position[0]] == 1:
                if self.levelMap[self.position[1]][self.position[2]] == 1:
                    x = self.position[2]
                    y = self.position[1]
                    while self.levelMap[y][x] == 1 and y <= self.position[3]:
                        y = y + 1
                    if self.levelMap[y - 1][x] == 0: #넘겨줘야 함
                        #print("pass 2")
                        pass
                    else:
                        #일자 또는 완전 ㄱ대칭
                        if top == self.position[1]:
                            #완전 ㄱ 대칭
                            #print("완전 ㄱ 대칭")
                            x = self.position[0]
                            y = self.position[3]
                            while self.levelMap[y][x] == 1:
                                x = x + 1
                            resultX = x - self.position[0]
                            y = self.position[1]
                            while self.levelMap[y][x] == 1:
                                y = y + 1
                            resultY = y - self.position[1]
                            return resultX, resultY

                        else:
                            print("pass")
                            resultX = 0
                            resultY = top - self.position[1] 
                else:
                    # if self.levelMap[self.position[1]][left] == 0:
                    #     #대칭 ㄱ
                    #     #print("대칭 ㄱ")
                    #     self.help()
                    #     resultX = left - self.position[0]
                    #     y = self.position[1]
                    #     while self.levelMap[y][left] == 1:
                    #         y = y + 1
                    #     resultY = y - self.position[1]
                    #     return resultX, resultY
                    
                    #else:
                    #왼쪽 일자 벽
                    #print("왼쪽 일자 벽")
                    resultY = 0
                    resultX = left - self.position[0]
                    x = self.position[0]
                    y = self.position[1]
                    while self.levelMap[y][x]:
                        y = y + 1
                    y = y - self.position[1]
                    if (y < 5):
                        resultY = y
                        resultX = 0
                    return resultX, resultY
                        
                    

            if self.levelMap[top - 1][right] == 1: 
                resultY = top - self.position[1] 

                # 1자 천장(완전 일자 포함)
                if right - int((self.position[0] + self.position[2]) / 2) < 3 or right - int((self.position[0] + self.position[2]) / 2) > -3:
                    #print("1자 천장")
                    resultX = 0

                #1자 천장 벽
                else:
                    #print("1자 천장 벽")
                    resultX = self.position[2] - right + 1
            else:
                #ㄱ 자
                #print("ㄱ 자")
                x = right
                y = top - 1
                while self.levelMap[top - 1][x] == 0:
                    x = x + 1
                resultX = x - 1 - self.position[2]
                while self.levelMap[y][right] == 0:
                    y = y - 1
                resultY = y + 1 - self.position[1]

        return resultX, resultY


    #전달받은 위치만큼 player의 position을 수정합니다.
    def resetPos(self,x, y):
        self.position[0] = self.position[0] + x
        self.position[2] = self.position[2] + x

        if y == -1: return

        self.position[1] = self.position[1] + y + 1
        self.position[3] = self.position[3] + y + 1

        
        

    def min(a,b):
        if a<b: return a
        else: return b

    def help(self):
        for x in range(self.position[0], self.position[2]):
            for y in range(self.position[1],self.position[3]):
                print(self.levelMap[y][x],end = "")
            print()
