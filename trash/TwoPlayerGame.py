from LRGame import *
from constants import *

class TwoPlayerGame(LRGame):
    def __init__(self, polyhexSize: int, topDistance: int):
        super().__init__(polyhexSize, topDistance)

    def next(self, moveL: tuple, rotationL: int, moveR: tuple, rotationR: int):
        if self.running:
            message = {
                "LEFT": self.lGame.next(moveL, rotationL),
                "RIGHT": self.rGame.next(moveR, rotationR)
            }
    
            if not message["LEFT"]['running'] or not message["RIGHT"]['running']:
               self.running = False
    
            else:
                if message["LEFT"]['placed']:
                    self.currentGame = "LEFT"
                    self.pushBoards(False)
                    self.clearFilledRows()
    
                if message["RIGHT"]['placed']:
                    self.currentGame = "RIGHT"
                    self.pushBoards(True)
                    self.clearFilledRows()
    
    
    
            return message
