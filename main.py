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