import sys
import queue
from time import time
from math import pi , acos , sin , cos

def calcd(y1,x1, y2,x2):
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   R   = 3958.76 # miles
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0 
   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

#get the path using heuristics
#f = g + h, g = distance from start, h = distance from end
def As(start, end):
   popped = set()
   maxq = 0
   visited = set()
   parents = {}
   distances = {}
   q = queue.PriorityQueue()
   q.put((calcd(
      locations[start][0],locations[start][1],
         locations[end][0],locations[end][1]), start))
   for key in locations:
       distances[key] = float("inf")
   visited.add(start)
   distances[start] = 0
   parents[start] = "ROOT"
   while q.qsize() > 0:
      maxq = max(q.qsize(), maxq)
      pop = q.get()[1]
      if pop in edges:
         popped.add(pop)
         for neighbor in edges[pop]:
            newdis = distances[pop] + edges[pop][neighbor]
            if newdis < distances[neighbor]:
               visited.add(neighbor)
               distances[neighbor] = newdis
               z = (newdis + calcd(
                  locations[neighbor][0],locations[neighbor][1],
                     locations[end][0],locations[end][1]), neighbor)
               q.put(z)
               parents[neighbor] = pop
         if end in edges[pop]:
            q = queue.PriorityQueue()
   if distances[end] == float('inf'):
      print("No path found.")
   else:
      print("Distance:", distances[end])
      print("Path len:", len(path(start,end,parents)), "stops")
   print("Nodes visited: %s, Max queue: %s" % (len(popped), maxq))
def twoijk(start, end):
   popped = set()
   maxq = 0
   visited = set()
   parents = {}
   distances = {}
   q = queue.PriorityQueue()
   q.put((0, start))
   for key in locations:
       distances[key] = float("inf")
   visited.add(start)
   distances[start] = 0
   parents[start] = "ROOT"
   while q.qsize() > 0:
      maxq = max(q.qsize(), maxq)
      pop = q.get()[1]
      if pop in edges:
         popped.add(pop)
         for neighbor in edges[pop]:
            newdis = distances[pop] + edges[pop][neighbor]
            if newdis < distances[neighbor]:
               visited.add(neighbor)
               distances[neighbor] = newdis
               q.put((newdis, neighbor))
               parents[neighbor] = pop
         if end in edges[pop]:
            count = 0
            for endn in edges[end]:
               if endn in visited:
                  count+=1
               if count == len(edges[end]):
                  q = queue.PriorityQueue()
   if distances[end] == float('inf'):
      print("No path found.")
   else:
      print("Distance:", distances[end])
      print("Path len:", len(path(start,end,parents)), "stops")
   print("Nodes visited: %s, Max queue: %s" % (len(popped), maxq))
def path(start, end, parents):
   path = []
   while end != "ROOT" and end != "":
      path.append(end)
      end = parents[end]
   path.reverse()
   return path
############################################################
tic = time()
R = lambda f:map(str, f.read().split())
l = list(R(open("rrNodes.txt")))
m = list(R(open("rrEdges.txt")))
nl = open("rrNodeCity.txt")
locations = {}
for x in range(0, len(l), 3):
    locations[l[x]] = [float(l[x+1]), float(l[x+2])]
edges = {}
for x in range(0, len(m), 2):
   if m[x] not in edges:
      edges[m[x]] = {}
   if m[x+1] not in edges:
      edges[m[x+1]] = {}
   z = calcd(
       locations[m[x]][1],locations[m[x]][0],
            locations[m[x+1]][1],locations[m[x+1]][0])
   edges[m[x]][m[x+1]] = z
   edges[m[x+1]][m[x]] = z
cities = {}
for line in nl:
   n = line.split()
   cities[n[0]] = ' '.join(n[1:])
print("\nFile load time: %f seconds\n" % (time()-tic))
################
##COMMAND LINE##
################
if len(sys.argv) == 3:
   if sys.argv[1] in locations and sys.argv[2] in locations:
      ticA = time()
      print("-- A* --")
      As(sys.argv[1], sys.argv[2])
      ticB = time()
      print("Runtime: %f sec." % (ticB-ticA))
      print("-- Dijkstra's --")
      twoijk(sys.argv[1], sys.argv[2])
      print("Runtime: %f sec." % (time()-ticB))
   else:
       print("Invalid input.")
