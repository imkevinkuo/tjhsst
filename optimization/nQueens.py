import sys
import random
import time

# "Boards" are int arrays containing all unique numbers, 1-indexed
# int element x at index y indicates a queen at row x, column y

#########################################################
## GENERAL METHODS ######################################
#########################################################

def generateBoard(n):
    board = [x for x in range(1, n+1)]
    random.shuffle(board)
    return board
def printBoard(board):
    for row in range(1, len(board)+1):
        rowstr = ""
        for col in range(0, len(board)):
            if board[col] == row:
                rowstr = rowstr + "Q "
            else:
                rowstr = rowstr + ". "
        print(rowstr)
def swap(board, x, y):
    temp = board[x]
    board[x] = board[y]
    board[y] = temp
def countConflicts(board):
    n = len(board)
    conflicts = 0
    for x in range(0, n):
        num = board[x]
        for z in range(x+1, n):
            num2 = board[z]
            if abs(num-num2) == z-x:
                conflicts += 1
                break
    return conflicts
# For backtracking: board does not have to be full to be "valid"
def valid(cfg):
    n = len(cfg)
    for i in range(n):
        for j in range(n):
            if i != j and abs(i-j) == abs(cfg[i]-cfg[j]):
                return False
    return True

#########################################################
## BACKTRACKING METHODS #################################
#########################################################

# Constructs boards one queen at a time
def helper(cfgs, n):
    for cfg in cfgs:
        if len(cfg) < n:
            for i in range(1,n+1):
                if i not in cfg:
                    ncfg = [q for q in cfg]
                    ncfg.append(i)
                    if valid(ncfg):
                        cfgs.append(ncfg)
            cfgs.remove(cfg)
    for cfg in cfgs:
        if len(cfg) < n:
            helper(cfgs,n)
            break
def nQueensBackTracking(n):
    cfgs = [[]]
    helper(cfgs,n)
    return sorted(cfgs)
        
#########################################################
## HILL CLIMBING METHODS ################################
#########################################################
    
# implement statistics for swaps and shuffles
# implement repeated trials to average statistics

#board size, board, # conflicts
def testSwaps(n, board, oldC): #returns once a lower one is found
    minC = oldC
    for x in range(0, n-1):
        for y in range(x+1, n):
            swap(board, x, y)
            newC = countConflicts(board)
            if newC < minC:
                minC = newC
            else:
                swap(board, x, y)
    return minC
# threshold for max # of shuffles
def nQueensIterative(n, threshold):
    visited = set()
    board = generateBoard(n)
    c = countConflicts(board)
    while c > 0:
        visited.add(tuple(board)) # don't need to repeat testSwaps on same board
        newC = testSwaps(n, board, c)
        if c == newC: # cannot minimize conflicts any further locally
            if threshold > 0:
                threshold -= 1
                while tuple(board) in visited:
                    board = generateBoard(n)
            else:
                print("Incomplete solution at local minimum:")
                return board
        else:
            c = newC
    return board

#########################################################
## GENETIC METHODS ######################################
#########################################################

# need to implement mutations
def babyBoard(n, board1, board2):
    pivot = int(n*0.5) # change coefficient
    part1 = board1[0:pivot]
    part2 = [x for x in board2 if x not in part1]
    return part1 + part2
def mutateBoard(board): # swap two random columns
    a = int(random.random()*len(board))
    b = int(random.random()*len(board))
    swap(board, a, b)
# Conflict distribution stats, stats = True or False
# Setting stats = True causes a considerable slowdown.
def checkSolution(n, pool, gen, stats):
    if stats:
        dist = [len([t for t in pool if countConflicts(t) == m]) for m in range(n)]
        print("Gen", gen, dist)
        if dist[0] > 0:
            return min(pool, key=lambda b:countConflicts(b))
    else:
        m = min(pool, key=lambda b:countConflicts(b))
        print("Gen", gen)
        if valid(m):
            return m
    return None
def nQueensGenetic(n, pop, gens):
    pool = [generateBoard(n) for b in range(pop)]
    gen = 0
    while True:
        s = checkSolution(n, pool, gen, False)
        if s:
            return s
        gen += 1
        newpool = []
        while len(pool) > 0:
            t1 = pool.pop()
            t2 = pool.pop()
            newpool.append(t1)
            newpool.append(t2)
            child = babyBoard(n, t1, t2)
            while child in newpool:
                mutateBoard(child)
            newpool.append(child)
        newpool.sort(key=lambda board:countConflicts(board))
        pool = newpool[:pop]
        random.shuffle(pool)
        
#########################################################
## MAIN #################################################
#########################################################

## sys.argv stuff
start = time.time()
n = 30

## GENETIC
child = nQueensGenetic(n,50,100)

## ITERATIVE
##child = nQueensIterative(n, 10)

## BACKTRACKING/BRUTE FORCE
##child = nQueensBackTracking(n)

print("Board Size:", n)
print("Time Elapsed:", "%.3f" % (time.time() - start), "sec.")
printBoard(child)
