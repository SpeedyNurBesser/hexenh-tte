import random
import copy

from constants import *

class RGame:
    def __init__(self, polyhexSize: int, polyhexSet, clearRows: bool = True):
        self.polyhexSize = polyhexSize

        self.boardSize = (polyhexSize*2+1, polyhexSize*6)
        self.board = [[' ' for i in range(self.boardSize[1])] for i in range(self.boardSize[0])]
        self.origin = (0,0)

        self.clearRows = clearRows
        
        self.spawnLocation = (int(self.boardSize[0] / 2), self.boardSize[1] - self.polyhexSize)

        self.DIRECTIONS = [(1,0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        if polyhexSet:
            self.polyhexSet = polyhexSet
        else:
            self.polyhexSet = self.generatePolyhexesSet(self.polyhexSize)   

        self.currentPolyhex = False
        self.nextPolyhex = False

        self.currentHighlight = []

        self.timer = 0
        self.fallInterval = 10 # given as number of steps, i.e. runs of the self.next() method, the method is expected to run 60 times a second
        self.steps = 0 # is never reset, needed for highscores


        self.newlyClearedCells = 0

        self.points = 0
        self.clearedRows = 0

        self.running = True

    def generatePolyhexesSet(self, size: int):
        def isRotatedCopy(polyhex):
            rotatedPolyhex = polyhex.copy()

            for n in range(6):
                rotatedPolyhex.sort()
                if rotatedPolyhex in unique_polyhexes:
                    return True
                rotatedPolyhex = self.rotatePolyhex(rotatedPolyhex, True)

            return False

        def generate(current_polyhex):
            if len(current_polyhex) == size:
                # only add unique_polyhexes
                # for every hexagon in the polyhex the polyhex is transformed so that the hexagon is at the origin, then further tests, if said polyhex or any rotated version is already inside unique_polyhexes list
                # if not add to unqiue polyhexes list
                current_polyhex.sort()

                possiblePolyhexConfigurations = transformEveryHexagonToOrigin(current_polyhex)
                for polyhex in possiblePolyhexConfigurations:
                    if isRotatedCopy(sorted(polyhex)):
                        return

                unique_polyhexes.append(current_polyhex)
                #print(current_polyhex)
                #print(f"{len(unique_polyhexes)}. New polyhex found")
                return

            if len(current_polyhex) == 1:
                generate(current_polyhex + [self.DIRECTIONS[0]])
            else:
                for x, y in current_polyhex:
                    for dx, dy in self.DIRECTIONS:
                        neighbor = (x + dx, y + dy)
                        if neighbor not in current_polyhex:
                            generate(current_polyhex + [neighbor])

        def transformEveryHexagonToOrigin(polyhex): 
                # returns a list of polyhexes, where for every hexagon in the polyhex the polyhex is transformed so that the hexagon is at the origin
                # exampe [(0, 0), (0, 1)] -> [[(0, 0), (0, 1)], [(0, -1), (0, 0)]]

                output = [] # list of polyhexes

                for hexagon in polyhex:
                    if hexagon == (0,0):
                        output.append(polyhex)
                    else:
                        vector = (hexagon[0] * (-1), hexagon[1] * (-1))
                        output.append(self.movePolyhex(polyhex, vector))

                return output

        unique_polyhexes = []

        generate([(0,0)])

        return unique_polyhexes


    def movePolyhex(self, polyhex: list, vector: tuple):
        output = []

        for hexagon in polyhex:
            output.append((hexagon[0] + vector[0], hexagon[1] + vector[1]))

        return output

    def rotatePolyhex(self, polyhex: list, clockwise: bool = True):
        # on a hexagonal grid plane with axial coordinates, x and y,
        # where the y axes is sitting on the x-axes with 60° tilt to the Left
        # a clockwise-rotation of 60° of a given point (x_o, y_o) around the orgin 
        # always results in a new point with the coordinates (-y_o, x_o + y_o)
        # given this knowledge, I was able to calculate that a 60° anti-clockwise (300° degree) rotation
        # always results in a new set of coordinates (x_o + y_o, -x_o)

        # I am not quite sure, why this is, but I realized that it is,
        # after having stared at a series of coordinates for half an hour

        def rotatePolyhex60DegClockwise(polyhex):
            rotatedPolyhex = []
            for hexagon in polyhex:
                originalX = hexagon[0]
                originalY = hexagon[1]

                rotatedPolyhex.append((originalY * (-1), originalX + originalY))

            return rotatedPolyhex

        def rotatePolyhex60DegAntiClockwise(polyhex):
            rotatedPolyhex = []
            for hexagon in polyhex:
                originalX = hexagon[0]
                originalY = hexagon[1]
                
                rotatedPolyhex.append((originalX + originalY, originalX * (-1)))

            return rotatedPolyhex

        rotatedPolyhex = []

        if clockwise:
            rotatedPolyhex = rotatePolyhex60DegClockwise(polyhex)
        else:
            rotatedPolyhex = rotatePolyhex60DegAntiClockwise(polyhex)

        return rotatedPolyhex

    def dropPolyhex(self, polyhex: list):
        # returns position of the given polyhex but dropped as far as possible while still being valid
        
        isValidMove = True
        lastValidMove = polyhex
        while isValidMove:
            move = self.isValidNewPosition(lastValidMove, (0, -1), 0)
            if move:
                lastValidMove = move
            else:
                isValidMove = False

        return lastValidMove


    def isOccupiedPosition(self, position: tuple):
        # returns True, if the given positon is either occupied (OCCUPIED_SYMBOL) or outside the borders of the board
        x = position[0]
        y = position[1]

        if x < 0 or y < 0:
            return True

        if x > (len(self.board) - 1):
            return True

        if y > (len(self.board[x]) - 1):
            return True

        if self.board[x][y] == OCCUPIED_SYMBOL:
            return True

        return False

    def isValidNewPosition(self, polyhex: list, vector: tuple, rotation: int):
        # tries to move polyhex using given vector and rotation
        # vector movement is prioritized before rotation, 
        # i.e. if the move on its own is valid, but rotation would make it invalid, the rotation is skipped

        # returns false, if move is invalid
        # returns new polyhex, if move is valid

        newPolyhex = polyhex

        if vector:
            if vector[1] > 0:
                newPolyhex = self.dropPolyhex(polyhex)
            else:
                newPolyhex = self.movePolyhex(polyhex, vector)

        if rotation and rotation != 0:
            # because of the way rotation works, the polyhex is...
            # 1. moved to the origin
            # 2. then rotated
            # 3. then moved back to its original position

            # as it is uncertain around which hexagon (origin) the polyhex should rotate,
            # all are tried in order and the first to work is used

            possibleRotatedPolyhexes = []

            for hexagon in newPolyhex:
                vectorToOriginalPosition = hexagon
                vectorToOrigin = (hexagon[0] *(-1), hexagon[1] * -1)

                polyhexAtOrigin = self.movePolyhex(newPolyhex, vectorToOrigin)

                rotatedPolyhex = newPolyhex

                if rotation == 1: # rotate clockwise
                    rotatedPolyhex = self.rotatePolyhex(polyhexAtOrigin, True)
                elif rotation == -1: # rotate anti-clockwise
                    rotatedPolyhex = self.rotatePolyhex(polyhexAtOrigin, False)
                else:
                    pass

                possibleRotatedPolyhexes.append(self.movePolyhex(rotatedPolyhex, vectorToOriginalPosition))

            for rotatedPolyhex in possibleRotatedPolyhexes:
                validPolyhex = True
                for position in rotatedPolyhex:
                    if self.isOccupiedPosition(position):
                        validPolyhex = False

                if validPolyhex:
                    return rotatedPolyhex


        for position in newPolyhex:
            if self.isOccupiedPosition(position):
                return False

        return newPolyhex

    def filledRowsExist(self):
        # returns a list of the index of all rows which are completely filled, if such rows exists
        # else returns false

        filledRows = []

        for y, _ in enumerate(self.board[0]):
            if self.isFilledRow(y):
                filledRows.append(y)

        # before returning the list of filled rows is returned,
        # as the list lists filled rows bottom to top,
        # but having the list top to bottom is much more helpful,
        # as the filled rows are removed in the given order
        filledRows.reverse()

        if filledRows != []:
            return filledRows

        return False

    def isFilledRow(self, row: int):
        for x in range(len(self.board)):
            if self.board[x][row] != OCCUPIED_SYMBOL:
                    return False

        return True

    def loseConditionFulfilled(self):
        # the game is lost, when a block is placed inside the x topmost rows,
        # where x is the polyhexSize

        for x in self.board:
            for i in range(self.polyhexSize):
                y = self.boardSize[1] - i -1
                if x[y] == OCCUPIED_SYMBOL: return True

        return False

    def isEmptyBoard(self):
        for row in self.board:
            for cell in row:
                if cell == OCCUPIED_SYMBOL:
                    return False

        return True

    def getRandomPolyhex(self): 
        return random.choice(self.polyhexSet)


    def placePolyhexOnBoard(self, polyhex: list, symbol: str):
        newBoard = copy.deepcopy(self.board)

        for x, y in polyhex:
            newBoard[x][y] = symbol

        self.board = newBoard

    def removeSymbolFromBoard(self, polyhex: list):
        newBoard = copy.deepcopy(self.board)

        for x, y in polyhex:
            newBoard[x][y] = ' ' 
            
        self.board = newBoard

    def clearRow(self, row: int):
        # clears a given row and moves all occupied symbols above downwards

        for x in range(len(self.board)):
            self.board[x][row] = ' '
            self.newlyClearedCells +=1

        for x, _ in enumerate(self.board):
            # gets all rows above the given row
            for y in range(len(self.board[x]) - row):
                upperY = y + row
                
                if self.board[x][upperY] == OCCUPIED_SYMBOL:
                    self.board[x][upperY] = ' '
                    self.board[x][upperY - 1] = OCCUPIED_SYMBOL

            
    def debugPrintBoard(self):
        rows = [[] for _ in range(len(self.board[0]))]
        for col in self.board:
            for i in range(len(col)):
                rows[i].append(col[i])

        for row in rows:
            outputString = '# '
            for cell in row:
                outputString += cell

            outputString += ' #'
            print(outputString)
        print("")


    def next(self, move: tuple, rotation: int):
        self.steps += 1
        
        message = {
            'running': True,
            'spawn': False,
            'placed': False
        }

        if self.currentPolyhex:

            newPosition = self.isValidNewPosition(self.currentPolyhex, move, rotation)
            if newPosition:
                self.removeSymbolFromBoard(self.currentHighlight)
                self.removeSymbolFromBoard(self.currentPolyhex)

                self.currentPolyhex = newPosition
                self.currentHighlight = self.dropPolyhex(self.currentPolyhex)

                self.placePolyhexOnBoard(self.currentHighlight, HIGHLIGHT_SYMBOL)
                self.placePolyhexOnBoard(self.currentPolyhex, PLAYER_SYMBOL)
                

            # every fallInterval the the polyhex will automatically be dropped by one space
            # if the polyhex can't fall anymore, it is placed as a unmovable occupied symbol
            # if the polyhex is placed, the lose condition and the row removal condition are checked
            self.timer += 1
            if (self.timer % self.fallInterval == 0):
                fallenPosition = self.isValidNewPosition(self.currentPolyhex, (0, -1), 0)
                if fallenPosition:
                    self.removeSymbolFromBoard(self.currentPolyhex)
                    self.currentPolyhex = fallenPosition
                    self.placePolyhexOnBoard(self.currentPolyhex, PLAYER_SYMBOL)
                else:
                    self.placePolyhexOnBoard(self.currentPolyhex, OCCUPIED_SYMBOL)
                    self.currentPolyhex = False
                    self.currentHighlight = []
                    message['placed'] = True

                    if self.clearRows:
                        self.newlyClearedCells = 0
                        clearedRows = 0

                        filledRows = self.filledRowsExist()
                        if filledRows:
                            for row in filledRows:
                                self.clearRow(row)
                                clearedRows += 1

                        if self.isEmptyBoard():
                            self.points += 2*(clearedRows * self.newlyClearedCells)
                        else:
                            self.points += (clearedRows * self.newlyClearedCells)
                        self.clearedRows += clearedRows
                        self.fallInterval = 30 - int(self.clearedRows / 10)

                    if self.loseConditionFulfilled(): 
                        message['running'] = False
                        self.running = False

            # staircasing detection
            # some pieces can through rotation move upwards by using the staircase structure of the border
            # if the timer runs over the theoretical maximum time a piece can spend in the air,
            # the piece is dropped and instantly placed
            if self.timer > (self.fallInterval * (self.boardSize[1] + 4)):
                self.removeSymbolFromBoard(self.currentPolyhex)
                self.placePolyhexOnBoard(self.dropPolyhex(self.currentPolyhex), OCCUPIED_SYMBOL)
                self.currentPolyhex = False
                self.currentHighlight = []
                message['placed'] = True
        else:
            message['spawn'] = True
            self.timer = 0
            if self.nextPolyhex:
                self.currentPolyhex = self.movePolyhex(self.nextPolyhex.copy(), self.spawnLocation)
            else:
                self.currentPolyhex = self.movePolyhex(self.getRandomPolyhex(), self.spawnLocation)

            self.nextPolyhex = self.getRandomPolyhex()

        return message

