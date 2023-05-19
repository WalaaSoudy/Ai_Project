import time
import numpy as nump
import random
import pygame
import math

PURPLE = (148, 19, 165)
BLACK = (0, 0, 0)
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


def getEmptyPlaces(matrix):
    emptyPlaces = []
    for cl in range(7):
        if matrix[5][cl] == 1:
            emptyPlaces.append(cl)
    return emptyPlaces


def isWinner(matrix, piece):
    # test horizontal
    for c in range(4):
        for r in range(6):
            if matrix[r][c] == piece and matrix[r][c + 1] == piece and matrix[r][c + 2] == piece and matrix[r][
                    c + 3] == piece:
                return True

    # test vertical
    for c in range(7):
        for r in range(3):
            if matrix[r][c] == piece and matrix[r + 1][c] == piece and matrix[r + 2][c] == piece and matrix[r + 3][
                    c] == piece:
                return True

    # test positive diaganols
    for c in range(6, -1, -1):
        for r in range(5, -1, -1):
            if matrix[r][c] == piece and matrix[r - 1][c - 1] == piece and matrix[r - 2][c - 2] == piece and \
                    matrix[r - 3][
                        c - 3] == piece:
                return True

    # test negative diaganols
    for c in range(6, -1, -1):
        for r in range(3):
            if matrix[r][c] == piece and matrix[r + 1][c - 1] == piece and matrix[r + 2][c - 2] == piece and \
                    matrix[r + 3][
                        c - 3] == piece:
                return True


def miniMax(matrix, dep, maximixingAgent):
    valid_locations = getEmptyPlaces(matrix)
    endState = (len(getEmptyPlaces(matrix)) == 0 or isWinner(
        matrix, AI_1_PIECE) or isWinner(matrix, AI_2_PIECE))
    if dep == 0 or endState:
        if endState:
            if isWinner(matrix, AI_2_PIECE):
                return (None, math.inf)
            elif isWinner(matrix, AI_1_PIECE):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, heuristicFunction(matrix, AI_2_PIECE))
    if maximixingAgent:
        val = -math.inf
        cl = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextEmptyIndex(matrix, col)
            matrixCopy = matrix.copy()
            matrixCopy[row][col] = AI_2_PIECE
            _, new_score = miniMax(matrixCopy, dep - 1, False)
            if new_score > val:
                val = new_score
                cl = col
        return cl, val

    else:
        val = math.inf
        cl = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextEmptyIndex(matrix, col)
            matrixCopy = matrix.copy()
            matrixCopy[row][col] = AI_1_PIECE
            _, new_score = miniMax(matrixCopy, dep - 1, True)
            if new_score < val:
                val = new_score
                cl = col
        return cl, val


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


def displayGUI(matrix):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(GUI, PURPLE, (c * RECT_SIZE, r *
                             RECT_SIZE + RECT_SIZE, RECT_SIZE, RECT_SIZE))
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
