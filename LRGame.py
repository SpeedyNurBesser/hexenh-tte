from LGame import LGame
from RGame import RGame
from constants import *

class LRGame:
    def __init__(self, polyhexSize: int, topDistance: int):
        self.polyhexSize = polyhexSize

        self.rGame = RGame(self.polyhexSize, False, False)
        #[self.convertPolyhexToOtherGrid(polyhex) for polyhex in self.rGame.polyhexSet]
        self.lGame = LGame(self.polyhexSize, False, False)
        self.currentGame = "RIGHT"
        self.running = True

        self.topDistance = topDistance
        self.boardSize = self.rGame.boardSize
        self.originDistance = self.topDistance + self.boardSize[0]

        self.newlyClearedCells = 0

        self.points = 0
        self.clearedRows = 0

        self.nextPiece

        # to get all overlapping cells 
        # all cells from the right board are translated to coordinates of the left board
        # if those coordinates are valid, i.e. are inside the borders of the left board,
        # the cell pair is saved
        # knowledge of overlappingCells is needed to syncronize them between boards

        # the heights of all overlapping cells are saved
        # knowledge of the y-coordinate of all overlapping cells is needed to differentiate between connected and unconnected rows of the same y-coordinate
        # if a y-coord is saved in overlappingHeights, there is only one single connected row, instead of two unconnected ones
        self.overlappingCells = []
        self.overlappingHeights = set()
        for x, col in enumerate(self.rGame.board):
            for y, cell in enumerate(col):
                position = (x, y)
                translatedPosition = self.translatePositionRtoL(position)
                if self.positionExists(translatedPosition):
                    self.overlappingCells.append({
                        "R": position,
                        "L": translatedPosition
                    })
                    self.overlappingHeights.add(position[1])
        self.overlappingHeights = list(self.overlappingHeights)
        self.overlappingHeights.sort()
        if self.overlappingHeights != []:
            if self.overlappingHeights[0] != 0:
                self.overlappingHeights.append(self.overlappingHeights[0] - 1)
                self.overlappingHeights.sort()
            if self.overlappingHeights[-1] != (self.boardSize[1] -1):
                self.overlappingHeights.append(self.overlappingHeights[-1] + 1)

        self.overlappingCellsPerRow = [0 for polyhex in range(self.boardSize[1])]
        for cell in self.overlappingCells:
            #print(cell)
            self.overlappingCellsPerRow[cell["R"][1]] += 1

        #print(self.overlappingCellsPerRow)

        self.steps = 0



    def translatePositionRtoL(self, position: tuple):
        return (position[0] + position[1] - self.originDistance, position[1])

    def translatePositionLtoR(self, position: tuple):
        return (position[0] - position[1] + self.originDistance, position[1])

    def convertPolyhexToOtherGrid(self, polyhex):
        # converts a given polyhex to the other coordinate system(either R to L, or L to R)
        # assuming that the origin is at the same place
        # it is different from the translatePosition methods, which translates the coordinates in respective to the altered origin
        
        # the conversion works by the realization that the two different systems used in the right and left game
        # are essentially two parts of one whole coordinate system, the so-called cube coordinate system, 
        # as it has 3 axes, q, s, and r, which run through a 2d plane with each axes being seperated from the other by 60°
        # the right-bound system uses coordinates(s, r),
        # while the left-bound system uses coordinates (q, r)
        # in the cube system all three coordinates q, s, and r always sum up to 0
        # so only two coordinates are needed to calculate the other, (q + s + r = 0 => q = -s-r)
        # also see https://www.redblobgames.com/grids/hexagons/#conversions

        # this conversion is mainly needed to save the work of generating the whole polyhex set for both the left- and right-bound board

        output = []
        for hexagon in polyhex:
            q = hexagon[0]
            r = hexagon[1]
            s = -q-r
            output.append((s, r))

        return output

    def positionExists(self, position: tuple):
        # returns True, if the given positon is not outside the borders of a board
        x = position[0]
        y = position[1]

        if x < 0 or y < 0:
            return False

        if x > (self.boardSize[0] - 1):
            return False

        if y > (self.boardSize[1] - 1):
            return False

        return True

    def pushBoards(self, fromRight: bool = True):
        for overlappingCells in self.overlappingCells:
            l = overlappingCells["L"]
            r = overlappingCells["R"]

            if fromRight:
                self.lGame.board[l[0]][l[1]] = self.rGame.board[r[0]][r[1]]
            else:
                self.rGame.board[r[0]][r[1]] = self.lGame.board[l[0]][l[1]]

    def clearFilledRows(self):
        clearedRows = 0
        self.newlyClearedCells = 0
        
        for i in range(self.boardSize[1]):
            row = self.boardSize[1] - i - 1
            # counting downwards is needed to ensure, that no further up line is removed by falling down,
            # when a line further down is cleared

            if row in self.overlappingHeights:
                if self.rGame.isFilledRow(row) and self.lGame.isFilledRow(row):
                    self.clearEntireRow(row)
                    self.newlyClearedCells += (2 * self.boardSize[0] - self.overlappingCellsPerRow[row])
                    clearedRows += 1

            else:
                if self.rGame.isFilledRow(row):
                    self.rGame.clearRow(row)
                    self.pushBoards(True)
                    clearedRows += 1
                    self.newlyClearedCells += self.boardSize[0]
                    
                if self.lGame.isFilledRow(row):
                    self.lGame.clearRow(row)
                    self.pushBoards(False)
                    clearedRows += 1
                    self.newlyClearedCells += self.boardSize[0]

        self.clearedRows += clearedRows
        self.lGame.fallInterval = 30 - int(self.clearedRows / 10)
        self.rGame.fallInterval = 30 - int(self.clearedRows / 10)

        if self.lGame.isEmptyBoard() and self.rGame.isEmptyBoard():
            self.points += 2*(clearedRows * self.newlyClearedCells)
        else:
            self.points += (clearedRows * self.newlyClearedCells)

    def clearEntireRow(self, row: int):
        # clear entire row at once, then let pieces fall
        # blocks fall on the current side first
        # then all blocks from the other side which still can fall, will fall
        # when they are not able to fall the blocks don't fuse, the block just stays at the same place
        # this gives a benefit to the the person clearing the row
        # NOTE: for TwoPlayerGames, the currentGame is equal to the side of the player who last placed a block

        if self.currentGame == "RIGHT":
            for x in range(len(self.rGame.board)):
                self.rGame.board[x][row] = ' '

            for x in range(len(self.lGame.board)):
                self.lGame.board[x][row] = ' '

            for x, _ in enumerate(self.rGame.board):
                # gets all rows above the given row
                for y in range(len(self.rGame.board[x]) - row):
                    upperY = y + row
                
                    if self.rGame.board[x][upperY] == OCCUPIED_SYMBOL:
                        self.rGame.board[x][upperY] = ' '
                        self.rGame.board[x][upperY - 1] = OCCUPIED_SYMBOL

                    self.pushBoards(True)

                    if self.lGame.board[x][upperY] == OCCUPIED_SYMBOL and self.lGame.board[x][upperY - 1] == ' ':
                        self.lGame.board[x][upperY] = ' '
                        self.lGame.board[x][upperY - 1] = OCCUPIED_SYMBOL

                    self.pushBoards(False)
        else:
            for x in range(len(self.rGame.board)):
                self.rGame.board[x][row] = ' '

            for x in range(len(self.lGame.board)):
                self.lGame.board[x][row] = ' '

            for x, _ in enumerate(self.rGame.board):
                # gets all rows above the given row
                for y in range(len(self.rGame.board[x]) - row):
                    upperY = y + row
                
                    if self.lGame.board[x][upperY] == OCCUPIED_SYMBOL:
                        self.lGame.board[x][upperY] = ' '
                        self.lGame.board[x][upperY - 1] = OCCUPIED_SYMBOL

                    self.pushBoards(False)

                    if self.rGame.board[x][upperY] == OCCUPIED_SYMBOL and self.rGame.board[x][upperY - 1] == ' ':
                        self.rGame.board[x][upperY] = ' '
                        self.rGame.board[x][upperY - 1] = OCCUPIED_SYMBOL

                    self.pushBoards(True)
            


    def next(self, move: tuple, rotation: int):
        self.steps += 1

        if self.currentGame == "RIGHT":
            message = self.rGame.next(move, rotation)
            self.nextPiece = self.lGame.nextPiece

            if not message['running']:
                self.running = False

            if message['placed']:
               self.pushBoards(True)
               self.clearFilledRows()
               self.currentGame = "LEFT"

            return message
        else:
            message = self.lGame.next(move, rotation)
            self.nextPiece = self.rGame.nextPiece

            if not message['running']:
                self.running = False
            
            if message['placed']:
               self.pushBoards(False)
               self.clearFilledRows()
               self.currentGame = "RIGHT"

            return message

