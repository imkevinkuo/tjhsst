# tjhsst
  
A compilation of my high school projects/assignments.  
Graph Traversal Algorithms: [Word Ladder](#wordladder), [Rail Road](#railroad)  
Game Automation: [Sudoku](#sudoku), [Ghost](#ghost), [Othello](#othello)  
Optimization: [Travelling Salesman](#salesman), [N-Queens](#nQueens), [Neural Networks](#neuralnetwork)  
Graphics: [Computer Vision](#computervision), [Mandelbrot Set](#mandelbrot), [Raytracing](#raytracing)  
Simulations: [Forest Fire](#forestfire), [Social Links](#sociallinks), [Fireflies](#fireflies)  
Misc: [Closest Points](#closestpoints), [Huffman](#huffman)  
  
## wordladder
Builds a graph with the 6-letter words in words.txt. Words with a one letter difference are neighbors in the graph.  
  
## railroad
Builds a railroad graph from two text files: a location list and an edge list. Romanian cities are used for a simplified problem, while U.S.A. rail stations + major cities are used for the expanded problem.  
The program then traverses it using either A* or Dijkstra's algorithm. A* has a faster runtime than Dijkstra's, but does not fully minimize the path length.  
  
## sudoku
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/sudoku/sudoku.png" width="50%" align="right">  
Uses deductions such as elimination and twin rules to solve sudoku puzzles. <br>
A puzzle is a string of 81 characters, where the '.' character represents an empty space. sudoku128.txt contains 128 puzzles. <br>
<br>
## ghost
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/ghost/ghost.png" width="50%" align="right">  
A game where players take turns spelling out individual letters of a word. The first player to complete a word or a word-less prefix loses.  
The Python script creates an alphabetic trie out of the words in ghost.txt and supports any combination of human and computer players.  
  
## othello
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/othello/othello.png" width="50%" align="right">  
Uses a minimax algorithm that values corners > edges > other squares.  
The script supports player vs. player, player vs. computer, or computer vs. computer.  
It can also read in a board and output an 'optimal' move - **oModerator.py** (written by instructor) takes two such programs and makes them play each other, recording the win/loss results at the end.  
  
## salesman
Travelling Salesman Problem (TSP)  
**Iterative** - randomly generates a path, then "untangles" it, eliminating all intersections between line segments in the path. After untangling, the program makes local optimizations, which minimizes path length in sets of 4-8 adjacent points.  
**Genetic algorithm** - creates a size N population of untangled paths and measures path fitness inversely with path length. Each generation cycle creates N/2 "children paths" by combining two members of the current population. The least fit N/2 members of the new population are then removed from the set.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/salesman/working path.png" width="50%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/salesman/best path.png" width="50%">  
  
## nQueens
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/nqueens/nqueens30.png" width="40%" align="right">
Places N queens on a NxN board such that none of them attack each other. <br>
<b>Brute force backtracking</b> - Generates all possible boards one queen at a time and only works off legal permutations (i.e. will eliminate a "solution" that contains a queen in A1 and another in B2, even if the board size is 8).  Returns a list of all possible boards. Time efficiency is n! due to brute force nature. <br>
<b>Hill climbing</b> - Generates a random board and checks single column swaps to reduce # of conflicts. Sometimes, a solution cannot be found due to the starting spot (we reach a 'local minimum'), in which case we generate a new board and restart. <br>
<b>Genetic algorithm</b> - Similar to the genetic TSP method. Splices parent boards by copying the front of parent 1 (up to a specified pivot point) and appending the rest of the unused numbers in the order they occur in parent 2. This algorithm's time efficiency is far more reliable than the above two methods at large N.<br>
  
## neuralnetwork
WIP    
  
## computervision
**Grayscale**  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/leaves.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/leavesgb.jpg" width="30%">  
  
**Edge detection (Sobel/Canny)**  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/leavesgbe.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/leavesgbet.jpg" width="30%">  
  
**Circle detection (Hough Transform)**  
<nowiki>*</nowiki>brighter spots in the third image have a greater likelyhood of being detected as a circle.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/coins.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/coinse.jpg" width="30%">  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/coinshough.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/coinsfinal.jpg" width="30%">  
  
**Concentric Circle Detection**  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/donuts.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/donutsedge.jpg" width="30%">  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/donutshough.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/donutsfinal.jpg" width="30%">  
  
**Line Detection**  
<nowiki>*</nowiki>the third image plots two variables, rho and theta. Pixel intensity increases with likelyhood of being a line.  
Implementation details can be found <a href= "https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html">here</a>.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/tilted.png" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/tiltede.jpg" width="30%">  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/tiltedhough.jpg" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/computervision/img/tiltedfinal.jpg" width="30%">  
  
## mandelbrot
Plots a shaded Mandelbrot Set using glut and GL.  
Allows the user to zoom in/out indefinitely and increase/decrease calculation precision.  
MPIbrot has identical function, but can use multiple processing cores using mpirun.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/mandelbrot/fewsteps.png" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/mandelbrot/moresteps.png" width="30%">
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/mandelbrot/zoomedin.png" width="30%">  
  
## raytracing
haHAA
  
## forestfire
Simulates a "forest fire" where fire spreads to adjacent cells.  
Uses system time as a seed to generate trees in a grid. Several trials are conducted with varying "tree densities", and the program calculates the density with the longest normalized burnout time (# of iterations until burnout, divided by grid size).  
  
## sociallinks  
The two graphs below are results of a simulation on forming connections.  
Group one starts with a given population and draws random links between everyone. The plot is given by graphrand.jpg.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/sociallinks//graphrand.jpg" width="50%">  
Group two starts with a small number of people (a "popular group") who all know each other. We iteratively add new members to the society and give each new member a few social links. The resulting graph is shown by graphiter.jpg.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/sociallinks//graphiter.jpg" width="50%">  
Note how in graphrand, the graph is shaped more symmetrically, while in graphiter, there are only a few popular people and most people (the new members added later) only have a few connections.  
  
## fireflies
Displays fireflies (yellow dots) on a night (black) background.  
Each firefly builds up charge over time. Upon reaching full charge, it displays a full intensity yellow dot on the screen, which then fades.  
Discharging a light will cause nearby fireflies to also adjust their discharge times to more closely match each other.  
End result is all fireflies discharging and lighting up together.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/fireflies/fireflies.png" width="50%" align="right">
  
## closestpoints
Compares three algorithms for finding the two closest points in a set.  
**Brute force** - O(n^2)  
**Recursive partitioning** - O(nlog(n))  
**Sieve**: O(n), documented in ["A Simple Randomized Sieve Algorithm for the Closest-Pair Problem"](https://www.cs.umd.edu/~samir/grant/cp.pdf)  
  
## huffman
Simple Huffman encoding and decoding. Uses one Amendement from the U.S. Constitution for each of the sample .txt files.  