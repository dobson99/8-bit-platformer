import pygame
from constants import *

class Block():
    def __init__(self, imageName, imageRect):
        self.image = pygame.image.load(Constants.RESOURCES_DIR + imageName)
        self.image_rect = imageRect
        #self.image_rect = self.image.get_rect()
                
    def getRect(self):
        return self.image_rect
    
class Flower(Block):
    def __init__(self, imageName, imageRect):
        self.image = pygame.image.load(Constants.RESOURCES_DIR+ imageName)
        self.image_rect = imageRect
        
