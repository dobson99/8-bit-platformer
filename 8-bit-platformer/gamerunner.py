from gameobj import Game
from controllers import RealController
from maps import *

game = Game()
game.controller = RealController() # (...as opposed to a mock controller used for testing)
game.playerX = 48
game.playerY = 16
game.map = getMainMap()
game.setCurrentRoom(game.map["Hayley's Room"])
game.executeGameLoopIndefinitely()

        
