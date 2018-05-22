# tjhsst
  
Here are several of my high school projects/assignments.  
  
### wordladder
builds a graph with the 6-letter words in words.txt. Words with a one letter difference are neighbors in the graph.  
  
### railroad
builds a railroad graph from two text files: a location list and an edge list. Romanian cities are used for a simplified problem, while U.S.A. rail stations + major cities are used for the expanded problem.  
The program then traverses it using either A* or Dijkstra's algorithm. A* has a faster runtime than Dijkstra's, but does not fully minimize the path length.  
  
### sudoku
uses deductions such as elimination and twin rules to solve sudoku puzzles.  
A puzzle is a string of 81 characters, where the '.' character represents an empty space. sudoku128.txt contains 128 puzzles.  
  
### ghost
is a game where players take turns spelling out individual letters of a word.  
The first player to complete a word or a word-less prefix loses.  
The Python script creates an alphabetic trie out of the words in ghost.txt to support an AI player.  
Supports any combination of human and computer players.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/ghost/ghost.png" width="50%">  
  
### othello  
uses a minimax algorithm that values corners > edges > other squares.  
The script supports player vs. player, player vs. computer, or computer vs. computer.  
It can also read in a board and output an 'optimal' move - **oModerator.py** (written by instructor) takes two such programs and makes them play each other, recording the win/loss results at the end.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/othello/othello.png" width="50%">  
  
### salesman
the Travelling Salesman Problem.
  
**Iterative** - randomly generates a path, then "untangles" it, eliminating all intersections between line segments in the path. After untangling, the program makes local optimizations, which minimizes path length in sets of 4-8 adjacent points.  

**Genetic algorithm** - creates a size N population of untangled paths and measures path fitness inversely with path length. Each generation cycle creates N/2 "children paths" by combining two members of the current population. The least fit N/2 members of the new population are then removed from the set.  

Example of path mid-untangling:  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/optimization//working path.png" width="50%">  
Untangled path:  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/optimization//best path.png" width="50%">  
  
### nQueens
draws an N-by-N square board with N queens, such that none of them attack each other.  

**Brute force backtracking** - Generates all possible boards one queen at a time and only works off legal permutations (i.e. will eliminate a "solution" that contains a queen in A1 and another in B2, even if the board size is 8).  Returns a list of all possible boards. Time efficiency is n! due to brute force nature.  
**Hill climbing** - Generates a random board and checks single column swaps to reduce # of conflicts. Sometimes, a solution cannot be found due to the starting spot (we reach a 'local minimum'), in which case we generate a new board and restart.
**Genetic algorithm** - Similar to the genetic TSP method. Splices parent boards by copying the front of parent 1 (up to a specified pivot point) and appending the rest of the unused numbers in the order they occur in parent 2. This algorithm's time efficiency is far more reliable than the above two methods at large N.
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/optimization/nqueens30.PNG" width="50%">  
  
### sociallinks
analyzes two different social groups:  

Each graph is a distribution of people based on # of social connections. 
Group one starts with a given population and draws random links between everyone. The plot is given by graphrand.jpg.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/sociallinks//graphrand.jpg" width="50%">  
Group two starts with a small number of people (a "popular group") who all know each other. We iteratively add new members to the society and give each new member a few social links. The resulting graph is shown by graphiter.jpg.  
<img src="https://raw.githubusercontent.com/imkevinkuo/tjhsst/master/sociallinks//graphiter.jpg" width="50%">  
Note how in graphrand, the graph is shaped more symmetrically, while in graphiter, there are only a few popular people and most people (the new members added later) only have a few connections.
  