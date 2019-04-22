import pygame
import random

class square:
    def __init__(self,xPos,yPos,ready,colour):
        self.xPos = xPos
        self.yPos = yPos
        self.ready = bool(ready)
        self.flag = None
        self.colour = colour
        
    def draw(self,win):
        
        #drawing the actual rectangle
        if self.ready:
            pygame.draw.rect(win,self.colour,(self.xPos,self.yPos,19,19))
        else:
            pygame.draw.rect(win,(55,0,0),(self.xPos,self.yPos,19,19))
        