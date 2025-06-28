import random
import copy

OCCUPIED_SYMBOL = '@'
DIRECTIONS = [(1,0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

def movePolyhex(polyhex: list, vector: tuple):
    output = []

    for hexagon in polyhex:
        output.append((hexagon[0] + vector[0], hexagon[1] + vector[1]))

    return output


def rotatePolyhex60DegreesNtimes(polyhex: list, n:int=1):
    # returns the given polyhex rotated 60*n degrees

    def rotatePolyhex60Degrees(polyhex):
        rotatedPolyhex = []
        for hexagon in polyhex:
            originalX = hexagon[0]
            originalY = hexagon[1]

            # on a hexagonal grid plane with axial coordinates, x and y
            # a clockwise-rotation of 60° of a given point (x_o, y_o) 
            # results in a new point (y_o * (-1), x_o + y_o)
            # I am not quite sure, why this is, but I realized that it is,
            # after having stared at a series of coordinates for half an hour
            rotatedPolyhex.append((originalY * (-1), originalX + originalY))
        
        return rotatedPolyhex

    rotatedPolyhex = polyhex.copy()

    numberOfRotations = 0

    if n < 0: numberOfRotations = 6 - n
    else: numberOfRotations = n

    for _ in range(numberOfRotations):
        rotatedPolyhex = rotatePolyhex60Degrees(rotatedPolyhex)

    return rotatedPolyhex

def generatePolyhexes(n: int):
    def isContinuous(polyhex):
        visited = set()
        stack = [polyhex[0]]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for dx, dy in DIRECTIONS:
                    neighbor = (current[0] + dx, current[1] + dy)
                    if neighbor in polyhex and neighbor not in visited:
                        stack.append(neighbor)

        return len(visited) == len(polyhex)

    def transformEveryHexagonToOrigin(polyhex): 
        # returns a list of polyhexes, where for every hexagon in the polyhex the polyhex is transformed so that the hexagon is at the origin
        # exampe [(0, 0), (0, 1)] -> [[(0, 0), (0, 1)], [(0, -1), (0, 0)]]

        output = [] # list of polyhexes

        for hexagon in polyhex:
            if hexagon == (0,0):
                output.append(polyhex)
            else:
                vector = (hexagon[0] * (-1), hexagon[1] * (-1))
                output.append(movePolyhex(polyhex, vector))

        return output

    def isRotatedCopy(polyhex):
        for n in range(6):
            rotatedPolyhex = rotatePolyhex60DegreesNtimes(polyhex, n)
            rotatedPolyhex.sort()
            if rotatedPolyhex in unique_polyhexes:
                return True

        return False

    def generate(current_polyhex):
        if len(current_polyhex) == n:
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
            generate(current_polyhex + [DIRECTIONS[0]])
        else:
            for x, y in current_polyhex:
                for dx, dy in DIRECTIONS:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in current_polyhex:
                        generate(current_polyhex + [neighbor])
        

    unique_polyhexes = []

    generate([(0,0)])

    return unique_polyhexes

def spawnRandomPolyhex(polyhexes: list, spawnLocation: tuple): # returns polyhex positioned at a given spawn location
    polyhex = random.choice(polyhexes)
    spawnedPolyhex = movePolyhex(polyhex, spawnLocation)
    return spawnedPolyhex

def isValidNewPosition(polyhex: list, vector: tuple, rotation: int, board: list):
    # returns false, if move is invalid
    # returns new polyhex, if move is valid
    newPolyhex = polyhex

    if vector:
        newPolyhex = movePolyhex(polyhex, vector)
    
    if rotation:
        toOriginalPositionVector = (polyhex[0][0], polyhex[0][1])
        toOriginVector = (polyhex[0][0] * (-1), polyhex[0][1] * (-1))

        polyhexAtOrigin = movePolyhex(polyhex, toOriginVector)
        rotatedPolyhex = rotatePolyhex60DegreesNtimes(polyhexAtOrigin, rotation)
        
        newPolyhex = movePolyhex(rotatedPolyhex, toOriginalPositionVector)

    for position in newPolyhex:
        if isOccupied(board, position):
            return False

    return newPolyhex

def placePolyhexOnBoard(polyhex: list, board: list):
    newBoard = copy.deepcopy(board)

    for x, y in polyhex:
        newBoard[x][y] = OCCUPIED_SYMBOL

    return newBoard

def isOccupied(board: list, position: tuple):
    x = position[0]
    y = position[1]

    if x < 0 or y < 0:
        return True
        
    if x > (len(board) - 1):
        return True
    
    if y > (len(board[x]) - 1):
        return True

    if board[x][y] == OCCUPIED_SYMBOL:
        return True

    return False


def printBoard(board: list):
    rows = [[] for _ in range(len(board[0]))]
    for col in board:
        for i in range(len(col)):
            rows[i].append(col[i])

    for row in rows:
        outputString = '# '
        for slot in row:
            outputString += slot

        outputString += ' #'
        print(outputString)
    print("")


polyhexSize = int(input("Size: "))

gameboardSizeX = polyhexSize *4 + 1
gameboardSizeY = polyhexSize *6
origin = (0,0)
spawnLocation = (int(gameboardSizeX / 2), gameboardSizeY -5) # middle of x axes at the top of the board

board = [[' ' for i in range(gameboardSizeY)] for i in range(gameboardSizeX)]

print("The board is of size ", gameboardSizeX, " x ", gameboardSizeY)

polyhexes = generatePolyhexes(polyhexSize)

print(f"Number of unique polyhexes: {len(polyhexes)}")

running = True

currentPolyhex = None

fallTimer = 0
dt = 1

while running:
    if currentPolyhex:
        # movement and rotation stuff
        move = random.randint(0, 4)

        newPosition = False

        match move:
            case 0:
                pass
            case 1:
                newPosition = isValidNewPosition(currentPolyhex, False, 1, board)
            case 2:
                newPosition = isValidNewPosition(currentPolyhex, False, 5, board)
            case 3:
                #pass
                newPosition = isValidNewPosition(currentPolyhex, (1, 0), False, board)
            case 4:
                #pass
                newPosition = isValidNewPosition(currentPolyhex, (-1, 0), False, board)

        if newPosition:
            currentPolyhex = newPosition


        fallTimer += 1 * dt
        if (fallTimer >= 90):
            fallTimer = 0

            newPosition = isValidNewPosition(currentPolyhex, (0, -1), False, board)
            if newPosition:
                currentPolyhex = newPosition
            else:
                for position in currentPolyhex:
                    if isOccupied(board, position):
                        print("Game Over!")
                        running = False
                board = placePolyhexOnBoard(currentPolyhex, board)
                currentPolyhex = None

            printBoard(board)
    else:
        currentPolyhex = spawnRandomPolyhex(polyhexes, spawnLocation)
    


