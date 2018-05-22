import sys
import time
import random
global neighbors
global transforms
def printBoard(board):
    print(" "*2 + "-"*16)
    for x in range(0, 8):
        line = ""
        for i in range(0, 8):
            c = board[x*8+i]
            if i == 8:
                line = line+c
            else:
                line = line+c+" "
        print(str(x) + "|" + line + "|" + str(x))
    print(" "*2 + "-"*16)
    print(" ", end="", flush=True)
    for c in range(0, 8):
        print(" "+str(c), end="", flush=True)
    print()
def createTransformations():
    global transforms
    transforms = {}
    types = {"I", "RL", "RR", "R2", "FX", "FY", "FD", "FO"}
    for t in types:
        l = list()
        if t == "I":
            for x in range(0, 64):
                l.append(x)
        if t == "RL":
            for x in range(0, 64):
                r,c = getRC(x)
                l.append(getPos(c, 7-r))
        if t == "RR":
            for x in range(0, 64):
                r,c = getRC(x)
                l.append(getPos(7-c, r))
        if t == "R2":
            for x in range(63, -1, -1):
                l.append(x)
        if t == "FD":
            for x in range(0, 64):
                r,c = getRC(x)
                l.append(getPos(7-c, 7-r))
        if t == "F0":
            for x in range(0, 64):
                r,c = getRC(x)
                l.append(getPos(c, r))
        if t == "FX":
            for x in range(0, 64):
                r,c = getRC(x)
                l.append(getPos(7-r, c))
        if t == "FY":
            for x in range(0, 64):
                r,c = getRC(x)
                l.append(getPos(r, 7-c))
        transforms[t] = l
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
def getMoves(board, ally):
    syms = {'X':'O', 'O':'X'}
    moves = set()
    opp = syms[ally]
    for x in range(0, 64):
        if board[x] == ".":
            for n in neighbors[x]:
                if board[n] == opp:
                    if hasAlly(board, x, n, ally, opp):
                        moves.add(x)
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
def getNextMove0(board, moves, turn):
    return random.choice(list(moves))
def getNextMove1(board, moves, turn, opp):
    maxs = 0
    maxm = getNextMove0(board, moves, turn)
    for m in moves:
        mvs = movescore(board, m, turn, opp)
        if mvs > maxs:
            maxm = m
            maxs = mvs
    return maxm
def getNextMove2(board, moves, turn, opp):
    for x in moves:
        if x == 0 or x == 7 or x == 56 or x == 63:
            return x
    return getNextMove1(board, moves, turn, opp)
def getNextMove0b(board, moves, turn, opp):
    nextToCorner = {1,14,15,6,8,9,48,49,57,54,55,62}
    newmoves = moves - nextToCorner
    if len(newmoves) > 0:
        return random.choice(list(newmoves))
    return getNextMove0(board, moves, turn)
def getNextMove3(board, moves, turn, opp):
    syms = {"X":0, "O":1}
    minmoves = 64
    minmove = getNextMove0(board, moves, turn)
    for m in moves:
        newboard = move(str(board), m, turn, opp)
        enemyMoves = getMoves(newboard, syms[opp])
        if len(enemyMoves) < minmoves:
            minmoves = len(enemyMoves)
            minmove = m
    return m
#x positive, o negative
def getNextMoveMM(board, turn, opp, depth, maxdepth): #minimax
    bestmove = -1
    bestscore = -float('inf')
    if turn == 'O':
        bestscore = float('inf')
    if depth == maxdepth:
        bestscore = evalScore(board)
    else:
        moves = getMoves(board, turn)
        if len(moves) == 0:
            bestscore = evalScore(board)
        else:
            for m in moves:
                cboard = move(str(board), m, turn, opp)
                score, bm = getNextMoveMM(
                    cboard, opp, turn, depth+1, maxdepth)
                if better(score, bestscore, turn):
                    bestscore = score
                    bestmove = m
    return (bestscore, bestmove)
def getNextMoveAB(board, turn, opp, depth, maxdepth, a, b): #alphabeta
    bestmove = -1
    if depth == maxdepth:
        return (evalScore(board), -1)
    moves = getMoves(board, turn)
    if len(moves) == 0:
        return (evalScore(board), -1)
    if turn == 'X':
        bestscore = -float('inf')
        for m in moves:
            cboard = move(str(board), m, turn, opp)
            score, bm = getNextMoveAB(
                cboard, opp, turn, depth+1, maxdepth, a, b)
            bestscore = max(bestscore, score)
            a = max(a, bestscore)
            if b <= a:
                break
            if score == bestscore:
                bestmove = m
    if turn == 'O':
        bestscore = float('inf')
        for m in moves:
            cboard = move(str(board), m, turn, opp)
            score, bm = getNextMoveAB(
                cboard, opp, turn, depth+1, maxdepth, a, b)
            bestscore = min(bestscore, score)
            b = min(b, bestscore)
            if b <= a:
                break
            if score == bestscore:
                bestmove = m
    return (bestscore, bestmove)
def better(score, bestscore, turn):
    if turn == 'X':
        return score > bestscore
    if turn == 'O':
        return score < bestscore
def evalScore(board):
    score = 0
    empty = 0
    for b in board:
        if b == '.':
            empty += 1
    if empty <= 8:
        score = 0
        for b in board:
            if b == 'X':
                score+=1
            if b == 'O':
                score-=1
    else:
        for p in {0, 7, 56, 63}:
            if board[p] == 'X':
                score += 100
            if board[p] == 'O':
                score -= 100
    return score
def playGame(players, board, fast, rev):
    play = 0
    global transforms
    syms = ["X", "O"]
    turn = 0
    passed = False
    winner = 0
    rot = "I"
    while True:
        m = getMoves(board, syms[turn])
        if not fast:
            if rot == "I":
                printMoves(board, m)
            else:
                printBoard([board[x] for x in transforms[rot]])
        if len(m) > 0:
            inp = ""
            pos = -1
            #COMPUTER INPUT ------------------------------------
            if players[turn].endswith("C"):
                mt = turn
                if rev:
                    mt = 1 - turn
                if players[mt] == "1C":
                    pos = getNextMove0(board, m, syms[turn])
                if players[mt] == "2C":
                    empty = 0
                    depth = 2
                    for b in board:
                        if b == '.':
                            empty += 1
                    if empty <= 8:
                        depth = empty
                    score, pos = getNextMoveMM(board, syms[turn], syms[1-turn], 0, depth)
            else:
                ####
                #print("Player " + syms[turn] + ":", end = " ", flush = True)
                inp = input()
            #PLAYER INPUT, ROTATION OR MOVE
            row, col = -1, -1
            if len(inp) == 1 or len(inp) == 2: #index or rot
                if inp[0].isdigit():
                    pos = int(inp)
                else:
                    if inp.upper() in transforms:
                        rot = inp.upper()
            elif pos == -1:
                for c in inp:
                    if c.isdigit():
                        if row == -1:
                            row = int(c)
                        elif col == -1:
                            col = int(c)
                pos = row*8 + col
            #PLACE THE PIECE
            if pos in m:
                board = move(board, pos, syms[turn], syms[1-turn])
                turn = 1 - turn
            passed = False
        else:
            if passed:
                winner = evalWinner(board, rev)
                if not fast:
                    print(str(winner[1]) + " - " + str(winner[2]))
                if winner != 2 and rev:
                    return 1 - winner[0]
                return winner[0]
            else:
                turn = 1 - turn
                passed = True
def evalWinner(board, rev):
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
dct = {"X":0, "O":1, 0:"X", 1:"O"}
iboard = "."*27+"OX"+"."*6+"XO"+"."*27
createNeighbors()
createTransformations()
if len(sys.argv) > 1:
    if len(sys.argv[1]) == 64:
        board = sys.argv[1]
        pce = sys.argv[2]
        ####
        empty = 0
        depth = 2
        for b in board:
            if b == '.':
                empty += 1
        if empty > 54:
            print(getNextMove0(board, getMoves(board, pce), pce))
        if empty <= 8:
            depth = empty
        score, pos = getNextMoveMM(board, pce, dct[1-dct[pce]], 0, depth)
        ####
        print(pos)
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
            if len(sys.argv) == 4:
                if sys.argv[1] == "c" and sys.argv[2] == "c":
                    data = [0, 0, 0]
                    for x in range(0, int(sys.argv[3])):
                        if x%2 == 0:
                            data[playGame(players, iboard, True, False)] += 1
                        else:
                            data[playGame(players, iboard, True, True)] += 1
                    print("C1: " + str(data[0]) + " C2: " + str(data[1]) + " T: " + str(data[2]))
            else:
                playGame(players, iboard, False, False)
        sys.exit()
