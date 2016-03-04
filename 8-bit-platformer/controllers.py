import sys, pygame, os
from pygame.locals import *
class RealController():
    """This is an object that is used to control the game. When actually playing
    this will be a normal controller that accepts input from keyboard and automatically
    loops through the game loop. When under test, this controller is a TestController
    that simulates keypresses and has fine grained control over things like when to advance
    the game loop"""
    
    def getKeys(self):
        return pygame.key.get_pressed()
    
class TestController():
    """This is an object that is used to control the game used for test purposes. This controller
    simulates keypresses and has fine grained control over things like when to advance
    the game loop"""
    
    def __init__(self):
        list1 = []
        for x in range(0, 322):
            list1.append(0)
        self.keys = tuple(list1)
        
    
            
    def getKeys(self):
        return self.keys
   
    def setKeyPressed(self, key):
        list1 = list(self.keys)
        list1[key] = 1
        self.keys = tuple(list1)
        
    def unsetKeyPressed(self, key):
        list1 = list(self.keys)
        list1[key] = 0
        self.keys = tuple(list1)
        
           
       