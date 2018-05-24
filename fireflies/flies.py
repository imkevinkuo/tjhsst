import numpy as np
import cv2
import sys
import math
import time
import random
threshold = 100
def fx(x):
    return 1 - np.exp(-x)
def dfx(x):
    return np.exp(x)
def drawDots(locations, image):
    time = 0.05
    flashed = set()
    for pair in locations:
        z = locations[pair] # Z = INTERNAL TIME
        if z > 4:
            locations[pair] = 0
            flashed.add(pair)
        else:
            locations[pair] = z + time
            a = 255 - fx(locations[pair])*260 # INTENSITY
            image = cv2.circle(image,pair, 8, (0,a,a), -1)
    for pair in flashed:
        for pair2 in neighborhoods[pair]:
            if pair2 not in flashed:
                if locations[pair2] > 0.1:
                    locations[pair2] = locations[pair2] + 0.015
    cv2.imshow("Fireflies", image)
    cv2.waitKey(1)
    return image
def distance(p1, p2):
    a = abs(p1[0]-p2[0])
    b = abs(p1[1]-p2[1])
    return math.sqrt(a*a + b*b)
##################################
locations = {}
neighborhoods = {}
ndist = 1000
for loc in range(0, 100):
    xl = int(random.random()*700)+50
    yl = int(random.random()*700)+50
    x = random.random()*3
    intensity = int(random.random()*255)
    locations[(yl,xl)] = x
    neighborhoods[(yl,xl)] = set()
for loc1 in neighborhoods:
    for loc2 in locations:
        if distance(loc1,loc2) < ndist and loc1 != loc2:
            neighborhoods[loc1].add(loc2)
while True:
    drawDots(locations, np.zeros((800,800,3), np.uint8))
