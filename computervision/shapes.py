import numpy as np
import cv2
import sys
import math
import urllib.request
import time
def openUrlImg(url):
    with urllib.request.urlopen(url) as url:
        image = np.asarray(bytearray(url.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
def canny(img):
    newimg = cv2.Canny(img,100,200)
    edgePoints = {}
    kernelx = [-1, 0, 1,
               -2, 0, 2,
               -1, 0, 1]
    kernely = [-1,-2,-1,
                0, 0, 0,
                1, 2, 1]
    for y in range(1, img.shape[0]-2, 1):
        for x in range(1, img.shape[1]-2, 1):
            if newimg[y,x] != 0:
                pixels = []
                #store blocks
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        pixel = img[y+dy, x+dx][0]
                        pixels.append(pixel)
                #calculating gx and gy
                gx = 0
                gy = 0
                for p in range(0,9):
                    gx += pixels[p]*kernelx[p]
                    gy += pixels[p]*kernely[p]
                edgePoints[(y, x)] = (gx,gy)
    return edgePoints
def houghTransform(img, edgePoints):
    votes = {}
    whovoted = {}
    temp = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            votes[(y,x)] = 0
            whovoted[(y,x)] = set()
    for point in edgePoints:
        y1,x1 = point
        gy,gx = edgePoints[point]
        m = 0 #if gx == 0 and gy == 0
        if gx == 0 and gy != 0:
            for y in range(img.shape[0]):
                votes[(y,x1)] += 1
                whovoted[(y,x1)].add(point)
        elif gx != 0 or gy == 0:
            m = gy/gx
            for x in range(img.shape[1]):
                y = int((m*(x-x1))+y1+0.5)
                if y >= 0 and y < img.shape[0]:
                    votes[(y,x)] += 1
                    whovoted[(y,x)].add(point)
    maximum = max(votes[point] for point in votes)
    ratio = 255/maximum
    for point in votes:
        temp[point] += int(votes[point]*ratio)
    return temp, votes, whovoted
def detectCircles(img, edgePoints, nvotes, whovoted):
    votes = {}
    radii = {}
    m = 0
    for v in nvotes:
        #eliminate low counts, store radius of each point
        if nvotes[v] > m*.45:
            radii[v] = {distance(v, point2) for point2 in whovoted[v]}
            votes[v] = nvotes[v]
    elim = set()
    centerPoints = {}
    for point in votes:
        if point not in elim:
            maxP = (0,0)
            maxV = 0
            for point in votes: #gets the maximum votes point
                if point not in elim:
                    if votes[point] > maxV:
                        maxP = point
                        maxV = votes[point]
            if maxV > 0: #if there is a max
                #get radii frequency maxima
                rp = radii[maxP]
                print(rp)
                elimr = set()
                rs = set()
                while len(elimr) < len(rp):
                    maxr = max({a for a in rp if a not in elimr})
                    total = maxr
                    count = 1
                    elimr.add(maxr)
                    for r in rp:
                        if r not in elimr:
                            if r > 0.7*maxr:
                                total += r
                                count += 1
                                elimr.add(r)
                    #frequency has to be certain % of total # of points
                    if total/count > 0 and count > len(rp)*0.2:
                        rs.add(total/count)
                elim.add(maxP)
                for neighbor in votes:
                    if neighbor not in elim:
                        dist = distance(maxP, neighbor)
                        for radius in rs:
                            if dist < radius:
                                elim.add(neighbor)
                #check if circle is valid
                #inprecision from closest edgePoint
                #eliminates circles with too many edgePoints far from votes
                dvalue = -1
                for tr in rs: #test each radius
                    bad = 0
                    for ang in range(0, 360):
                        rad = math.radians(ang)
                        newx = maxP[1] + (tr*math.cos(rad))
                        newy = maxP[0] + (tr*math.sin(rad))
                        dist = set()
                        for edgePoint in edgePoints: #whovoted[maxP]?
                            d = distance((newy, newx), edgePoint)
                            dist.add(d)
                        if min(dist)/tr > 0.4:
                            bad = 1
                            break
                    if bad == 0:
                        if maxP not in centerPoints:
                            centerPoints[maxP] = set()
                        centerPoints[maxP].add(tr)
    return centerPoints
def houghLines(img, edgePoints):
    votes = {} # theta, p -> count
    pmax = 0
    for point in edgePoints:
        y,x = point
        for theta in range(0, 180):
            rad = math.radians(theta)
            p = round(x*math.cos(rad) + y*math.sin(rad))
            if p > pmax:
                pmax = p
            if (p, theta) not in votes:
                votes[(p, theta)] = 0
            votes[(p, theta)] += 1
    #accumulator
    temp = np.zeros((180,pmax+1,3), np.uint8)
    linePoints = set()
    mv = max(votes[v] for v in votes)
    for v in votes:
        p, theta = v
        temp[theta,p] = int(256*math.sqrt(votes[v]/mv)+0.5)
        if votes[v] > mv*0.45:
            rad = math.radians(theta)
            if rad == math.radians(90):
                for y in range(img.shape[0]):
                    x = ((p-(y*math.sin(rad)))/math.cos(rad))
                    if x < img.shape[1] and x > 0:
                        linePoints.add((y,x))
            else:
                for x in range(img.shape[1]):
                    y = ((p-(x*math.cos(rad)))/math.sin(rad))
                    if y < img.shape[0] and y > 0:
                        linePoints.add((y,x))
    return temp, linePoints
def displayImage(img, name):
    trim = 0
    edgePoints = {}
    aboveFloor = set()
    temp = img.copy()
    prev = temp
    savename = name[0:len(name)-4]
    prevname = ""
    huff = 0
    hl = 0
    votes = {}
    whovoted = {}
    linePoints = {}
    while True:
        cv2.imshow(name, temp)
        k = cv2.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            break
        if k == ord('s'):
            cv2.imwrite(savename + ".jpg", temp)
            print("saved")
        elif k == ord('z'):
            store = temp.copy()
            temp = prev
            prev = store
            storename = savename
            savename = prevname
            prevname = storename
        else:
            prev = temp.copy()
            prevname = savename
            if k == ord('r'):
                temp = img
                savename = name
                trim = 0
            elif k == ord('e'):
                edgePoints = canny(img)
                temp = highlightPoints(blankImage(temp), edgePoints, [0,0,0])
                savename = savename+"e"
            elif k == ord('c'):
                if huff == 1:
                    centerPoints = detectCircles(img, edgePoints, votes, whovoted)
                    #draw
                    drawPoints = set()
                    for center in centerPoints:
                        for radius in centerPoints[center]:
                            for ang in range(0, 360):
                                rad = math.radians(ang)
                                newx = (center[1] + radius*math.cos(rad))
                                newy = (center[0] + radius*math.sin(rad))
                                if newy < img.shape[0] and newy > 0 and newx < img.shape[1] and newx > 0:
                                    drawPoints.add((newy, newx))
                    temp = highlightPoints(blankImage(temp), drawPoints, [0,0,0])
                    temp = highlightPoints(temp, centerPoints, [0,0,255])
                    savename = savename+"c"
                if huff == 0:
                    temp, votes, whovoted = houghTransform(img, edgePoints)
                    huff = 1
            elif k == ord('l'):
                if hl == 1:
                    temp = highlightPoints(img, linePoints, [255,255,255])
                if hl == 0:
                    temp, linePoints = houghLines(img, edgePoints)
                    hl = 1
                savename = savename+"l"
def blankImage(img):
    temp = img.copy()
    for y in range(0, img.shape[0]):
        for x in range(0, img.shape[1]):
            temp[y,x] = [255, 255, 255]
    return temp
def highlightPoints(img, points, color):
    temp = img.copy()
    for point in points:
        temp[point] = color
    return temp
def distance(point1, point2):
    y1, x1 = point1
    y2, x2 = point2
    return math.sqrt(((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)))
########################
##### COMMAND LINE #####
########################
img = cv2.imread(sys.argv[1], -1)
new = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
for y in range(0, img.shape[0]):
    for x in range(0, img.shape[1]):
        new[y,x] = img[y,x][0:3]
    
displayImage(new, sys.argv[1])
