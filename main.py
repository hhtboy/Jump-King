from PIL import Image, ImageDraw, ImageFont
import time
import random
import os
#import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from Joystick import Joystick
from GameManager import GameManager

def main():
    gameManager = GameManager()
   

    while True:
        
        gameManager.update()
        gameManager.fixedUpdate()
        gameManager.draw()


if __name__ == '__main__':
    main()