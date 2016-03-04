import sys, pygame, os
from pygame.locals import *
from controllers import *
from time import *
from gameobj import *
import unittest

#for key in d: will simply loop over the keys in the dictionary, 
# rather than the keys and values. 
# To loop over both key and value you can use 
#        for key, value in d.iteritems():
def getTestMap():
    
        roomMap = {}
        
        d1 = Door()
        d2 = Door()
        d1.destinationDoor = d2
        d2.destinationDoor = d1
        d1.playerEntryPlacement = Placement.left
        d2.playerEntryPlacement = Placement.right
        
        d3 = Door()
        d4 = Door()
        d3.destinationDoor = d4
        d4.destinationDoor = d3
        d3.playerEntryPlacement = Placement.above
        d4.playerEntryPlacement = Placement.below
        
        d5 = Door()
        d6 = Door()
        d5.destinationDoor = d6
        d6.destinationDoor = d5
        d5.playerEntryPlacement = Placement.above
        d6.playerEntryPlacement = Placement.below

        
        room = Room("Room A")
        layout = []
        layout.append([1,1,1,1,1,1,1,1])
        layout.append([1,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,1,0,0,1])
        layout.append([1,0,8,0,1,0,0,d1])
        layout.append([1,1,1,1,1,1,1,1])
        room.createBlocksFromLayout(layout)
        roomMap[room.name] = room
                                
        room = Room("Room B")
        layout = []
        layout.append([1,1,1,1,1,1,1,1,1,1,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([d2,0,0,0,0,0,0,0,0,0,0])
        layout.append([1,1,1,1,1,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,1,1,1,1,1,1,1,d3,d5,1])
        room.createBlocksFromLayout(layout)
        roomMap[room.name] = room
        
        room = Room("Room C")
        layout = []
        layout.append([1,1,1,1,1,1,1,1,d4,d6,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,0])
        layout.append([1,1,1,1,1,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,0])
        layout.append([1,0,0,0,0,0,0,0,0,0,0])
        layout.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,])
        room.createBlocksFromLayout(layout)
        roomMap[room.name] = room
             
        h1 = TallDoor()
        h2 = TallDoor()
        h1.destinationDoor = h2
        h2.destinationDoor = h1
        h1.playerEntryPlacement = Placement.left
        h2.playerEntryPlacement = Placement.right

        k = DoorKey()
        room = Room("Room D")
        layout = []
        layout.append([1,1,1,1,1,1,1,1,1,1,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,h1])
        layout.append([1,0,0,k,0,0,0,0,0,0,0])
        layout.append([1,1,1,1,1,1,1,1,1,1,1])
        room.createBlocksFromLayout(layout)
        roomMap[room.name] = room
        
        room = Room("Room E")
        layout = []
        layout.append([1,1,1,1,1,1,1,1,1,1,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([1,0,0,0,0,0,0,0,0,0,1])
        layout.append([h2,0,0,0,0,0,0,0,0,0,1])
        layout.append([0,0,0,0,0,0,0,0,0,0,0])
        layout.append([1,1,1,1,1,1,1,1,1,1,1])
        room.createBlocksFromLayout(layout)
        roomMap[room.name] = room
             
        return roomMap

class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()
        self.game.controller = TestController()
        self.game.map = getTestMap()
        self.game.setCurrentRoom(self.game.map["Room A"])

    def testCollideWithLeftWall(self):
        self.game.accY = 0.0
        self.game.controller.setKeyPressed(K_o)
        self.game.playerCollisionPoints = {} 
        self.game.playerCollisionPoints[Constants.LEFT]   = [[0,8]]
        self.game.executeGameLoop(5)
        self.assertTrue(self.game.playerX >  16 and self.game.playerX < 17, "BALHA")
    
    def testCollideWithRightWall(self):
        self.game.accY = 0.0
        self.game.controller.setKeyPressed(K_p)
        self.game.playerCollisionPoints = {} 
        self.game.playerCollisionPoints[Constants.RIGHT]  = [[15,8]]   
        self.game.playerY = 48
        self.game.playerX = 48
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(1)
        self.assertTrue(self.game.playerX >  48 and self.game.playerX < 49, "self.game.playerX is " + str(self.game.playerX))
    

    # The player block sinks lower than it should when the p Key is pressed. 
    # If p is not pressed, it just lands fine.
    def testCollideWithRightWallWithGravityEnabled(self):
        self.game.playerX = 48
        self.game.playerY = 31
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)# one pixel too low after this
        self.game.executeGameLoop(1) # 2-3 pixels too low
        self.game.executeGameLoop(1) # 2-3 pixels too low
        self.game.executeGameLoop(1) # 2-3 pixels too low
        
    def testMoveToNewRoom(self):
       #self.game.setCurrentRoom(roomA)
        self.game.playerX = 85
        self.game.playerY = 64        
        self.game.controller.setKeyPressed(K_p)
        self.game.executeGameLoop(8)
        print("blah")
        
    def testMoveToNewRoom2(self):
        roomA = self.game.map["Room A"]
        roomB = self.game.map["Room B"]
        self.game.setCurrentRoom(roomA)
        self.game.playerX = 85
        self.game.playerY = 64
        self.game.tickSpeed = 30
        self.game.controller.setKeyPressed(K_p)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.controller.unsetKeyPressed(K_p)
        self.assertTrue(self.game.currentRoom == roomB, "current room is " + str(self.game.currentRoom.name))
        self.game.controller.setKeyPressed(K_o)
        self.game.executeGameLoop(20)
        self.assertTrue(self.game.currentRoom == roomA, "current room is " + str(self.game.currentRoom.name))
    
    def testMoveToNewRoom3(self):
        roomB = self.game.map["Room B"]
        roomC = self.game.map["Room C"]
        self.game.setCurrentRoom(roomB)
        self.game.playerX = 90
        self.game.playerY = 80
        self.game.tickSpeed = 30
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.controller.setKeyPressed(K_p)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.controller.unsetKeyPressed(K_p)
        self.assertTrue(self.game.currentRoom == roomC, "current room is " + str(self.game.currentRoom.name))
        print("ssss")
        
    def testPlayerPassesOverFlower(self):
        self.game.setCurrentRoom(self.game.map["Room A"])
        self.game.playerX = 16
        self.game.playerY = 48
        self.game.executeGameLoop(10)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.controller.setKeyPressed(K_p)        
        self.game.executeGameLoop(5)
        self.assertTrue(self.game.playerX > 20) # Means we moved through the flower
        
    def testFrictionAfterLandSlowsDownQuickly(self):
        self.game.setCurrentRoom(self.game.map["Room C"])
        self.game.playerX = 16
        self.game.playerY = 144
        self.game.executeGameLoop(1)
        self.game.controller.setKeyPressed(K_p)        
        self.game.controller.setKeyPressed(K_SPACE)        
        self.game.executeGameLoop(1)
        self.game.controller.unsetKeyPressed(K_SPACE)  
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(10)
        self.game.executeGameLoop(10)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        
    def testDrawTextInfo(self):
        self.game.setCurrentRoom(self.game.map["Room C"])
        self.game.playerX = 16
        self.game.playerY = 144
        self.game.executeGameLoop(1)
        self.game.displayRoomName();
        
    def testExitTall(self):
        self.game.setCurrentRoom(self.game.map["Room D"])
        self.game.playerX = 125
        self.game.playerY = 100
        self.game.executeGameLoop(1)
        self.game.controller.setKeyPressed(K_p)        
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.controller.unsetKeyPressed(K_p)        
        self.game.controller.setKeyPressed(K_o)        
        self.game.executeGameLoop(10)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        
    def testBlockAnimation(self):
        h = TallDoor()
        self.assertTrue(h.imageIndex == 0)
        h.imageIndex = h.imageIndex + 1
        self.assertTrue(h.imageIndex == 1)
        

    def findDoorInRoom(self, room):
        return room.exits[0]
    
    
    def testGameLoopCyclesBlockImage(self):
        self.game.setCurrentRoom(self.game.map["Room D"])
        self.game.playerX = 125
        self.game.playerY = 100
        h = self.findDoorInRoom(self.game.currentRoom)
        self.assertTrue(h.imageIndex == 0)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(1)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.assertTrue(h.imageIndex == 1)     
        

    def testPickUpKeyIncreasesPlayerKeyCount(self):
        self.game.setCurrentRoom(self.game.map["Room D"])
        self.game.playerX = 20
        self.game.playerY = 120
        self.assertTrue(len(self.game.player.collectables) == 0)
        self.game.controller.setKeyPressed(K_p)        
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.game.executeGameLoop(5)
        self.assertTrue(len(self.game.player.collectables) == 1)
        
        
    def testMovingBlockMoves(self):
        self.game.setCurrentRoom(self.game.map["Room C"])
        
    def testCollisionWithIrregularPolygon(self):
        self.game.setCurrentRoom(self.game.map["Room D"])
        self.game.playerX = 20
        self.game.playerY = 120
        

       

        
