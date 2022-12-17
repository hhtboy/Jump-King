from PIL import Image, ImageDraw, ImageFont
import time
import random
import os
#import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from manager.GameManager import GameManager
from core.Player import Player

def main():
    gameManager = GameManager.instance()

    gameManager.gameStart()
   
    while gameManager.gameOver != True:
        #상태, 가속도, 애니메이션 업데이트
        gameManager.update()
        #위치 업데이트
        gameManager.fixedUpdate()
        #그리기
        gameManager.draw()


if __name__ == '__main__':
    main()