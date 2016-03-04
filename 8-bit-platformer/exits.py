import sys, pygame, os
from controllers import *
from pygame.locals import *
import time
from blocks import *
from constants import *


# should doo

class DoorKey():
    def __init__(self):
        self.initializeImages()
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.setImageRectAndRecalc(self.image.get_rect())
        self.collision_rect = self.image_rect 
        self.secondsPerFrame = 0.1
        self.timeOfLastCycle = 0
        self.room = None

    def initializeImages(self):
        self.images = []
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "key1.bmp"))
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "key2.bmp"))
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "key3.bmp"))
    
    def setImageRectAndRecalc(self, rect):
        self.image_rect = rect 
        x = self.image_rect.x + (self.image_rect.width / 4) 
        y = self.image_rect.y
        width = self.image_rect.width / 2;
        height = self.image_rect.height;
        self.collision_rect = Rect(x,y,width,height)
        
    
    def cycleAnimation(self):
        timeNow = time.time()
        timeSinceLastCycle = timeNow - self.timeOfLastCycle
        if timeSinceLastCycle > self.secondsPerFrame:      
            self.imageIndex = self.imageIndex + 1
            if (self.imageIndex >= len(self.images)):
                self.imageIndex = 0
            self.image = self.images[self.imageIndex]
            self.timeOfLastCycle = timeNow
    
    
    
    
class Door():
    
    def __init__(self): # roomName is the destination room
        self.playerEntryPlacement = None
        self.initializeImages()
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.setImageRectAndRecalc(self.image.get_rect())
        self.collision_rect = self.image_rect 
        self.secondsPerFrame = 0.1
        self.timeOfLastCycle = 0
        self.room = None

    def initializeImages(self):
        self.images = []
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "exit.bmp"))
    
    def setImageRectAndRecalc(self, rect):
        self.image_rect = rect
        x = self.image_rect.x + (self.image_rect.width / 4) 
        y = self.image_rect.y
        width = self.image_rect.width / 2;
        height = self.image_rect.height;
        self.collision_rect = Rect(x,y,width,height)
        
    
    def cycleAnimation(self):
        timeNow = time.time()
        timeSinceLastCycle = timeNow - self.timeOfLastCycle
        if timeSinceLastCycle > self.secondsPerFrame:      
            self.imageIndex = self.imageIndex + 1
            if (self.imageIndex >= len(self.images)):
                self.imageIndex = 0
           # print ("cycling animation " + str(self.imageIndex + 1) + "/" + str(len(self.images)) + " for Door") #+ " for Door"))
            self.image = self.images[self.imageIndex]
            self.timeOfLastCycle = timeNow
 
class TallDoor(Door):
    def __init__(self): # roomName is the destination room
        self.playerEntryPlacement = None
        self.images = None
        self.image = None
        self.imageIndex = None
        Door.__init__(self)
        
    def initializeImages(self):
        self.images = []
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "exitTall2.bmp"))
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "exitTall.bmp"))
        self.images.append(pygame.image.load(Constants.RESOURCES_DIR + "greenBlock.bmp"))
