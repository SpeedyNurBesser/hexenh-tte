import pygame
import math
from RGame import RGame
from LGame import LGame
from LRGame import LRGame

from constants import *

SCREEN_SIZE = (640, 360)

game = LRGame(4, -9)
game.lGame.board[1][3] = OCCUPIED_SYMBOL

#game.board[0][3] = OCCUPIED_SYMBOL

HEXAGON_INNER_RADIUS = SCREEN_SIZE[1] / (2* (game.boardSize[1] + 4))
HEXAGON_OUTER_RADIUS = HEXAGON_INNER_RADIUS / 0.866

BASE_HEXAGON_CORNERS = [(0, 1),(-0.866, 0.5),(-0.866, -0.5),(0, -1),(0.866, -0.5),(0.866,0.5)]

GRID_OFFSET = (16* HEXAGON_INNER_RADIUS, 4* HEXAGON_INNER_RADIUS)

def getHexagonCorners(vector: tuple, radius: int):
    outputCorners = []

    for corner in BASE_HEXAGON_CORNERS:
        stretchedX = corner[0] * radius
        stretchedY = corner[1] * radius

        movedX = stretchedX + vector[0]
        movedY = stretchedY + vector[1]

        outputCorners.append((movedX, movedY))

    return outputCorners

pygame.init()
pygame.display.set_caption('Place those hexes!')
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0
pygame.key.set_repeat(150, 50)


while running:
    move = [0, 0]
    rotation = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                move[1] -= 1
            if keys[pygame.K_s]:
                move[1] += 1 # a move upwards is interpreted as a drop
            if keys[pygame.K_a]:
                move[0] -= 1
            if keys[pygame.K_d]:
                move[0] += 1

            if keys[pygame.K_q]:
                rotation -= 1
            if keys[pygame.K_e]:
                rotation += 1

    screen.fill("black")

    for x, col in enumerate(game.rGame.board):
        for y, slot in enumerate(col):
            if y <= (game.boardSize[1] - game.polyhexSize - 1):
                offsetPosition = (GRID_OFFSET[0] + (2*x+y)*(HEXAGON_INNER_RADIUS),
                                GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))

                if slot == OCCUPIED_SYMBOL:
                    pygame.draw.polygon(screen, "red", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS))
                    pygame.draw.polygon(screen, "black", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS), 3)
                elif slot == PLAYER_SYMBOL:
                    pygame.draw.polygon(screen, "green", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS))
                    pygame.draw.polygon(screen, "black", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS), 1)
                elif slot == HIGHLIGHT_SYMBOL:
                    pygame.draw.polygon(screen, "blue", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS), 1)
                else:
                    pygame.draw.polygon(screen, "gray", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS) ,1)

    for x, col in enumerate(game.lGame.board):
        for y, slot in enumerate(col):
            if y <= (game.boardSize[1] - game.polyhexSize - 1):
                offsetPosition = ((2*x-y)*(HEXAGON_INNER_RADIUS) + GRID_OFFSET[0] + game.originDistance * (2*HEXAGON_INNER_RADIUS) ,
                                GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))

                if slot == OCCUPIED_SYMBOL:
                    pygame.draw.polygon(screen, "red", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS))
                    pygame.draw.polygon(screen, "black", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS), 3)
                elif slot == PLAYER_SYMBOL:
                    pygame.draw.polygon(screen, "green", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS))
                    pygame.draw.polygon(screen, "black", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS), 1)
                elif slot == HIGHLIGHT_SYMBOL:
                    pygame.draw.polygon(screen, "blue", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS), 1)
                else:
                    pygame.draw.polygon(screen, "gray", getHexagonCorners(offsetPosition, HEXAGON_OUTER_RADIUS) ,1)



    # draw next piece
    if game.rGame.nextPolyhex:
        for vector in game.rGame.nextPolyhex:
            scaledVector = (
                (2 * vector[0] - vector[1]) * (HEXAGON_INNER_RADIUS),
                vector[1]*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5)
                )
            position = (scaledVector[0] + 50, scaledVector[1] + 200)

            pygame.draw.polygon(screen, "red", getHexagonCorners(position, HEXAGON_OUTER_RADIUS))



    game.next(move, rotation)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_k]:
        game.debugPrintBoard()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    if not game.running:
        print("GAME OVER!")

pygame.quit()

