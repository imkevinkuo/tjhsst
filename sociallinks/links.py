import numpy as np
import cv2
import sys
import math
import time
import random
def drawDots(edges, image):
    yl = 700
    xl = 1300
    Z = 60
    degrees = {}
    maxdv = 0
    for v in edges:
        deg = len(edges[v])
        if deg not in degrees:
            degrees[deg] = 0
        degrees[len(edges[v])] += 1
        if degrees[len(edges[v])] > maxdv:
            maxdv = degrees[len(edges[v])]
    for key in sorted(degrees.keys()):
        print(key, degrees[key])
    maxdk = max(degrees)
    #drawing things now
    cv2.circle(image,(0,0), 100000,(255,255,255),-1)
    #plot axis
    for a in range(image.shape[0]-Z,0,-int((yl-Z)/8)):
        cv2.line(image, (Z,a), (xl,a), 0)
    cv2.line(image, (0,yl-Z), (xl,yl-Z), 0)
    for b in range(Z,xl,Z*2):
        cv2.line(image, (b,0), (b,yl-Z), 0)
    cv2.line(image, (Z,0), (Z, yl), 0)
    px = 0
    py = 0
    for deg in sorted(degrees.keys()):
        lol = 600
        if rand:
            lol = 20
        x = Z + int((xl-100)*deg/lol)
        y = -Z + yl - int(yl*degrees[deg]/(maxdv*2.5))
        cv2.circle(image, (x,y), 5, (0,0,255),-1)
        if px != 0 and py != 0:
            #draw line
            cv2.line(image, (px,py), (x,y), 0,2)
        px = x
        py = y
    cv2.imshow("Links", image)
    print(sum([k*degrees[k] for k in degrees]))
    return image
##################################
edges = {}
numV = 100000 # population size
m = 3
numE = numV*m 
rand = False
#random
if rand:
    for v in range(0,numV):
        edges[v] = set()
    for e in range(0,numE): #E IS JUST A COUNTER
        e1 = int((random.random()*(numV-2))+1.9)
        e2 = int((random.random()*(numV-2))+1.9)
        # make a new friendship
        while e2 == e1 or e1 in edges[e2] or e2 in edges[e1]:
            e2 = int((random.random()*(numV-2))+1.9)
        edges[e1].add(e2)
        edges[e2].add(e1)
#popularity
else:
    popular = [] # we have 7 initial people who all know each other
    i = m*2 + 1 #7?
    ztt = [x for x in range(i)]
    for v in range(0,i):
        edges[v] = set([n for n in ztt if n != v])
        for x in range(i):
            popular.append(v)
    for v in range(i,numV): # here are all the others
        edges[v] = set()
        #add edges
        for x in range(m):
            v2 = random.choice(popular)
            while v2 in edges[v] or v2 == v:
                v2 = random.choice(popular)
            edges[v].add(v2)
            edges[v2].add(v)
            popular.append(v)
            popular.append(v2)
image = drawDots(edges, np.zeros((700,1300,3), np.uint8))
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
if k == ord('s'):
    cv2.imwrite("graph.jpg", image)
    print("saved")
