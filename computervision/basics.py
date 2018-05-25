import numpy as np
import cv2
import sys
import math
import urllib.request
import time
def grayScale(img):
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            b = img[x,y,0]*.11
            g = img[x,y,1]*.59
            r = img[x,y,2]*.3
            e = b+g+r
            img[x,y] = [e, e, e]
    return img
def gaussianBlur(img):
    temp = img.copy()
    mat = [1,2,1,
           2,4,2,
           1,2,1]
    for col in range(1, img.shape[0]-1, 1):
        for row in range(1, img.shape[1]-1, 1):
            pixels = []
            #store blocks
            for dc in range(-1, 2):
                for dr in range(-1, 2):
                    pixel = img[col+dc, row+dr][0]
                    pixels.append(pixel)
            #modify
            g = sum(pixels[x]*mat[x] for x in range(0,9))/16
            #replace
            for dc in range(-1, 2):
                for dr in range(-1, 2):
                    temp[col+dc, row+dr] = [g,g,g]
    return temp
def openUrlImg(url):
    with urllib.request.urlopen(url) as url:
        image = np.asarray(bytearray(url.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
def detectEdges(img, threshold, floor):
    aboveFloor = {}
    edgePoints = {}
    kernelx = [-1, 0, 1,
               -2, 0, 2,
               -1, 0, 1]
    kernely = [-1,-2,-1,
                0, 0, 0,
                1, 2, 1]
    points = {}
    for col in range(1, img.shape[0]-2, 1):
        for row in range(1, img.shape[1]-2, 1):
            pixels = []
            #store blocks
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    pixel = img[col+dc, row+dr][0]
                    pixels.append(pixel)
            #calculating gx and gy
            gx = 0
            gy = 0
            for p in range(0,9):
                gx += pixels[p]*kernelx[p]
                gy += pixels[p]*kernely[p]
            #add
            g = gx**2 + gy**2
            if g > floor:
                aboveFloor[(col+dc, row+dr)] = (gx,gy)
                if g > threshold:
                    edgePoints[(col+dc, row+dr)] = (gx,gy)
    return aboveFloor, edgePoints
def roundtoNearest(radians, angles):
    closestAngle = 0
    lowestDiff = math.pi
    for angle in angles:
        if radians < 0:
            radians += math.pi
        currentDiff = abs((math.pi*angle) - radians)
        if currentDiff < lowestDiff:
            lowestDiff = currentDiff
            closestAngle = angle
    return closestAngle
def thinEdges(img, edgePoints):
    angles = {0, 1/4, 2/4, 3/4}
    newPoints = {}
    for point in edgePoints:
        gx,gy = edgePoints[point]
        #calculating arc
        arc = 1/2
        if gx == 0:
            if gy == 0:
                arc = 0
        else:
            arc = math.atan(gy/gx)
        arc = roundtoNearest(arc, angles)
        #angle maps to dx, dy
        pos = {0:(1,0), 1/4:(1,1), 2/4:(0,1), 3/4:(-1,1)}
        dx, dy = pos[arc]
        #keep condition
        if (img[point[0], point[1]][0] > img[point[0]+dx, point[1]+dy][0]) and (img[point[0], point[1]][0] > img[point[0]-dx, point[1]-dy][0]):
            newPoints[point] = edgePoints[point]
    return newPoints
def hardEdges(img, edgePoints, aboveFloor):
    toAdd = {}
    middle = {point for point in aboveFloor if point not in edgePoints}
    for point in middle:
        for dc in range(-1, 2):
            for dr in range(-1, 2):
                if (point[0]+dc, point[1]+dr) in edgePoints:
                    toAdd[point] = 0
                    break
    return toAdd
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
        x1,y1 = point
        gx,gy = edgePoints[point]
        m = 0
        if gx == 0 and gy != 0:
            for y in range(img.shape[0]):
                votes[(y,x1)] += 1
                whovoted[(y,x1)].add(point)
        else:
            m = gy/gx
            for x in range(img.shape[1]):
                y = round((m*(x-x1))+y1)
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
    m = max(nvotes[vote] for vote in nvotes)*0.6
    for v in nvotes:
        #eliminate low counts
        if nvotes[v] > m:
            votes[v] = nvotes[v]
    elim = set()
    centerPoints = {}
    for x in range(0, 16):
        maxV = 0
        maxP = (0,0)
        for point in votes:
            if point not in elim:
                if votes[point] > maxV:
                    maxP = point
                    maxV = votes[maxP]
        if maxV > 0:
            #sweeps and elims
            elim.add(maxP)
            for neighbor in votes:
                if neighbor not in elim:
                    if distance(maxP, neighbor) < 30:
                        elim.add(neighbor)
            #calc radius
            radius = sum(distance(maxP, point2) for point2 in whovoted[maxP])/maxV
            #radius and min should be similar
            minD = min(distance(maxP, point2) for point2 in whovoted[maxP])
            if abs(radius-minD) < minD:
                centerPoints[maxP] = radius
    print(centerPoints)
    return centerPoints
def distance(point1, point2):
    y1, x1 = point1
    y2, x2 = point2
    return math.sqrt(((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)))
def displayImage(img, name, threshold, floor):
    trim = 0
    edgePoints = {}
    aboveFloor = set()
    temp = img.copy()
    prev = temp
    savename = name[0:len(name)-4]
    prevname = ""
    huff = 0
    votes = {}
    whovoted = {}
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
            if k == ord('b'): #blur
                temp = gaussianBlur(temp)
                savename = name+"b"
            elif k == ord('g'):
                temp = grayScale(temp)
                savename = name+"g"
            elif k == ord('r'):
                temp = img
                savename = name
                trim = 0
            elif k == ord('e'):
##                if trim == 2:
##                    hEdges = hardEdges(img, edgePoints, aboveFloor)
##                    temp = highlightPoints(temp, hEdges, [0,0,0])
##                    savename = name+"etl"
##                if trim == 1:
##                    edgePoints = thinEdges(img, edgePoints)
##                    temp = highlightPoints(blankImage(temp), edgePoints, [0,0,0])
##                    savename = name+"et"
##                    trim = 2
##                if trim == 0:
##                    aboveFloor, edgePoints = detectEdges(img, threshold, floor)
##                    temp = highlightPoints(blankImage(temp), edgePoints, [0,0,0])
##                    savename = name+"e"
##                    trim = 1
                edgePoints = canny(img)
                temp = highlightPoints(blankImage(temp), edgePoints, [0,0,0])
                savename = name+"e"
            elif k == ord('c'):
                if huff == 1:
                    centerPoints = detectCircles(img, edgePoints, votes, whovoted)
                    #draw
                    drawPoints = set()
                    for center in centerPoints:
                        radius = centerPoints[center]
                        for ang in range(0, 360):
                            rad = math.radians(ang)
                            newx = (center[1] + radius*math.cos(rad))
                            newy = (center[0] + radius*math.sin(rad))
                            if newy < img.shape[0] and newy > 0 and newx < img.shape[1] and newx > 0:
                                drawPoints.add((newy, newx))
                    temp = highlightPoints(blankImage(temp), drawPoints, [0,0,0])
                    temp = highlightPoints(temp, centerPoints, [0,0,255])
                    savename = name+"c"
                if huff == 0:
                    temp, votes, whovoted = huffTransform(img, edgePoints)
                    huff = 1
def blankImage(img):
    temp = img.copy()
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            temp[x,y] = [255, 255, 255]
    return temp
def highlightPoints(img, points, color):
    temp = img.copy()
    for point in points:
        temp[point] = color
    return temp
########################
##### COMMAND LINE #####
########################
if len(sys.argv) >= 2:
    hthreshold = 1600
    lthreshold = 800
    if len(sys.argv) >= 3:
        hthreshold = int(sys.argv[2])
        if len(sys.argv) >= 4:
            lthreshold = int(sys.argv[3])
    img = cv2.imread(sys.argv[1], -1)
    if img is None:
        img = openUrlImg(sys.argv[1])
    displayImage(img, sys.argv[1], hthreshold, lthreshold)
