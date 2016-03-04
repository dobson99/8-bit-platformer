# To do: tidy these up
import sys, pygame, os
from controllers import *
from pygame.locals import *
from blocks import *
from exits import *
from constants import Constants
import time

pygame.init()

if not pygame.mixer: print("Can't start pygame sound mixer")




# Used by Doors to say where player should be positioned relative to a door once they've gone through it
class Placement():
    left = "left"
    right = "right"
    above = "above"
    below = "below"
    
class Colour():
    black = 0,0,0


class Player():
    def __init__(self, imageName):
        self.image = pygame.image.load(Constants.RESOURCES_DIR + imageName)
        self.image_rect = self.image.get_rect()
        self.collectables = []
    
    def pickupObjFromRoom(self, obj, room):
        self.collectables.append(obj)
        room.collectables.remove(obj)

class Room():
    def __init__(self, roomName, backgroundImageFilename="none"):
        self.exits = []
        self.blocks = []
        self.scenery = []
        self.collectables = []
        self.name = roomName
        self.backgroundColour = Colour.black
        self.roomHeight = 0 # Height in blocks
        if backgroundImageFilename == "none":
            self.backgroundImage = None
        else:
            self.setBackgroundImage(Constants.RESOURCES_DIR + "castle1.jpg");
        
    def setBackgroundImage(self, fileName):
        self.backgroundImage = pygame.image.load(fileName)
        self.backgroundImage  = pygame.transform.scale( self.backgroundImage, (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.backgroundImageRect = self.backgroundImage.get_rect()
       
    def createBlocksFromLayout(self, layout):
        # Convert the layout into instances of blocks
        rowPos = 0
        cPos = 0
        for row in layout:
            for obj in row:
                row = rowPos * Constants.BLOCK_SIZE
                col = cPos * Constants.BLOCK_SIZE
                rect = Rect(col, row, (Constants.BLOCK_SIZE), (Constants.BLOCK_SIZE))
                if obj == 1:
                    block = Block("bricksquare.bmp",rect)
                    self.blocks.append(block)
                if obj == 2:
                    block = Block("block2.bmp",rect)
                    self.blocks.append(block)    
                if obj == 3:
                    block = Block("yellowBlock.bmp",rect)
                    self.blocks.append(block) 
                if obj == 4:
                    block = Block("orangeBlock.bmp",rect)
                    self.blocks.append(block)   
                if obj == 5:
                    block = Block("greenBlock.bmp",rect)
                    self.blocks.append(block)      
                if obj == 6:
                    block = Block("purpleBlock.bmp",rect)
                    self.blocks.append(block)    
                if obj == 7:
                    block = Flower("hayleyFlower.bmp",rect)
                    self.scenery.append(block)       
                if obj == 8:
                    self.scenery.append(Flower("charlotteFlower.bmp", rect))
                if isinstance(obj,DoorKey):
                    key = obj
                    key.setImageRectAndRecalc (rect)
                    self.collectables.append(key)
                if isinstance(obj,Door):
                    door = obj
                    door.setImageRectAndRecalc (rect)
                    door.room = self
                    self.exits.append(door)
                cPos = cPos + 1
            cPos = 0
            rowPos = rowPos + 1
        self.roomHeight = rowPos



class Game():
    """Game class"""
    def __init__(self):
        self.playerKeyCount = 0
        self.screenWidth = Constants.SCREEN_WIDTH #800
        self.screenHeight = Constants.SCREEN_HEIGHT#500
        size = self.screenWidth, self.screenHeight
        #self.speed = [2, 2]
        self.font = pygame.font.SysFont("Free Sans",24)
        # set accelleration and speed
        self.mScale = 3
        self.playerX = Constants.PLAYER_START_X
        self.playerY = Constants.PLAYER_START_Y
        self.speedX = Constants.PLAYER_INITIAL_SPEED_X
        self.speedY = 0.0
        self.accX = 0.7
        self.decX = 0.5
        self.maxSpeedX = 4.0
        self.maxSpeedY = 8.0
        self.jumpStartSpeedY = 9.0 
        # self.accY = 1 
        self.accY = 0.35 
        self.jumping = False
        self.jumpKeyDown = False
        self.moveRequest = False
        self.tickSpeed = 100
        
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        
        self.player = Player("player.bmp")
#        self.player = Player("gina.jpg")
        self.player.image_rect = Rect(32, 140, 16, 16)
        
        self.sound1 = self.load_sound("whiff.wav")
                
        self.font = pygame.font.SysFont("Arial", 24)
        self.prevRectX = None
        self.prevRectY = None
        
        self.playerCollisionPoints = {} 
        self.playerCollisionPoints[Constants.TOP]    = [[8,0]]
        self.playerCollisionPoints[Constants.BOTTOM] = [[8,15]]
        self.playerCollisionPoints[Constants.LEFT]   = [[0,8]]
        self.playerCollisionPoints[Constants.RIGHT]  = [[15,8]]

#         self.playerCollisionPoints[Constants.TOP]    = [[12,0]]
#         self.playerCollisionPoints[Constants.BOTTOM] = [[12,24]]
#         self.playerCollisionPoints[Constants.LEFT]   = [[0,12]]
#         self.playerCollisionPoints[Constants.RIGHT]  = [[24,12]]
#         
        self.playerCenterPoint = [8,8]
        self.currentRoom = None
        self.justSwitchedRooms = False
        self.delayFactor = 0; # Used to slow the game down, just for easier viewing of tests which run quickly
        self.messageCountdown = 1000 # remove instructions after a period of time - hack
        
    def reset(self):
        self.currentRoom = self.map["Hayley's Room"]
        self.playerX = Constants.PLAYER_START_X
        self.playerY = Constants.PLAYER_START_Y
        self.speedY = 0
        self.firstKeyPressed = False
        
        
    def loadMap(self, map):
        self.map = map
        
        
    def setCurrentRoom(self, room):
        self.currentRoom = room
        
            
    def load_sound(self, name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join(Constants.RESOURCES_DIR, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print("Can't load sound:", fullname)
            raise SystemExit
        return sound        
    

        #self.gravityVectorY = 0
    
    def movePlayerRect(self, moveVect):
        self.player.moveImageRect(moveVect)



    def checkBottomCollision(self):
        pass
    
    
    def printPlayerRect(self, rect):
        if ((rect.x != self.prevRectX) or (rect.y != self.prevRectY)):
            print ("player rect X:" + str(self.player.image_rect.x) + ", Y:" + str(self.player.image_rect.y))
            self.prevRectX = rect.x
            self.prevRectY = rect.y
    
    def executeGameLoopIndefinitely(self):
        while 1:
            self.runGameLoopOnce()
            
    def executeGameLoop(self, count):
        for x in range(count):
            self.runGameLoopOnce()

    def runGameLoopOnce(self):
            self.clock.tick(self.tickSpeed)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

            # Update the player's position - ordering is important here. see visio
            self.playerX += self.speedX
            self.playerY += self.speedY
            self.moveRequest = False
            
            # Process player keyboard input (adjust speed X based on user input)
            keys = self.controller.getKeys()

            if keys[K_p]:
                self.speedX += self.accX
                self.moveRequest = True
            if keys[K_o]:
                self.speedX -= self.accX
                self.moveRequest = True
            if keys[K_SPACE]:
                if not self.jumping and not self.jumpKeyDown:
                    self.jumping = True
                    self.jumpKeyDown = True
                    self.speedY = -self.jumpStartSpeedY
            if keys[K_r]:
                self.reset()

            else:
                self.jumpKeyDown = False

            # Limit the sideways acceleration of the player (adjust speed X and speed Ybased on accerlation limits)
            if self.speedX > self.maxSpeedX: self.speedX = self.maxSpeedX
            if self.speedX < -self.maxSpeedX: self.speedX = -self.maxSpeedX
            if self.speedY < -self.maxSpeedY: self.speedY = -self.maxSpeedY
            
            
            self.speedY += self.accY
    
    
            # Decelerate the player's sideways movement if left or right wasn't pressed
            if not self.moveRequest:
                if self.speedX < 0: 
                    self.speedX += self.decX
                if self.speedX > 0: 
                    self.speedX -= self.decX

  
                # Deceleration may produce a speed that is greater than zero but
                # smaller than the smallest unit of deceleration. These lines ensure
                # that the player does not keep travelling at slow speed forever after
                # decelerating.
                if self.speedX > 0 and self.speedX < self.decX: 
                    self.speedX = 0
                if self.speedX < 0 and self.speedX > -self.decX: 
                    self.speedX = 0
    
            
            # Render the game world
            
            if (self.currentRoom.backgroundImage == None):
                self.screen.fill(self.currentRoom.backgroundColour)
            else:
                self.screen.blit(self.currentRoom.backgroundImage, self.currentRoom.backgroundImageRect)
            for b in self.currentRoom.blocks:
                self.screen.blit(b.image, b.image_rect)
            for e in self.currentRoom.exits: 
                self.screen.blit(e.image, e.image_rect)
            for s in self.currentRoom.scenery:
                self.screen.blit(s.image, s.image_rect)    
            for o in self.currentRoom.collectables:
                self.screen.blit(o.image, o.image_rect)    
            self.player.image_rect.x = self.playerX
            self.player.image_rect.y = self.playerY
            self.screen.blit(self.player.image, self.player.image_rect)            
            self.displayRoomName()
            self.displayStats()

            pygame.display.flip()
            
                               
            # Penetration resolution
            contactX = True
            contactYBottom = True
            contactYTop = True

            
            for i in range(1,Constants.CONTACT_SOLVER_ITERATIONS):
                if not (contactX or contactYBottom or contactYTop):
                    break
                
                nextMoveX = self.speedX 
                nextMoveY = self.speedY 
                
                # No collisions found yet
                contactX = False
                contactYBottom = False
                contactYTop = False
                originalMoveX = nextMoveX
                originalMoveY = nextMoveY
                
                # check collision with blocks
                for b in self.currentRoom.blocks:
                    if (contactX or  contactYBottom or contactYTop):
                        continue
                    
                    for name in self.playerCollisionPoints:
                        if name == Constants.TOP and nextMoveY > 0: continue
                        if name == Constants.BOTTOM and nextMoveY < 0: continue
                        if name == Constants.LEFT and nextMoveX > 0: continue
                        if name == Constants.RIGHT and nextMoveX < 0: continue

                        if name == Constants.LEFT or name == Constants.RIGHT:
                            projectedMoveX = nextMoveX
                        else:
                            projectedMoveX = 0
     
                        if name == Constants.TOP or name == Constants.BOTTOM:
                            projectedMoveY = nextMoveY 
                        else:
                            projectedMoveY = 0  
                            
                        collisionPoint1 = self.playerCollisionPoints[name][0]

                        collisionPoint1X = collisionPoint1[0]
                        collisionPoint1Y = collisionPoint1[1]
                        
                        pointToCheck1 = [collisionPoint1X + self.playerX + projectedMoveX, collisionPoint1Y + self.playerY + projectedMoveY]

                        
                        while (b.image_rect.collidepoint(pointToCheck1)):
                            if name == Constants.LEFT: 
                                projectedMoveX = projectedMoveX + 1.0
                            if name == Constants.RIGHT: 
                                projectedMoveX = projectedMoveX - 1.0
                            if name == Constants.TOP: 
                                projectedMoveY = projectedMoveY + 1.0
                            if name == Constants.BOTTOM: 
                                projectedMoveY = projectedMoveY - 1.0
                            
                            # Recalculate points to check
                            pointToCheck1 = [collisionPoint1X + self.playerX + projectedMoveX, collisionPoint1Y + self.playerY + projectedMoveY]
#                             pointToCheck2 = [collisionPoint2X + self.playerX + projectedMoveX, collisionPoint2Y + self.playerY + projectedMoveY]
                 
                        
                        if name == Constants.TOP or name == Constants.BOTTOM: nextMoveY = projectedMoveY
                        if name == Constants.LEFT or name == Constants.RIGHT: nextMoveX = (projectedMoveX)
                                                                       
                    
                    if nextMoveY > originalMoveY and originalMoveY < 0:
                        contactYTop = True
                        
                    if nextMoveY < originalMoveY and originalMoveY > 0:
                        contactYBottom = True
                        
                    if abs(nextMoveX - originalMoveX) > 0.01:
                        contactX = True
                        
                    if contactX and contactYTop and self.speedY < 0:
                        self.speedY = 0
                        nextMoveY = 0
            
            # If a contact has been detected, apply the recalculated movement vector
            # and disable any further movement this frame (in either X or Y as appropriate)
            if contactYBottom or contactYTop:
                self.playerY = self.playerY + nextMoveY
                self.player.image_rect.y = self.playerY
                self.speedY = 0
                if contactYBottom:
                    if self.jumping == True: # Slow down on landing
                        self.speedX = self.speedX * .5
                    self.jumping = False
                    
            if contactX:
                self.playerX = self.playerX + nextMoveX
                self.speedX = 0
                
            # Check collisions with exits
            for door in self.currentRoom.exits:
                centerPointX = self.playerCenterPoint[0]
                centerPointY = self.playerCenterPoint[1]
                playerRect = self.player.image_rect;
                #x = centerPointX - BLOCK_SIZE / 4
                pointToCheck = [centerPointX + self.playerX, centerPointY + self.playerY]
                if (door.collision_rect.colliderect(playerRect)):
                    self.switchRooms(door)
                    break
                
            # Update block animation # this can be refactored into an existing loop for performance later
            for door in self.currentRoom.exits:
                door.cycleAnimation()

            for doorKey in self.currentRoom.collectables:
                doorKey.cycleAnimation()

                
            # Check collision with other objects such as keys and collectables
            for otherObj in self.currentRoom.collectables:
                centerPointX = self.playerCenterPoint[0]
                centerPointY = self.playerCenterPoint[1]
                playerRect = self.player.image_rect;
                pointToCheck = [centerPointX + self.playerX, centerPointY + self.playerY]
                if (otherObj.collision_rect.colliderect(playerRect)):  # Change this so that PLAYER has a generic collection of collectables, not just doorKeys etc
                    self.player.pickupObjFromRoom(otherObj, self.currentRoom) #doorKeys.append(otherObj)
                    #self.currentRoom.otherObjects.remove(otherObj)
                    break
                
     
                      
    def switchRooms(self, door):
        newRoom = door.destinationDoor.room
        self.currentRoom = newRoom
        placement = door.destinationDoor.playerEntryPlacement
        x = door.destinationDoor.image_rect.x
        y = door.destinationDoor.image_rect.y + ((door.destinationDoor.image_rect.height / 2) - 1)
        if placement == Placement.left:
            x = x - Constants.BLOCK_SIZE
        elif placement == Placement.right:
            x = x + Constants.BLOCK_SIZE
        elif placement == Placement.above:
            y = y - Constants.BLOCK_SIZE
        elif placement == Placement.below:
            y = y + Constants.BLOCK_SIZE
        
        self.playerX = x
        self.playerY = y

        
    def displayRoomName(self):
        countStr  = str(len(self.player.collectables));
        text = self.currentRoom.name + ". You have " + countStr  + " keys."
        x = (self.screenWidth /2.5)
        y = (self.currentRoom.roomHeight * Constants.BLOCK_SIZE)
        self.screen.blit(self.font.render(text,1,(255,255,255)),(x,y))

    def displayStats(self):

        if (self.messageCountdown > 0):
            self.showText("Use O, P and spacebar to move player" , (250,15)) #TODO find a better home for this text
            self.showText("Press R to reset if you get stuck", (250,35))
            self.messageCountdown = self.messageCountdown -1


    def showText(self,text, coordinates):
        self.screen.blit(self.font.render(text,1,(255,255,255)),(coordinates))

