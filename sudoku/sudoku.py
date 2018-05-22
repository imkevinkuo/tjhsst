import sys
import math
import time
global guesses
global m
global aGroups
global locations
global allSyms
global cellNeighbors
global puzzles
guesses = 0
m = 0
aGroups = {}
locations = []
allSyms = set()
cellNeighbors = []
puzzles = {}
def makePuzzles(file):
    global puzzles
    x = 1
    for line in file:
        puzzles[x] = line[:len(line)-1]
        x += 1
def printBoard(b):
    n = int(math.sqrt(m))
    for row in range(0, m):
        r = ""
        for chunk in range(0, n):
           r = r + b[(row*9)+(chunk*3):(row*9)+(chunk*3)+3]
           if chunk < n-1:
               r = r + "|"
        if row%n == 0 and row < m and row > 0:
            print("-" * 11)
        print(r)
def solveBoard(board, d): #returns either a string or False
    board = deduceBoard(board, d)
    if len(d) > 0:
        loc = findMinPos(d)
        poss = d[loc]
        if len(poss) > 0:
            global guesses
            guesses+=len(poss)-1
            for x in poss:
                dtemp = {k:set(d[k]) for k in d} #copy dictionary
                updatePossible(board, loc, x, dtemp)
                dtemp.pop(loc)
                board = board[:loc] + str(x) + board[loc+1:]
                b = solveBoard(board, dtemp)
                if b != False:
                    return b
    if len(d) == 0:
        return board
    return False
def findMinPos(d): # position with least number of possibilties
    tolerance = 0
    while tolerance < 10:
        for loc in d:
            if len(d[loc]) == tolerance:
                return loc
        tolerance += 1
    return -1
def findPossible(board): # run once at beginning, creates all possibilties
    d = {}
    for x in range(0, len(board)):
        if board[x] == '.':
            d[x] = set(allSyms - set(board[a] for a in cellNeighbors[x]))
    return d
def updatePossible(board, loc, new, d): #only reduces neighbors, does not remove loc due to concurrent modification
    for n in cellNeighbors[loc]:
        if n in d:
            if new in d[n]:
                d[n].remove(new)
    return d

## Main solver function ##
def deduceBoard(board, d):
    remove = set()
    for loc in d:
        if len(d[loc]) > 0:
            if len(d[loc]) > 1: #no need to run deductions for one possibility
                n = uniqueP(board, loc, d)
                if int(n) > 0:
                    remove.add(loc)
                    updatePossible(board, loc, n, d)
                    d[loc].clear()
                    board = board[:loc] + str(n) + board[loc+1:]
                if len(d[loc]) == 2:
                    rem = twinsN(board, loc, d)
                    for v, loc in rem:
                        remove.add(loc)
                        updatePossible(board, loc, v, d)
                        d[loc].clear()
                        board = board[:loc] + str(v) + board[loc+1:]
            else: # only one possibility for this square
                n = d[loc].pop()
                remove.add(loc)
                updatePossible(board, loc, n, d)
                board = board[:loc] + str(n) + board[loc+1:]
    for r in remove:
        d.pop(r)
    return board

## Specific algorithms ##
def uniqueP(board, loc, d):
    for grp in locations[loc]:
        s = set(d[loc])
        for n in aGroups[grp]:
            if n in d and n != loc:
                s = s - d[n]
        if len(s) == 1:
            return s.pop()
    return 0
def twinsN(board, loc, d):
    remove = set()
    for grp in locations[loc]:
        for n in aGroups[grp]:
            if n in d:
                if d[n] == d[loc] and n != loc: #found a match
                    for l in aGroups[grp]:
                        if l in d:
                            diff = d[l] - d[n]
                            if len(diff) == 1:
                                remove.add((diff.pop(), l))  #(new value, loc)
    return remove

## Helpers ##
def createGlobals(l):
    global m
    m = int(math.ceil(math.sqrt(l)))
    global allSyms
    allSyms = set(str(x+1) for x in range(m))
    global aGroups
    aGroups = createGroups(l)
    global locations
    locations = createLocations(l)
    global cellNeighbors
    cellNeighbors = createNeighbors(l)
def createLocations(l):
    locations = []
    for a in range(0, l):
        locations.append((int(a/9),9+(a%9),18 + 3*int(a/27) + math.ceil(((a%9)-2)/3)))
    return locations
def createGroups(l):
    groups = {}
    for a in range(0, m):
        groups[a] = set(range(a*9, a*9+9))
        groups[a+m] = set(range(a, a+l-1, m))
        groups[a+m+m] = set()
        for x in range(a*3 + (18*int(a/3)), a*3 + (18*int(a/3)) + 19, 9):
            groups[a+m+m] |= set(range(x, x+3))
    return groups
def createNeighbors(l):
    cn = []
    for loc in range(0, l):
        cn.append(set())
        for grp in locations[loc]:
            cn[loc] |= aGroups[grp]
        cn[loc] -= {loc}
    return cn

## Solves each puzzle ##
def sBoard(a, b):
    createGlobals(81)
    tic = time.time()
    if a == b:
        board = puzzles[a]
        printBoard(board)
        board = solveBoard(board, findPossible(board))
        if board != False:
            print()
            printBoard(board)
    else:
        boards = {}
        for x in range(a, b+1):
            board = puzzles[x]
            print("Puzzle", x)
            print(board)
            unsolved = board
            solved = solveBoard(board, findPossible(board))
            if solved != False:
                print(solved)
            else:
                print("Couldn't solve Puzzle", x)
                sys.exit(2)
            print()
    print("Guesses:", guesses)
    print("Time:", time.time() - tic)
    sys.exit(0)
    
def usage():
    print("Usage: sudoku.py [puzzle #]")
    print("Usage: sudoku.py [start] [end]")
    sys.exit(1)
    
## COMMAND LINE ##
    
f = open("sudoku128.txt")
makePuzzles(f)
f.close()
if len(sys.argv) == 2:
    if sys.argv[1].isdigit():
        sBoard(int(sys.argv[1]), int(sys.argv[1]))
elif len(sys.argv) == 3:
    if sys.argv[1].isdigit() and sys.argv[2].isdigit():
        if int(sys.argv[1]) <= int(sys.argv[2]) and int(sys.argv[1]) > 0 and int(sys.argv[2]) <= 129:
            sBoard(int(sys.argv[1]), int(sys.argv[2]))
usage()
