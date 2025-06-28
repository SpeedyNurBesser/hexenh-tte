from RGame import RGame

import copy

class LGame(RGame):
    def __init__(self, polyhexSize: int, polyhexSet, clearRows: bool = True):
        #self.DIRECTIONS = [(1,0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1)]
        super().__init__(polyhexSize, polyhexSet, clearRows)

    def generatePolyhexesSet(self, size: int):
        DIRECTIONS = [(1,0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1)]
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
                generate(current_polyhex + [DIRECTIONS[0]])
            else:
                for x, y in current_polyhex:
                    for dx, dy in DIRECTIONS:
                        neighbor = (x + dx, y + dy)
                        if neighbor not in current_polyhex:
                            generate(current_polyhex + [neighbor])

        def transformEveryHexagonToOrigin(polyhex): 
                # returns a list of polyhexes, where for every hexagon in the polyhex the polyhex is transformed so that the hexagon is at the origin
                # example: [(0, 0), (0, 1)] -> [[(0, 0), (0, 1)], [(0, -1), (0, 0)]]

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

    def rotatePolyhex(self, polyhex: list, clockwise: bool = True):
        # on a hexagonal grid plane with axial coordinates, x and y,
        # where the y axes is sitting on the x-axes with 60° tilt to the right
        # a clockwise-rotation of 60° of a given point (x_o, y_o) around the orgin 
        # always results in a new point with the coordinates (x_o + y_o, -x_o)
        # a anti-clockwise-rotation of 60° leads to the new point (-y_o, x_o + y_o)

        def rotatePolyhex60DegClockwise(polyhex):
            rotatedPolyhex = []
            for hexagon in polyhex:
                originalX = hexagon[0]
                originalY = hexagon[1]

                rotatedPolyhex.append((originalX - originalY, originalX))

            return rotatedPolyhex

        def rotatePolyhex60DegAntiClockwise(polyhex):
            rotatedPolyhex = []
            for hexagon in polyhex:
                originalX = hexagon[0]
                originalY = hexagon[1]
                
                rotatedPolyhex.append((originalY, originalY - originalX))

            return rotatedPolyhex

        rotatedPolyhex = []

        if clockwise:
            rotatedPolyhex = rotatePolyhex60DegClockwise(polyhex)
        else:
            rotatedPolyhex = rotatePolyhex60DegAntiClockwise(polyhex)

        return rotatedPolyhex
  