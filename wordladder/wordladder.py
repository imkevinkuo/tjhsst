import sys
import heapq
from string import ascii_lowercase
from pickle import load, dump
from time import time

## Loading data ##
def createDict():
    wordlist = set(open("words.txt").read().split())
    #stores neighbors
    dgraph = {}
    for word in wordlist:
        dgraph[word] = {}
        temp = word
        for x in range(0, 6):
            newchars = list(temp)
            temp1 = newchars[x]
            for y in range(0, 26):
                newchars[x] = ascii_lowercase[y]
                n  = "".join(newchars)
                found = False
                if n in wordlist and n != word:
                    dgraph[word][n] = 1
            if x < 5:
                temp2 = newchars[x+1]
                newchars[x] = temp2
                newchars[x+1] = temp1
                m  = "".join(newchars)
                if m in wordlist and m != word:
                    dgraph[word][m] = 5
    file = open("nbrs.pkl", "wb")
    dump(dgraph, file, protocol=3)
    file.close()
    count = 0
    for key in dgraph:
        count += len(dgraph[key])
    print("Vertices:", len(dgraph))
    print("Edges:", int(count/2))
    print("Saved in nbrs.pkl.")

## Traversal algorithms + helper ##
def path(start, end, parents):
    path = []
    while end != "ROOT" and end != "":
        path.append(end)
        end = parents[end]
    path.reverse()
    return path

def bfs(dgraph, start):
    parents = {}
    distances = {}
    visited = set()
    q = set()
    
    q.add(start)
    visited.add(start)
    distances[start] = 0
    parents[start] = "ROOT"
    
    while q:
        nextlv = set()
        for pop in q:
            for neighbor in dgraph[pop]:
                if neighbor not in visited:
                    distances[neighbor] = distances[pop]+1
                    parents[neighbor] = pop
                    visited.add(neighbor)
                    nextlv.add(neighbor)
        q = nextlv
    return parents, distances
    
def dfs(dgraph, start):
    parents = {}
    distances = {}
    visited = set()
    q = []
    
    q.append(start)
    visited.add(start)
    distances[start] = 0
    parents[start] = "ROOT"
    
    while q:
        pop = q.pop() # pop gets last item
        for neighbor in dgraph[pop]:
            if neighbor not in visited:
                distances[neighbor] = distances[pop]+1
                parents[neighbor] = pop
                visited.add(neighbor)
                q.append(neighbor)
    return parents, distances

def ijk(dgraph, start):
    parents = {v:"" for v in dgraph}
    distances = {v:float('inf') for v in dgraph}
    
    distances[start] = 0
    parents[start] = "ROOT"
    words = [(distances[v], v) for v in dgraph]
    heapq.heapify(words) # all unvisited nodes

    while words:
        pop = heapq.heappop(words)[1]
        for neighbor in dgraph[pop]:
            newdis = distances[pop] + dgraph[pop][neighbor]
            if newdis < distances[neighbor]:
                distances[neighbor] = newdis
                parents[neighbor] = pop
                heapq.heappush(words, (newdis, neighbor))
    return parents, distances

## Graph statistics ##
def diameter():
## diameter: run bfs on each independent graph component
## get all the vertices that are a 'dead end' on the graph
## run bfs on all the dead ends, get the max path
## this gives us longest path in the component
    maxDist = 0
    visited = set()
    for start in dgraph:
        if start not in visited:
            parents, distances = bfs(dgraph, start)
            ## first run only
            if maxDist == 0:
                for v in distances:
                    if v in parents.values():
                        visited.add(v)
            ##
            myMax = max(distances.values())
            if (myMax > maxDist):
                maxDist = myMax
    print("Diameter:", maxDist+1)
    
def neighbors():
    mostword = []
    mostcount = 0
    for word in dgraph:
        if len(dgraph[word]) > mostcount:
            mostword = []
            mostcount = len(dgraph[word])
        if len(dgraph[word]) == mostcount:
            mostword.append(word)
    print("Most neighbors:", mostcount)
    for word in mostword:
        print(word, ":", [key for key in dgraph[word]])

    ncount = {}
    for word in dgraph:
        if len(dgraph[word]) in ncount:
            ncount[len(dgraph[word])] += 1
        else:
            ncount[len(dgraph[word])] = 1
    print()
    print("Amount of vertices with N neighbors:")
    print("N : Amount")
    print("----------")
    for key in sorted(ncount):
        print(key,":", ncount[key])
        
def components():
    compsizes = {}
    usedwords = set()
    for word in dgraph:
        if word not in usedwords:
            size = 0
            wordstack = []
            wordstack.append(word)
            usedwords.add(word)
            while wordstack:
                size+=1
                popped = wordstack.pop()
                for neighbor in dgraph[popped]:
                    if neighbor not in usedwords:
                        wordstack.append(neighbor)
                        usedwords.add(neighbor)
            if size > 0:
                if size in compsizes:
                    compsizes[size] += 1
                else:
                    compsizes[size] = 1
    biggestsize = 0
    for key in sorted(compsizes):
        if biggestsize < key:
            biggestsize = key
    print("Largest component is size", biggestsize)
    print("Amount of components with N vertices:")
    print("N : Amount")
    print("----------")
    for key in sorted(compsizes):
        print(key,":", compsizes[key])
        
## Exits ##
def usage():
    print("Usage: wordladder.py [create/stats]")
    print("Usage: wordladder.py [bfs/dfs/ijk] startWord endWord")
    sys.exit(1)
def invalidWord(word):
    print("\'%s\' not found in words.txt." % word)
    sys.exit(2)

## Command line ##
dgraph = load(open("nbrs.pkl", "rb"))
print()
if len(sys.argv) >= 2:
    # timing
    tic = time()
    #
    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 == "create":
            createDict()
        elif arg1 == "stats":
            diameter()
            print()
            neighbors()
            print()
            components()
        else:
            usage()
    if len(sys.argv) >= 3:
        start = sys.argv[2]
        if start not in dgraph:
            invalidWord(start)
        parents = {}
        distances = {}
        cmd = sys.argv[1]
        if cmd == "bfs":
            parents, distances = bfs(dgraph, start)
        elif cmd == "dfs":
            parents, distances = dfs(dgraph, start)
        elif cmd == "ijk":
            parents, distances = ijk(dgraph, start)
        else:
            usage()
        if len(sys.argv) == 3:
            mV = max(distances, key=lambda v:distances[v])
            print("Farthest traversal: %s, %d changes" % (mV, distances[mV]))
        elif len(sys.argv) == 4:
            end = sys.argv[3]
            if end not in dgraph:
                invalidWord(end)
            if end not in distances or distances[end] == float("inf"):
                print("No path found.")
            else:
                print("Changes:", distances[end])
                print("Path:", path(start, end, parents))
        else:
            usage()
    # timing
    toc = time()
    print("\nRuntime: %f seconds" % (toc-tic))
    #
else:
    usage()
