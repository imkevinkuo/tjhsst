import sys
import time
import random
import math
import cv2
import numpy as np
global locations
global scaledlocs
global dists
def permutations(lis):
    pms = []
    if len(lis) == 0:
       pms.append([])
    if len(lis) == 1:
        pms.append(lis)
    if len(lis) == 2:
        pms.append(lis)
        pms.append(lis[::-1])
    if len(lis) >= 3:
        for x in range(0, len(lis)):
            nlis = lis[0:x] + lis[x+1:len(lis)]
            nperms = permutations(nlis)
            for p in nperms:
                p.append(lis[x])
                pms.append(p)
    return pms
def babyPath(p1, p2):
    pivot = int(len(p1)*random.random())
    babypath = []
    p2c = [city for city in p2]
    for x in range(0, pivot):
        babypath.append(p1[x])
        p2c.remove(p1[x])
    for x in range(0, len(p2c)):
        babypath.append(p2c[x])
    return babypath
def createPerms(n):
    return permutations([x for x in range(0, n)])
def localOptimize(path, n, xstart):
    pp = createPerms(n)
    for x in range(xstart, len(path), 1):
        points = []
        for z in range(0, n+2):
            points.append(path[(x+z)%len(path)])
        rp = points[1:n+1]
        mindis = permLength(points)
        for pn in pp:
            p = [rp[a] for a in pn]
            pl = permLength(p)
            pl += dist(locations[points[0]], locations[p[0]])
            pl += dist(locations[points[n+1]], locations[p[n-1]])
            if pl < mindis:
                mindis = pl
                rp = p
                break
        if rp != points[1:n+1]:
            for z in range(1, n+1):
                path[(x+z)%len(path)] = rp[z-1]
            return (path, x)
    return (path, -1)
def proxOptimize(path, n, xstart): #proximity optimize
    for x in range(xstart, len(path), 1):
        indexes = [] #corresponds to points
        points = [] #contains n points
        points.append(path[x])
        indexes.append(x)
        for m in range(1,n):
            mind = float('inf')
            mini = 0 #min dist index
            for i in range(0, 734):
                if i not in indexes:
                    d = dist(locations[path[i]], locations[path[x]]) 
                    if d < mind:
                       mind = d
                       mini = i
            indexes.append(mini)
            points.append(path[mini])
        #append the n-1 nearest points to x
        #and record indicies
        start = min(indexes)
        end = max(indexes)+1
        minp = path
        mindis = permLength(path[start:end])
        pp = permutations(points)
        for perm in pp:
            newp = [c for c in path]
            for x in range(0,n):
                newp[indexes[x]] = perm[x]
            pl = permLength(newp[start:end])
            if pl < mindis:
                mindis = pl
                minp = newp
                break
    return (path, -1)
def permLength(path):
    return sum(dist(locations[path[x]], locations[path[x+1]]) for x in range(0, len(path)-1))
def generatePath(n):
    path = []
    nums = [x for x in range(0, n)]
    for x in range(0, n):
        num = random.choice(nums)
        nums.remove(num)
        path.append(num)
    return path
def greedyPath(n):
    available = [x for x in range(0,n)]
    path = []
    count = 0
    path.append(4)
    available.remove(4)
    while len(available) > 0:
        mindist = float('inf')
        minc = 0
        for b in available:
            if path[count] != b:
                d = dist(locations[path[count]], locations[b])
                if d < mindist:
                    mindist = d
                    minc = b
        path.append(minc)
        available.remove(minc)
        count += 1
    return path
def pathLength(path):
    length = 0
    for x in range(0, len(path)):
        if x == len(path) - 1:
            length += dist(locations[path[x]], locations[path[0]])
        else:
            length += dist(locations[path[x]], locations[path[x+1]])
    return length
def revLength(path, x, y):
    tl = 0
    lp = len(path)
    w = (x-1+lp)%lp
    z = (y+1)%lp
    tl += dist(locations[path[w]], locations[path[y]])
    tl += dist(locations[path[x]], locations[path[z]])
    tl -= dist(locations[path[w]], locations[path[x]])
    tl -= dist(locations[path[y]], locations[path[z]])
    return tl
def swapLength(path, x, y):
    lp = len(path)
    a = (x-1+lp)%lp
    b = (x+1)%lp
    c = (y-1+lp)%lp
    d = (y+1)%lp
    tl = 0
    if abs(x-y) != 1:
        tl -= dist(locations[path[a]], locations[path[x]])
        tl -= dist(locations[path[b]], locations[path[x]])
        tl -= dist(locations[path[c]], locations[path[y]])
        tl -= dist(locations[path[d]], locations[path[y]])
        tl += dist(locations[path[a]], locations[path[y]])
        tl += dist(locations[path[b]], locations[path[y]])
        tl += dist(locations[path[c]], locations[path[x]])
        tl += dist(locations[path[d]], locations[path[x]])
    else:
        return revLength(path, x, y)
    return tl
def dist(a,b):
    if a not in dists:
        dists[a] = {}
    if b not in dists:
        dists[b] = {}
    if b not in dists[a] or a not in dists[b]:
        d = math.sqrt(((a[0]-b[0])*(a[0]-b[0]))+((a[1]-b[1])*(a[1]-b[1])))
        dists[a][b] = d
        dists[b][a] = d
    return dists[a][b]
def testSwaps(path, xstart):
    for x in range(xstart, len(path)):
        for y in range(x+1, len(path)):
            if x != y:
                nl = swapLength(path, x, y)
                if nl < -0.001:
                    p = [l for l in path]
                    p[x] = path[y]
                    p[y] = path[x]
                    return (p,x)
    return (path,-1)
def testRevs(path, xstart):
    a = xstart
    b = len(path) - 1
    for x in range(a,b):
        for y in range(x+1,b):
            tl = revLength(path, x, y)
            if tl < -0.001:
                p = [l for l in path]
                for n in range(x,y+1):
                    p[n] = path[y-n+x]
                if not organized(p):
                    p = organize(p)
                return (p,x)
    return (path,-1)
def drawDots():
    image = np.zeros((800,800,3), np.uint8)
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            image[y,x] = [255,255,255]
    for index in locations:
        y, x = locations[index]
##          ny = y - 41600
##          nx = x - 10800
##          pair = (int(ny/2.5),800 - int(nx/2.5))
        ny = y - 53000
        nx = x - 29800
        pair = (800 - int(ny/7),int(nx/7))
        scaledlocs[index] = pair
        image = cv2.circle(image,pair, 4, (0,0,255), -1)
        #image = cv2.putText(image,str(index), pair, cv2.FONT_HERSHEY_SIMPLEX, 0.3, 15)
    return image
def drawPath(path, image):
    for x in range(0,len(path)-1):
        a,b = scaledlocs[path[x]]
        c,d = scaledlocs[path[x+1]]
        image = cv2.line(image,(a, b),(c, d),(0,0,0),1)
    a,b = scaledlocs[path[len(path)-1]]
    c,d = scaledlocs[path[0]]
    image = cv2.line(image,(a, b),(c, d),(0,0,0),1)
    cv2.imshow("Salesman", image)
    cv2.waitKey(1)
    return image
def organize(path):
    newpath = []
    n = len(path)
    start = 0
    direction = 1
    to = n
    wrap = 0
    for x in range(0, n):
        if path[x] == 0:
            start = x
            if path[(x+1)%n] < path[(x-1+n)%n]:
                direction = -1
                to = -1
                wrap = n-1
            break
    minpath = []
    for z in range(start, to, direction):
        minpath.append(path[z])
    for z in range(wrap, start, direction):
        minpath.append(path[z])
    return minpath
def organized(p):
    if p[0] != 1:
        return False
    if p[1] > p[len(p)-1]:
        return False
    return True
def importPath(filename):
    R = lambda f:map(str, f.read().split())
    ls = list(R(open(filename)))
    path = []
    for s in ls:
        s = s[0:len(s)-1]
        path.append(int(s)-1)
    #print(pathLength(path))
    return path
def fitness(pathlen):
    return int((pathlen-80000)/1000)
def untangle(path):
    ts = ()
    le = 0 #left off
    ts = testRevs(path,le)
    count = 0
    while ts[1] != -1:
        count += 1
        le = ts[1]
        path = ts[0]
        ts = testRevs(path,le)
        drawPath(path, image.copy())
    return ts[0]
########################
##### COMMAND LINE #####
########################
global locations
global scaledlocs
global dists
R = lambda f:map(str, f.read().split())
#ls = list(R(open("tsp0038.txt")))
ls = list(R(open("tsp0734.txt")))
locations = {}
scaledlocs = {}
dists = {}
n = int(ls[0])
for x in range(0, n):
    locations[x] = (int(float(ls[(2*x)+1])), int(float(ls[2*x+2])))
## SHOWCASE -----------------------------------------
image = drawDots() 
path = generatePath(n)
untangle(path)
while True:
    lmao = 1
#### IMPORT --------------------------------------------
##path = importPath("in.txt")
##print([path[c]+2 for c in range(0, len(path))])
#### GENETIC -------------------------------------------
##pop = 50
###salesman.py, population size
##if len(sys.argv) == 2:
##    pop = int(sys.argv[1])
##pool = []
##print("Generating population...")
##for b in range(0, pop):
##    # do print on same line
##    bd = generatePath(n)
##    bd = untangle(bd)
##    c = pathLength(bd)
##    pool.append((c,bd))
##print("Pop generated")
##cdist = []
##gen = 0
##t = time.time()
##image = drawDots()
##try:
##    while True:
##        gen += 1
##        newgen = []
##        #create child for every two parents
##        #chance to replace worst parent
##        newpool = []
##        random.shuffle(pool)
##        while len(pool) > 0:
##            t1 = pool.pop()
##            t2 = pool.pop()
##            if t1 == t2:
##                pool.append(t2)
##                t2 = pool.pop()
##            newpool.append(t1)
##            newpool.append(t2)
##            # offspring          
##            child = babyPath(t1[1], t2[1])
##        #print(t1[0], t2[0], pathLength(child))
##            #prob = 1/(c+1)
##            # MUTATION FUNCTION?
##            #child, throwaway = testRevs(child, int(random.random()*734))
##            child = untangle(child)
##            newpool.append((pathLength(child), child))
##        #keep # of pop most fit
##        newpool.sort()
##        p = [newpool[x] for x in range(0,pop)]
##        if p == pool:
##            print("rip")
##        pool = p
##        ##calculate distribution
##        cdist = []
##        for tup in pool:
##            fit = fitness(tup[0])
##            while fit >= len(cdist):
##                cdist.append([])
##            cdist[fit].append(tup)
##        print("Gen", gen, [len(cdist[l]) for l in range(0, len(cdist))])
##        if len(cdist[0]) >= 1:
##            tup = cdist[0][0]
##            print(gen, (time.time() - t))
##            print(tup[0])
##            break
##except KeyboardInterrupt:
##    for group in cdist:
##        if len(group) > 0:
##            tup = group[0]
##            print(tup[0], tup[1])
##            drawPath(tup[1], image.copy())
##            break
##    pass
##while True:
##    lmao = 1 #to keep image displayed
#### HILL CLIMBING -----------------------------------------------
##minlen = float('inf')
##minpath = []
### dots
##image = drawDots()
##while True:
##    path = generatePath(n)
##    #path = greedyPath(n)
##    #path = importPath("in.txt")
##    ts = ()
##    # untangle
##    for m in range(3):
##        print(m)
##        drawPath(path, image.copy())
##        le = 0 #left off
##        ts = testRevs(path,le)
##        count = 0
##        while ts[1] != -1:
##            count += 1
##            le = ts[1]
##            path = ts[0]
##            ts = testRevs(path,le)
##    pl = float('inf')
##    p2 = pathLength(path)
##    # local order optimize
##    for m in range(5,7):
##        print(m)
##        le = 0
##        ts = localOptimize(path, m, le)
##        while ts[1] != -1:
##            le = ts[1]
##            path = ts[0]
##            ts = localOptimize(path, m, le)
##            drawPath(path, image.copy())
##            print(pathLength(path))
##    # local area optimize
##    for m in range(7,9):
##        print(m)
##        le = 0
##        ts = proxOptimize(path, m, le)
##        while ts[1] != -1:
##            le = ts[1]
##            path = ts[0]
##            ts = proxOptimize(path, m, le)
##            drawPath(path, image.copy())
##            print(pathLength(path))
##    pl = pathLength(path)
##    # display min
##    if pl < minlen:
##        minlen = pl
##        minpath = organize(path)
##        drawPath(minpath, image.copy())
##        minpath = [p+1 for p in minpath]
##        print("Current min:", minlen)
##        print("Path:", minpath)
##    break
