import highscoreManager
import pygame
from tkinter import simpledialog
import sys
import math
import getpass
from RGame import RGame
from LGame import LGame
from LRGame import LRGame
from constants import *

gameName = "Hexenhütte"

activePlayer = getpass.getuser()

HIGHSCORES = highscoreManager.loadHighscores()

SCREEN_SIZE = (640, 360)

pygame.init()
pygame.display.set_caption(gameName)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.key.set_repeat(150, 50)
titleFont = pygame.font.SysFont(None, 40)
buttonFont = pygame.font.SysFont(None, 20)

BASE_HEXAGON_CORNERS = [(0, 1),(-0.866, 0.5),(-0.866, -0.5),(0, -1),(0.866, -0.5),(0.866,0.5)]

def drawText(text, font, color, surface, x, y, backgroundColor = False):
    textObject = font.render(text, 1, color)
    textRectangle = textObject.get_rect()
    textRectangle.topleft = (x, y)
    if backgroundColor:
        pygame.draw.rect(surface, backgroundColor, textRectangle)
    surface.blit(textObject, textRectangle)
    return textRectangle

def getHexagonCorners(radius, x, y):
    hexagonCorners = []
    for corner in BASE_HEXAGON_CORNERS:
        stretchedX = corner[0] * radius
        stretchedY = corner[1] * radius
        movedX = stretchedX + x
        movedY = stretchedY + y
        hexagonCorners.append((movedX, movedY))

    return hexagonCorners

def drawHexagon(radius, color, surface, x, y, border = False, border_width = 3, hexagon_corners = False):
    hexagonCorners = []
    if hexagon_corners:
        hexagonCorners = hexagon_corners
    else:
        hexagonCorners = getHexagonCorners(radius, x, y)

    hexagon = False
    if color:
        hexagon = pygame.draw.polygon(surface, color, hexagonCorners)
    if border:
        pygame.draw.polygon(surface, border, hexagonCorners, border_width)

    return hexagon

def pointInPolygon(x, y, polygon):
    numberOfCorners = len(polygon)
    j = numberOfCorners - 1
    inside = False

    for i in range(numberOfCorners):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        #1e-9 prevents division by zero
        # ((yi > y) != (yj > y)): the y coordinate is between two points

        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i

    return inside



def Titlescreen():
    selectedText = 0
    running = True
    click = False
    enter = False
    while running:
        screen.fill(COLOR_5)

        drawText(gameName, titleFont, COLOR_22, screen, 20, 20)

        text1 = drawText(" Single ", buttonFont, COLOR_22, screen, 30, 80)
        text2 = drawText(" Double Center ", buttonFont, COLOR_22, screen, 30, 110)
        text3 = drawText(" Double Bottom ", buttonFont, COLOR_22, screen, 30, 140)
        text4 = drawText(" Highscores ", buttonFont, COLOR_22, screen, 30, 170)
        text5 = drawText(" About ", buttonFont, COLOR_22, screen, 30, 200)

        mx, my = pygame.mouse.get_pos()

        if selectedText == 1:
            drawText(" Single ", buttonFont, (0, 0, 0), screen, 30, 80, (255, 255, 255))
            # easily the best tetrahex to fill a board
            drawHexagon(30, COLOR_6, screen, 403, 103, False)
            drawHexagon(30, COLOR_6, screen, 377, 148, False)
            drawHexagon(30, COLOR_6, screen, 429, 148, False)
            drawHexagon(30, COLOR_6, screen, 403, 193, False)

            drawHexagon(30, COLOR_2, screen, 400, 100, COLOR_1)
            drawHexagon(30, COLOR_2, screen, 374, 145, COLOR_1)
            drawHexagon(30, COLOR_2, screen, 426, 145, COLOR_1)
            drawHexagon(30, COLOR_2, screen, 400, 190, COLOR_1)
            if enter:
                PolyhexSizer("SINGLE")
        elif selectedText == 2:
            drawText(" Double Center ", buttonFont, (0, 0, 0), screen, 30, 110, (255, 255, 255))

            drawHexagon(30, COLOR_6, screen, 403, 103, False)
            drawHexagon(30, COLOR_6, screen, 429, 148, False)
            drawHexagon(30, COLOR_6, screen, 481, 148, False)
            drawHexagon(30, COLOR_6, screen, 377, 148, False)

            drawHexagon(30, COLOR_20, screen, 400, 100, COLOR_19)
            drawHexagon(30, COLOR_20, screen, 426, 145, COLOR_19)
            drawHexagon(30, COLOR_20, screen, 478, 145, COLOR_19)
            drawHexagon(30, COLOR_20, screen, 374, 145, COLOR_19)
            if enter:
                PolyhexSizer("DOUBLE_CENTER")
        elif selectedText == 3:
            drawText(" Double Bottom ", buttonFont, (0, 0, 0), screen, 30, 140, (255, 255, 255))
            drawHexagon(30, COLOR_6, screen, 403, 103, False)
            drawHexagon(30, COLOR_6, screen, 429, 148, False)
            drawHexagon(30, COLOR_6, screen, 481, 148, False)
            drawHexagon(30, COLOR_6, screen, 507, 193, False)

            drawHexagon(30, COLOR_11, screen, 400, 100, COLOR_9)
            drawHexagon(30, COLOR_11, screen, 426, 145, COLOR_9)
            drawHexagon(30, COLOR_11, screen, 478, 145, COLOR_9)
            drawHexagon(30, COLOR_11, screen, 504, 190, COLOR_9)
            if enter:
                PolyhexSizer("DOUBLE_BOTTOM")

        elif selectedText == 4:
            drawText(" Highscores ", buttonFont, (0, 0, 0), screen, 30, 170, (255, 255, 255))
            drawHexagon(30, COLOR_6, screen, 403, 103, False)
            drawHexagon(30, COLOR_6, screen, 429, 148, False)
            drawHexagon(30, COLOR_6, screen, 455, 193, False)
            drawHexagon(30, COLOR_6, screen, 481, 238, False)

            drawHexagon(30, COLOR_12, screen, 400, 100, COLOR_25)
            drawHexagon(30, COLOR_12, screen, 426, 145, COLOR_25)
            drawHexagon(30, COLOR_12, screen, 452, 190, COLOR_25)
            drawHexagon(30, COLOR_12, screen, 478, 235, COLOR_25)
            if enter:
                HighscoresModeSelect()
        elif selectedText == 5:
            drawText(" About ", buttonFont, (0, 0, 0), screen, 30, 200, (255, 255, 255))
            # the polyhex which caused me the most pain
            drawHexagon(30, COLOR_6, screen, 403, 103, False)
            drawHexagon(30, COLOR_6, screen, 429, 148, False)
            drawHexagon(30, COLOR_6, screen, 481, 148, False)
            drawHexagon(30, COLOR_6, screen, 403, 193, False)

            drawHexagon(30, COLOR_16, screen, 400, 100, COLOR_17)
            drawHexagon(30, COLOR_16, screen, 426, 145, COLOR_17)
            drawHexagon(30, COLOR_16, screen, 478, 145, COLOR_17)
            drawHexagon(30, COLOR_16, screen, 400, 190, COLOR_17)
            if enter:
                About()
        else:
            drawHexagon(30, COLOR_6, screen, 403, 103, False)
            drawHexagon(30, COLOR_6, screen, 377, 148, False)
            drawHexagon(30, COLOR_6, screen, 429, 148, False)
            drawHexagon(30, COLOR_6, screen, 403, 193, False)

            drawHexagon(30, COLOR_2, screen, 400, 100, COLOR_1)
            drawHexagon(30, COLOR_2, screen, 374, 145, COLOR_1)
            drawHexagon(30, COLOR_2, screen, 426, 145, COLOR_1)
            drawHexagon(30, COLOR_2, screen, 400, 190, COLOR_1)


        if text1.collidepoint((mx, my)):
            drawText(" Single ", buttonFont, (0, 0, 0), screen, 30, 80, (255, 255, 255))
            if click:
                PolyhexSizer("SINGLE")
        elif text2.collidepoint((mx, my)):
            drawText(" Double Center ", buttonFont, (0, 0, 0), screen, 30, 110, (255, 255, 255))
            if click:
                PolyhexSizer("DOUBLE_CENTER")
        elif text3.collidepoint((mx, my)):
            drawText(" Double Bottom ", buttonFont, (0, 0, 0), screen, 30, 140, (255, 255, 255))
            if click:
                PolyhexSizer("DOUBLE_BOTTOM")
        elif text4.collidepoint((mx, my)):
            drawText(" Highscores ", buttonFont, (0, 0, 0), screen, 30, 170, (255, 255, 255))
            if click:
                HighscoresModeSelect()
        elif text5.collidepoint((mx, my)):
            drawText(" About ", buttonFont, (0, 0, 0), screen, 30, 200, (255, 255, 255))
            if click:
                About()

        click = False
        enter = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP]:
                    if selectedText > 1:
                        selectedText -= 1
                    else:
                        selectedText = 5

                if keys[pygame.K_DOWN]:
                    if selectedText < 5:
                        selectedText += 1
                    else:
                        selectedText = 1

                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    selectedText = -1

                if keys[pygame.K_RETURN]:
                    enter = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    selectedText = 0 # would be confusing to have both selectiton through arrow keys and mouse
        pygame.display.update()
        clock.tick(60)

def PolyhexSizer(mode: str):
    # takes the mode of game selected in the GameSelector method as input and then prompts the player to enter a polyhex size between 3 and 10 for playing said game
    # starts the game with the given mode, and selected size

    # a tuple of the usual and the shadow's hexagon corners

    allHexagonCorners = [
        (getHexagonCorners(40, 75, 180), getHexagonCorners(40, 78, 183)),
        (getHexagonCorners(40, 145, 180), getHexagonCorners(40, 148, 183)),
        (getHexagonCorners(40, 215, 180), getHexagonCorners(40, 218, 183)),
        (getHexagonCorners(40, 285, 180), getHexagonCorners(40, 288, 183)),
        (getHexagonCorners(40, 355, 180), getHexagonCorners(40, 358, 183)),
        (getHexagonCorners(40, 425, 180), getHexagonCorners(40, 428, 183)),
        (getHexagonCorners(40, 495, 180), getHexagonCorners(40, 498, 183)),
        (getHexagonCorners(40, 565, 180), getHexagonCorners(40, 568, 183))
    ]

    hexagonColors = [
        (COLOR_18, COLOR_7),
        (COLOR_19, COLOR_18),
        (COLOR_16, COLOR_17),
        (COLOR_14, COLOR_15),
        (COLOR_13, COLOR_14),
        (COLOR_12, COLOR_25),
        (COLOR_25, COLOR_26),
        (COLOR_26, COLOR_27),
    ]

    running = True
    click = False
    enter = False

    currentSize = 3

    while running:

        screen.fill(COLOR_5)

        drawText("Select a polyhex size!", titleFont, COLOR_22, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        for i, cornerPair in enumerate(allHexagonCorners):
            if pointInPolygon(mx, my, cornerPair[0]):
                currentSize = i + 3
                if click:
                    SingleplayerGame(mode, currentSize)

        for i, cornerPair in enumerate(allHexagonCorners):
            currentHexagon = i + 3
            if currentHexagon <= currentSize:
                drawHexagon(0, COLOR_6, screen, 0, 0, False, False, cornerPair[1])
                drawHexagon(0, hexagonColors[currentSize - 3][0], screen, 0, 0, hexagonColors[currentSize - 3][1], 3, cornerPair[0])
            else:
                drawHexagon(0, COLOR_6, screen, 0, 0, False, False, cornerPair[0])

        drawText(str(currentSize), titleFont, COLOR_22, screen, 315, 275)

        if enter:
            SingleplayerGame(mode, currentSize)

        click = False
        enter = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] or keys[pygame.K_RIGHT]:
                    if currentSize < 10:
                        currentSize += 1

                if keys[pygame.K_DOWN] or keys[pygame.K_LEFT]:
                    if currentSize > 3:
                        currentSize -= 1

                if keys[pygame.K_RETURN]:
                    enter = True

                if keys[pygame.K_ESCAPE]:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    selectedText = 0 # would be confusing to have both selectiton through arrow keys and mouse


        pygame.display.update()
        clock.tick(60)

def SingleplayerGame(mode, polyhexSize):
    game = False

    leftOnly = False
    topDistance = 0

    if mode == "SINGLE":
        game = RGame(polyhexSize, False)
        leftOnly = True

    elif mode == "DOUBLE_BOTTOM":
        topDistance = (-1) * (2*polyhexSize+1)
        game = LRGame(polyhexSize, topDistance)

    elif mode == "DOUBLE_CENTER":
        game = LRGame(polyhexSize, topDistance)

    BOARD_SIZE = game.boardSize

    HEXAGON_INNER_RADIUS = SCREEN_SIZE[1] / (2* (BOARD_SIZE[1] + 4))
    HEXAGON_OUTER_RADIUS = HEXAGON_INNER_RADIUS / 0.866

    GRID_OFFSET = ()

    if leftOnly:
        gameWidth = ((BOARD_SIZE[0] + BOARD_SIZE[1])*HEXAGON_INNER_RADIUS)
        GRID_OFFSET = ((SCREEN_SIZE[0] - gameWidth) / 2, 4*HEXAGON_INNER_RADIUS)
    else:
        gameWidth = ((2*BOARD_SIZE[0]+topDistance)*HEXAGON_INNER_RADIUS)
        GRID_OFFSET = ((SCREEN_SIZE[0] - gameWidth) / 2, 4*HEXAGON_INNER_RADIUS)

    while game.running:
        move = [0, 0]
        rotation = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    GamePaused(game.points)

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

        game.next(move, rotation)

        screen.fill(COLOR_5)

        if leftOnly:
            for x, col in enumerate(game.board):
                for y, slot in enumerate(col):
                    if y <= (game.boardSize[1] - game.polyhexSize - 1):
                        offsetPosition = (GRID_OFFSET[0] + (2*x+y)*(HEXAGON_INNER_RADIUS),
                                        GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))
                        if slot == OCCUPIED_SYMBOL:
                            drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_26, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                        elif slot == PLAYER_SYMBOL:
                            drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_14, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                        elif slot == HIGHLIGHT_SYMBOL:
                            drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_18, border_width = 3, hexagon_corners = False)
                        else:
                            drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_2, border_width = 3, hexagon_corners = False)
        else:
            # either displays the left or the right board on top,
            # depending on the current game
            # the currentGames Board takes priority over the other
            if game.currentGame == "LEFT":

                for x, col in enumerate(game.rGame.board):
                    for y, slot in enumerate(col):
                        if y <= (game.boardSize[1] - game.polyhexSize - 1):
                            offsetPosition = (GRID_OFFSET[0] + (2*x+y)*(HEXAGON_INNER_RADIUS),
                                            GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))

                            if slot == OCCUPIED_SYMBOL:

                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_26, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == PLAYER_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_14, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == HIGHLIGHT_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_18, border_width = 3, hexagon_corners = False)
                            else:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_1, border_width = 3, hexagon_corners = False)

                for x, col in enumerate(game.lGame.board):
                    for y, slot in enumerate(col):
                        if y <= (game.boardSize[1] - game.polyhexSize - 1):
                            offsetPosition = ((2*x-y)*(HEXAGON_INNER_RADIUS) + GRID_OFFSET[0] + game.originDistance * (2*HEXAGON_INNER_RADIUS) ,
                                            GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))


                            if slot == OCCUPIED_SYMBOL:

                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_26, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == PLAYER_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_14, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == HIGHLIGHT_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_18, border_width = 3, hexagon_corners = False)
                            else:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_2, border_width = 3, hexagon_corners = False)

            else:

                for x, col in enumerate(game.lGame.board):
                    for y, slot in enumerate(col):
                        if y <= (game.boardSize[1] - game.polyhexSize - 1):
                            offsetPosition = ((2*x-y)*(HEXAGON_INNER_RADIUS) + GRID_OFFSET[0] + game.originDistance * (2*HEXAGON_INNER_RADIUS) ,
                                            GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))


                            if slot == OCCUPIED_SYMBOL:

                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_26, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == PLAYER_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_14, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == HIGHLIGHT_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_18, border_width = 3, hexagon_corners = False)
                            else:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_1, border_width = 3, hexagon_corners = False)

                for x, col in enumerate(game.rGame.board):
                    for y, slot in enumerate(col):
                        if y <= (game.boardSize[1] - game.polyhexSize - 1):
                            offsetPosition = (GRID_OFFSET[0] + (2*x+y)*(HEXAGON_INNER_RADIUS),
                                            GRID_OFFSET[1] + y*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5))

                            if slot == OCCUPIED_SYMBOL:

                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_26, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == PLAYER_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_14, screen, offsetPosition[0], offsetPosition[1], border = "black", border_width = 3, hexagon_corners = False)
                            elif slot == HIGHLIGHT_SYMBOL:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_18, border_width = 3, hexagon_corners = False)
                            else:
                                drawHexagon(HEXAGON_OUTER_RADIUS, False, screen, offsetPosition[0], offsetPosition[1], border = COLOR_2, border_width = 3, hexagon_corners = False)

        drawText(("Points: " + str(game.points)), buttonFont, COLOR_22, screen, 20, 20)
        drawText(("Cleared Rows: " + str(game.clearedRows)), buttonFont , COLOR_22, screen, 20, 40)

        if game.nextPolyhex:
            for vector in game.nextPolyhex:
                scaledVector = (
                    (2 * vector[0] + vector[1]) * (HEXAGON_INNER_RADIUS),
                    vector[1]*(math.sqrt(3) * HEXAGON_INNER_RADIUS + 1.5)
                )
                position = (scaledVector[0] + 50, scaledVector[1] + 200)
                drawHexagon(HEXAGON_OUTER_RADIUS, COLOR_1, screen, position[0], position[1], border = COLOR_2, border_width = 3)

        pygame.display.update()
        clock.tick(60)

    GameFinished(game.points, mode, polyhexSize, game.clearedRows, game.steps)

def GamePaused(points: int):
    Options("Game Paused...", [
        {
            "name": "Resume",
            "type": "CLOSE"
        },
        {
            "name": "Quit",
            "type": "SELECT",
            "function": lambda: Titlescreen()
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "Current Score: " + str(points),
            "type": "TEXT"
        }
    ])

def GameFinished(points: int, mode: str, size: int, clearedRows: int, steps: int):
    global activePlayer
    activePlayer = simpledialog.askstring(gameName, "Enter your name to submit your score!", initialvalue=activePlayer)
    if activePlayer:

        highscore = {
            "name": activePlayer,
            "score": points,
            "cleared": clearedRows,
            "steps": steps,
            "mode": mode,
            "size": size
        }

        global HIGHSCORES
        HIGHSCORES.append(highscore)
        HIGHSCORES = sorted(HIGHSCORES, key=lambda d: d['score'], reverse = True)
        highscoreManager.saveHighscores(HIGHSCORES)

    Options("Game Finished...", [
        {
            "name": "Play again",
            "type": "SELECT",
            "function": lambda: SingleplayerGame(mode, size)
        },
        {
            "name": "Quit",
            "type": "SELECT",
            "function": lambda: Titlescreen()
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "Score: " + str(points),
            "type": "TEXT"
        }
    ], False)


def GamePaused(points: int):
    Options("Game Paused...", [
        {
            "name": "Resume",
            "type": "CLOSE"
        },
        {
            "name": "Quit",
            "type": "SELECT",
            "function": lambda: Titlescreen()
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "Current Score: " + str(points),
            "type": "TEXT"
        }
    ])


def Options(title: str, options: list, escapable: bool = True):
    # structure of options
    # [
    #     {
    #         "name": "Hallo",
    #         "type": "", // TEXT, SELECT, CLOSE TODO: KEY_INPUT
    #         "function": lambda a: a+10
    #     },
    #
    # ]
    click = False
    enter = False
    selectedText = -1
    running = True
    while running:
        screen.fill(COLOR_5)

        pygame.draw.rect(screen, COLOR_6, pygame.Rect(0, 15, SCREEN_SIZE[0], 35))
        drawText(title, titleFont, COLOR_22, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        numberOfSelectTypeTexts = 0
        for id, option in enumerate(options):
            text = drawText(option["name"], buttonFont, COLOR_22, screen, 20, id * 30 + 80)
            if option["type"] == "SELECT" or option["type"] == "CLOSE":
                numberOfSelectTypeTexts += 1
                if text.collidepoint((mx, my)):
                    drawText(option["name"], buttonFont, COLOR_6, screen, 20, id * 30 + 80, COLOR_22)
                    if click:
                        if option["type"] == "SELECT":
                            option["function"]()
                        else:
                            running = False

                if selectedText == id:
                    drawText(option["name"], buttonFont, COLOR_6, screen, 20, id * 30 + 80, COLOR_22)
                    if enter:
                        if option["type"] == "SELECT":
                            option["function"]()
                        else:
                            running = False



        click = False
        enter = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE] and escapable:
                    running = False

                if keys[pygame.K_UP]:
                    if selectedText > 0:
                        selectedText -= 1
                    else:
                        selectedText = numberOfSelectTypeTexts - 1

                if keys[pygame.K_DOWN]:
                    if selectedText < (numberOfSelectTypeTexts - 1):
                        selectedText += 1
                    else:
                        selectedText = 0

                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    selectedText = -1

                if keys[pygame.K_RETURN]:
                    enter = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    selectedText = -1


        pygame.display.update()
        clock.tick(60)

def HighscoresModeSelect():
    Options(
        "Select mode to see highscores of",
        [
            {
             "name": " Single ",
             "type": "SELECT", 
             "function": lambda: HighscoresSizeSelect("SINGLE")
            },
            {
             "name": " Double Center ",
             "type": "SELECT", 
             "function": lambda: HighscoresSizeSelect("DOUBLE_CENTER")
            },
            {
             "name": " Double Bottom ",
             "type": "SELECT", 
             "function": lambda: HighscoresSizeSelect("DOUBLE_BOTTOM")
            },
            {
             "name": " Back ",
             "type": "CLOSE"
            }
        ]    
    )

def HighscoresSizeSelect(mode: str):
    Options(
        f"Select size to see highscores of",
        [
            {
             "name": " 3 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 3)
            },
            {
             "name": " 4 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 4)
            },
            {
             "name": " 5 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 5)
            },
            {
             "name": " 6 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 6)
            },
            {
             "name": " 7 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 7)
            },
            {
             "name": " 8 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 8)
            },
            {
             "name": " 9 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 9)
            },
            {
             "name": " 10 ",
             "type": "SELECT", 
             "function": lambda: Highscores(mode, 10)
            },
            {
             "name": " Back ",
             "type": "CLOSE"
            }
        ]
    )

def Highscores(mode: str, size: int):
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # matching highscores
    modeSortedHighscores = [element for element in HIGHSCORES if element['mode'] == mode]
    sortedHighscores = [element for element in modeSortedHighscores if element['size'] == size]

    chunckedHighscores = list(chunks(sortedHighscores, MAX_NUMBER_OF_HIGHSCORES_PER_PAGE))
    numberOfPages = len(chunckedHighscores)

    def generatePage(chunck, startValue = 1):
        pageName = f"Highscores ( {numberOfPages - len(chunckedHighscores)} / {numberOfPages} )"
        options = []
        for i, highscore in enumerate(chunck):
            options.append({
                "name": f"{i + startValue}. {highscore['name']} - {highscore['score']}",
                "type": "SELECT",
                "function": lambda: False
            })

        if chunckedHighscores != []:
            nextName, nextOptions = generatePage(chunckedHighscores.pop(0), startValue + MAX_NUMBER_OF_HIGHSCORES_PER_PAGE)
            options.append({
                "name": "Next Page",
                "type": "SELECT",
                "function": lambda: Options(nextName, nextOptions)
            })

        options.append({
            "name": "Back",
            "type": "CLOSE"
        })

        return pageName, options

    if chunckedHighscores == []:
        Options("It seems like there are no highscores... yet", [{"name": "Back","type": "CLOSE"}])
    else:
        defaultName, defaultOption = generatePage(chunckedHighscores.pop(0))
        Options(defaultName, defaultOption)

def About():
    Options(f"About the {gameName}", [
        {
            "name": f"{gameName} is the work in progress title of this challenging tetris-like game about",
            "type": "TEXT"
        },
        {
            "name": "stacking hexagons, or, I guess, it's about the opposite of stacking, as blocks are",
            "type": "TEXT"
        },
        {
            "name": 'placed "on bottom of each other", if that`s the expression.',
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "",
            "type": "TEXT"
        },
        {
            "name": "Anyway, thanks for playing. Enjoy.",
            "type": "TEXT"
        },
        {
            "name": "- Ole370",
            "type": "TEXT"
        }
    ])

Titlescreen()