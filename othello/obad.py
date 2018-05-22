import sys
import time
import random
global neighbors
global transforms
def getRC(index):
    return((int(index/8), index%8))
def getPos(row, col):
    return(row*8 + col)
def createNeighbors():
    global neighbors
    neighbors = {}
    for x in range(0, 64):
        neighbors[x] = set()
        if (x+1)%8 != 0: #not in right column
            neighbors[x].add(x+1)
            if x > 8: #not in top
                neighbors[x].add(x-7)
            if x < 56: #not in bottom column
                neighbors[x].add(x+9)
        if x%8 != 0: #not in left column
            neighbors[x].add(x-1)
            if x > 8: #not in top
                neighbors[x].add(x-9)
            if x < 56: #not in bottom column
                neighbors[x].add(x+7)
        if x > 8:
            neighbors[x].add(x-8)
        if x < 56:
            neighbors[x].add(x+8)
def getMoves(board, turn):
    moves = set()
    opp = "O"
    if turn == "O":
        opp = "X"
    for x in range(0, 64):
        if board[x] == ".":
            for n in neighbors[x]:
                if board[n] == opp:
                    if hasAlly(board, x, n, turn, opp):
                        moves.add(x)
    if len(moves) == 0:
        moves.add("P")
    return(moves)
def printMoves(board, moves):
    for x in moves:
        if x == "P":
            break
        board = board[:x] + "*" + board[x+1:]
    printBoard(board)
def hasAlly(board, o, n, ally, opp):
    diff = n - o
    while board[n] == opp and n in neighbors[o]:
        if n%8 == 0 and (diff == -1 or diff == -9 or diff == 7):
            return False
        if (n-7)%8 == 0 and (diff == 1 or diff == -7 or diff == 9):
            return False
        o = n
        n = n + diff
        if n < 0 or n > 63:
            return False
        if board[n] == ally:
            return True
    return False
def movescore(board, pos, ally, opp):
    diffs = set()
    total = 0
    for n in neighbors[pos]:
        if board[n] == opp and hasAlly(board, pos, n, ally, opp):
            diffs.add(n - pos)
    if len(diffs) > 0:
        board = board[:pos] + ally + board[pos+1:]
        for diff in diffs:
            current = pos+diff
            while board[current] == opp:
                current = current+diff
                total+=1
    return total
def move(board, pos, ally, opp):
    diffs = set()
    for n in neighbors[pos]:
        if board[n] == opp and hasAlly(board, pos, n, ally, opp):
            diffs.add(n - pos)
    if len(diffs) > 0:
        board = board[:pos] + ally + board[pos+1:]
        for diff in diffs:
            current = pos+diff
            while board[current] == opp:
                board = board[:current] + ally + board[current+1:]
                current = current+diff
    return board
def getNextMove0(board, moves):
    return random.choice(list(moves))
def evalWinner(board):
    x = 0
    o = 0
    winner = 0
    for p in board:
        if p == 'X':
            x+=1
        if p == 'O':
            o+=1
    if x == o:
        winner = 2
    if x > o:
        winner = 0
    if x < o:
        winner = 1
    return (winner, x, o)
################
##COMMAND LINE##
################
iboard = "."*27+"OX"+"."*6+"XO"+"."*27
createNeighbors()
if len(sys.argv) > 1:
    if len(sys.argv[1]) == 64:
        board = sys.argv[1]
        pce = sys.argv[2]
        print(getNextMove0(board, getMoves(board, pce)))
    else:
        players = []
        c = 1
        if len(sys.argv) >= 3:
            for x in range(1, len(sys.argv)):
                if x < 3:
                    if sys.argv[x].isdigit() or sys.argv[x] == "c":
                        if sys.argv[x].isdigit():
                            for x in range(0, int(sys.argv[x])):
                                players.append(str(c))
                                c = c+1
                        if sys.argv[x] == "c":
                            players.append(str(c) + "C")
                            c = c+1
                    else:
                        sys.exit()
            bplayers = list(reversed(players))
            if len(sys.argv) == 4:
                if sys.argv[1] == "c" and sys.argv[2] == "c":
                    data = [0, 0, 0]
                    for x in range(0, int(sys.argv[3])):
                        if x%2 == 0:
                            i = playGame(players, iboard, True)
                            data[i[0]] += 1
                        else:
                            i = playGame(bplayers, iboard, True)
                            data[i[0]] += 1
                    print(data)
            else:
                playGame(players, iboard, False)
        sys.exit()
