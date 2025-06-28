import math

HEXAGON_RADIUS = 100


def getHexagonCorners(vector: tuple, radius: int):
    corners = []

    for n in range(1, 7):
        degree = (n * 60) + 30

        x = int(radius * math.cos(math.radians(degree)))
        y = int(radius * math.sin(math.radians(degree)))
        movedX = x + vector[0]
        movedY = y + vector[1]

        corners.append((movedX, movedY))

    return corners
