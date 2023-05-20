import time
import numpy as nump
import random
import pygame
import math
from option import Option

PURPLE = (148, 19, 165)
BLACK = ( 0, 0, 0)
WHITEBLUE = (210, 240, 245)
BLUE = (0, 0, 255)
PINKK = (255, 20, 147)
GREY = (128, 128, 128)
AI_1 = 1
AI_2 = 2
AI_1_PIECE = 2
AI_2_PIECE = 4
RECT_SIZE = 90
WID = 7 * RECT_SIZE
HEIGHT = 7 * RECT_SIZE
SZ = (WID, HEIGHT)
RAD = int(RECT_SIZE / 2 - 5)  # radius

def getNextEmptyIndex(matrix, cl):  # checks the first empty row of the selected column
    for r in range(6):
        if matrix[r][cl] == 1:
            return r

def heuristicFunction(matrix, piec):
    tot_score = 0
    # positive diagonal move
    for r in range(3):
        for c in range(4):
            arr = [matrix[r + i][c + i] for i in range(4)]
            tot_score += calcMoveScore(arr, piec)

    # negative diagonal move
    for r in range(3):
        for c in range(4):
            arr = [matrix[r + 3 - i][c + i] for i in range(4)]
            tot_score += calcMoveScore(arr, piec)

    # center column move
    values_Col4 = []
    for row in matrix:
        value = int(row[3])
        values_Col4.append(value)
    num_pieces = values_Col4.count(piec)
    tot_score += num_pieces * 4

    # horizontal move
    for r in range(6):
        rowValues = []
        for value in matrix[r, :]:
            rowValues.append(int(value))

        for c in range(4):
            arr = rowValues[c:c + 4]
            tot_score += calcMoveScore(arr, piec)

    # Vertical move
    for c in range(7):
        columnValues = []
        for value in matrix[:, c]:
            columnValues.append(int(value))

        for r in range(3):
            arr = columnValues[r:r + 4]
            tot_score += calcMoveScore(arr, piec)
    return tot_score

def calcMoveScore(arr, piece):
    tot_score = 0

    if piece == AI_2_PIECE:
        nextPiece = AI_1_PIECE
    else:
        nextPiece = AI_2_PIECE

    if arr.count(piece) == 2 and arr.count(1) == 2:
        tot_score += 2
    elif arr.count(nextPiece) == 3 and arr.count(1) == 1:
        tot_score -= 4
    elif arr.count(piece) == 4:
        tot_score += 200
    elif arr.count(piece) == 3 and arr.count(1) == 1:
        tot_score += 9

    return tot_score

def miniMax(matrix, dep, maximixingAgent):
    valid_locations = getEmptyPlaces(matrix)
    endState = (len(getEmptyPlaces(matrix)) == 0 or isWinner(matrix, AI_1_PIECE) or isWinner(matrix, AI_2_PIECE))
    if dep == 0 or endState:
        if endState:
            if isWinner(matrix, AI_2_PIECE):
                return (None, math.inf)
            elif isWinner(matrix, AI_1_PIECE):
                return (None, -math.inf)
            else:  # Game is over
                return (None, 0)
        else:  # Depth is zero
            return (None, heuristicFunction(matrix, AI_2_PIECE))
    if maximixingAgent:
        val = -math.inf
        cl = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextEmptyIndex(matrix, col)
            matrixCopy = matrix.copy()
            matrixCopy[row][col] = AI_2_PIECE
            # putPiece(matrixCopy, row, col, AI_2_PIECE)
            _,new_score = miniMax(matrixCopy, dep - 1, False)
            if new_score > val:
                val = new_score
                cl = col
        return cl, val

    else:  # MinimizingAgent
        val = math.inf
        cl = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextEmptyIndex(matrix, col)
            matrixCopy = matrix.copy()
            matrixCopy[row][col] = AI_1_PIECE
            # putPiece(matrixCopy, row, col, AI_1_PIECE)
            _,new_score = miniMax(matrixCopy, dep - 1, True)
            if new_score < val:
                val = new_score
                cl = col
        return cl, val

def MiniMaxGUI():
    flag = True
    Depth=0
    start_time = time.time()

    role = random.randint(AI_1, AI_2)
    gameOver = False
    while flag:
        GUI.fill(WHITEBLUE)
        menu = FONT.render("Difficulty level ", 1, BLACK)
        mouse = pygame.mouse.get_pos()

        MENU_RECT = menu.get_rect(center=(290, 100))

        Option_1 = Option(pos=(300, 200), input="Easy", font=get_font(25),
                          color=PINKK,
                          hover_color=GREY)
        Option_2 = Option(pos=(300, 270), input="Medium",
                          font=get_font(24), color=PINKK,
                          hover_color=GREY)

        Option_3 = Option(pos=(300, 340), input="Hard",
                          font=get_font(24), color=PINKK,
                          hover_color=GREY)

        GUI.blit(menu, MENU_RECT)
        for option in [Option_1, Option_2,Option_3]:
            option.doHover(mouse)
            option.update(GUI)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Option_1.displayInput(mouse):
                    Depth=1
                elif Option_2.displayInput(mouse):
                    Depth = 3
                elif Option_3.displayInput(mouse):
                    Depth=5
                flag = False

        pygame.display.update()

    role = random.randint(AI_1, AI_2)
    gameOver = False
    while not gameOver:

        GUI.fill("white")
        pygame.draw.rect(GUI, WHITEBLUE, (0, 0, WID, RECT_SIZE))
        if role == AI_1:
            col, score = miniMax(matrix, Depth, True)
            if matrix[5][col] == 1:
                row = getNextEmptyIndex(matrix, col)
                matrix[row][col] = AI_1_PIECE
                # putPiece(matrix, row, col, AI_1_PIECE)
                if isWinner(matrix, AI_1_PIECE):
                    label = FONT.render("Agent 1 is the winner.", 1, BLUE)
                    GUI.blit(label, (120, 10))
                    gameOver = True
                role += 1
                print(nump.flip(matrix, 0))
                displayGUI(matrix)
        time.sleep(0.4)
        if role == AI_2 and not gameOver:
            col, score = miniMax(matrix, Depth, True)

            if matrix[5][col] == 1:
                row = getNextEmptyIndex(matrix, col)
                matrix[row][col] = AI_2_PIECE
                # putPiece(matrix, row, col, AI_2_PIECE)
                if isWinner(matrix, AI_2_PIECE):
                    label = FONT.render("Agent 2 is the winner.", 1, PINKK)
                    GUI.blit(label, (120, 10))
                    gameOver = True
                role -= 1
                print(nump.flip(matrix, 0))
                displayGUI(matrix)
        time.sleep(0.4)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time: ", execution_time, " seconds")

        if gameOver:
            pygame.time.wait(2000)
        pygame.display.update()

def miniMaxByAlphaBeta(matrix, dep, alpha, beta, maximixingAgent):
    valid_locations = getEmptyPlaces(matrix)
    endState = (len(getEmptyPlaces(matrix)) == 0 or isWinner(matrix, AI_1_PIECE) or isWinner(matrix, AI_2_PIECE))
    if dep == 0 or endState:
        if endState:
            if isWinner(matrix, AI_2_PIECE):
                return (None, 100000000000000)
            elif isWinner(matrix, AI_1_PIECE):
                return (None, -10000000000000)
            else:  # Game is over
                return (None, 0)
        else:  # Depth is zero
            return (None, heuristicFunction(matrix, AI_2_PIECE))
    if maximixingAgent:
        val = -math.inf
        cl = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextEmptyIndex(matrix, col)
            matrixCopy = matrix.copy()
            matrixCopy[row][col] = AI_2_PIECE
            # putPiece(matrixCopy, row, col, AI_2_PIECE)
            _,new_score = miniMaxByAlphaBeta(matrixCopy, dep - 1, alpha, beta, False)
            if new_score > val:
                val = new_score
                cl = col
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return cl, val

    else:  # MinimizingAgent
        val = math.inf
        cl = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextEmptyIndex(matrix, col)
            matrixCopy = matrix.copy()
            matrixCopy[row][col] = AI_1_PIECE
            # putPiece(matrixCopy, row, col, AI_1_PIECE)
            _,new_score = miniMaxByAlphaBeta(matrixCopy, dep - 1, alpha, beta, True)
            if new_score < val:
                val = new_score
                cl = col
            beta = min(beta, val)
            if alpha >= beta:
                break
        return cl, val

def MiniMaxByAlphaBetaGUI():
    flag = True
    Depth = 0
    start_time = time.time()

    role = random.randint(AI_1, AI_2)
    gameOver = False
    while flag:
        GUI.fill(WHITEBLUE)
        menu = FONT.render("Difficulty level ", 1, BLACK)
        mouse = pygame.mouse.get_pos()

        MENU_RECT = menu.get_rect(center=(290, 100))

        Option_1 = Option(pos=(300, 200), input="Easy", font=get_font(30),
                          color=PINKK,
                          hover_color=GREY)
        Option_2 = Option(pos=(300, 270), input="Medium",
                          font=get_font(30), color=PINKK,
                          hover_color=GREY)

        Option_3 = Option(pos=(300, 340), input="Hard",
                          font=get_font(30), color=PINKK,
                          hover_color=GREY)

        GUI.blit(menu, MENU_RECT)
        for option in [Option_1, Option_2, Option_3]:
            option.doHover(mouse)
            option.update(GUI)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Option_1.displayInput(mouse):
                    Depth = 1
                elif Option_2.displayInput(mouse):
                    Depth = 3
                elif Option_3.displayInput(mouse):
                    Depth = 5
                flag = False

        pygame.display.update()

    role = random.randint(AI_1, AI_2)
    gameOver = False
    while not gameOver:

        GUI.fill("white")

        pygame.draw.rect(GUI, WHITEBLUE, (0, 0, WID, RECT_SIZE))
        if role == AI_1:
            col, score = miniMaxByAlphaBeta(matrix, Depth, -math.inf, math.inf, True)
            if matrix[5][col] == 1:
                row = getNextEmptyIndex(matrix, col)
                matrix[row][col] = AI_1_PIECE
                # putPiece(matrix, row, col, AI_1_PIECE)

                if isWinner(matrix, AI_1_PIECE):
                    label = FONT.render("Agent 1 is the winner.", 1, BLUE)
                    GUI.blit(label, (120, 10))
                    gameOver = True
                role += 1
                print(nump.flip(matrix, 0))
                displayGUI(matrix)
        time.sleep(0.4)
        if role == AI_2 and not gameOver:
            col, score = miniMaxByAlphaBeta(matrix, Depth, -math.inf, math.inf, True)

            if matrix[5][col] == 1:
                row = getNextEmptyIndex(matrix, col)
                matrix[row][col] = AI_2_PIECE
                # putPiece(matrix, row, col, AI_2_PIECE)

                if isWinner(matrix, AI_2_PIECE):
                    label = FONT.render("Agent 2 is the winner.", 1, PINKK)
                    GUI.blit(label, (120, 10))
                    gameOver = True
                role -= 1
                print(nump.flip(matrix, 0))
                displayGUI(matrix)
        time.sleep(0.4)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time: ", execution_time, " seconds")
        if gameOver:
            pygame.time.wait(2000)
        pygame.display.update()

def getEmptyPlaces(matrix):
    emptyPlaces = []
    for cl in range(7):
        if matrix[5][cl] == 1:
            emptyPlaces.append(cl)
    return emptyPlaces

def isWinner(matrix, piece):
    # Check horizontal win
    for c in range(4):
        for r in range(6):
            if matrix[r][c] == piece and matrix[r][c + 1] == piece and matrix[r][c + 2] == piece and matrix[r][
                c + 3] == piece:
                return True

    # Check vertical win
    for c in range(7):
        for r in range(3):
            if matrix[r][c] == piece and matrix[r + 1][c] == piece and matrix[r + 2][c] == piece and matrix[r + 3][
                c] == piece:
                return True

    # Check positive diaganols for win
    for c in range(6, -1, -1):
        for r in range(5, -1, -1):
            if matrix[r][c] == piece and matrix[r - 1][c - 1] == piece and matrix[r - 2][c - 2] == piece and \
                    matrix[r - 3][
                        c - 3] == piece:
                return True

    # Check negatively diaganols for win
    for c in range(6, -1, -1):
        for r in range(3):
            if matrix[r][c] == piece and matrix[r + 1][c - 1] == piece and matrix[r + 2][c - 2] == piece and \
                    matrix[r + 3][
                        c - 3] == piece:
                return True


def displayGUI(matrix):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(GUI, PURPLE, (c * RECT_SIZE, r * RECT_SIZE + RECT_SIZE, RECT_SIZE, RECT_SIZE))
            pygame.draw.circle(GUI, WHITEBLUE, (
                int(c * RECT_SIZE + RECT_SIZE / 2), int(r * RECT_SIZE + RECT_SIZE + RECT_SIZE / 2)), RAD)

    for c in range(7):
        for r in range(6):
            if matrix[r][c] == AI_1_PIECE:
                pygame.draw.circle(GUI, BLUE, (
                    int(c * RECT_SIZE + RECT_SIZE / 2), HEIGHT - int(r * RECT_SIZE + RECT_SIZE / 2)), RAD)
            elif matrix[r][c] == AI_2_PIECE:
                pygame.draw.circle(GUI, PINKK, (
                    int(c * RECT_SIZE + RECT_SIZE / 2), HEIGHT - int(r * RECT_SIZE + RECT_SIZE / 2)), RAD)
    pygame.display.update()

pygame.init()
matrix = nump.ones((6, 7))
print(nump.flip(matrix, 0))
GUI = pygame.display.set_mode(SZ)
FONT = pygame.font.SysFont("Georgia", 50)

def get_font(size):
    return pygame.font.SysFont("Georgia", size)
def main_menu():
    flag = True
    while flag:
        GUI.fill(WHITEBLUE)
        menu = FONT.render("Main Menu", 1, BLACK)
        mouse = pygame.mouse.get_pos()

        MENU_RECT = menu.get_rect(center=(290, 100))

        Option_1 = Option(pos=(290, 200), input="MiniMax Algorithm", font=get_font(25),
                          color=PINKK,
                          hover_color=GREY)
        Option_2 = Option(pos=(320, 300), input="MiniMax By AlphaBeta Algorithm",
                          font=get_font(24), color=PINKK,
                          hover_color=GREY)

        GUI.blit(menu,MENU_RECT)
        for option in [Option_1, Option_2]:
            option.doHover(mouse)
            option.update(GUI)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Option_1.displayInput(mouse):
                    MiniMaxGUI()
                elif Option_2.displayInput(mouse):
                    MiniMaxByAlphaBetaGUI()
                flag = False

        pygame.display.update()
main_menu()