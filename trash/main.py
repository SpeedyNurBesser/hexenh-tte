import pygame
import math
from time import sleep
from rightAlignedGame import RGame
from lefttAlignedGame import LGame

HEXAGON_OUTER_RADIUS = 51
HEXAGON_INNER_RADIUS = int(0.866 * HEXAGON_OUTER_RADIUS)

def getHexagonCorners(vector: tuple, radius: int):
    baseHexagonCorners = [(0, 1),(-0.866, 0.5),(-0.866, -0.5),(0, -1),(0.866, -0.5),(0.866,0.5)]

    outputCorners = []

    for corner in baseHexagonCorners:
        stretchedX = corner[0] * radius
        stretchedY = corner[1] * radius

        movedX = stretchedX + vector[0]
        movedY = stretchedY + vector[1]

        outputCorners.append((movedX, movedY))

    return outputCorners

gridOffset = (4* HEXAGON_INNER_RADIUS, 4* HEXAGON_INNER_RADIUS)

# pygame setup
pygame.init()
pygame.display.set_caption('Place those hexes!')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
#pygame.Vector2
player_pos = [4*HEXAGON_INNER_RADIUS, 4*HEXAGON_INNER_RADIUS]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for x in range(0, 5):
        for y in range(0, 5):
            offsetVectorX = gridOffset[0] + (2*x+y)*(HEXAGON_INNER_RADIUS)
            offsetVectorY = gridOffset[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5)
            pygame.draw.polygon(screen, "gray", getHexagonCorners((offsetVectorX, offsetVectorY), HEXAGON_OUTER_RADIUS) ,1)


    pygame.draw.polygon(screen, "red", getHexagonCorners(player_pos, HEXAGON_OUTER_RADIUS),)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5
        player_pos[0] -= HEXAGON_INNER_RADIUS
        sleep(0.1)
    if keys[pygame.K_s]:
        player_pos[1] += math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5
        player_pos[0] += HEXAGON_INNER_RADIUS
        sleep(0.1)
    if keys[pygame.K_a]:
        player_pos[0] -= 2*HEXAGON_INNER_RADIUS
        sleep(0.1)
    if keys[pygame.K_d]:
        player_pos[0] += 2*HEXAGON_INNER_RADIUS
        sleep(0.1)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()