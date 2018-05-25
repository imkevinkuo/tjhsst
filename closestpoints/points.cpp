#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <cmath>
#include <fstream>
#include <iostream>
#define M 400

struct Point {
  double x;
  double y;
};
struct Line {
  int j;
  int k; // indices of the points
  double d; // sq distance
};
struct Key {
  int j; // corresponding grid col/row
  int k;
  Key* next;
  int s; // points size
  Key(int init_j, int init_k, Key* init_next) {
		j = init_j;
		k = init_k;
		next = init_next;
		s = 0;
  }
};
void printPoint(Point p) {
  printf("%.23f %.23f\n", p.x, p.y);  
}
void printLine(Line l) {
  printf("%i %i %.10f\n", l.j, l.k, l.d);
}
void printKey(Key* k) {
	printf("(%i %i)", k->j, k->k);
}
double calcSqDist(Point p1, Point p2) {
  double xd = p1.x - p2.x;
  double yd = p1.y - p2.y;
  return xd*xd + yd*yd;
}
double hyp(double xd, double yd) {
	return sqrt(xd*xd + yd*yd);  
}
int comparex(const void *v1, const void *v2) {
	const Point *p1 = (Point *)v1;
	const Point *p2 = (Point *)v2;
	if (p1->x < p2->x)
		return -1;
	else if (p1->x > p2->x)
		return +1;
	else
		return 0;
}
int comparey(const void *v1, const void *v2) {
	const Point *p1 = (Point *)v1;
	const Point *p2 = (Point *)v2;
	if (p1->y < p2->y)
		return -1;
	else if (p1->y > p2->y)
		return +1;
	else
		return 0;
}
Line bruteForce(Point points[], int size) {
	Line l = {0,0,2};
	for (int j = 0; j < size; j++) {
	  for (int k = 0; k < size; k++) {
		if (j != k) {
		  double d = calcSqDist(points[j], points[k]);
		  if (d < l.d) {
			l.j = j;
			l.k = k;
			l.d = d;
		  }
		}
	  }
	}
	return l;
}
Line brutePoint(Point points[], int size, int index) {
	Line l = {index,0,2};
	for (int k = 0; k < size; k++) {
		if (k != index) {
			double d = calcSqDist(points[index], points[k]);
			if (d < l.d) {
			  l.k = k;
			  l.d = d;
			}
		}
    }
	return l;
}
Line recurDist(Point points[], int size, int start, int end) { // inclusive start, exclusive end
	//printf("%i %i\n", start, end);
	Line l = {0,0,2};
	double mindist = 2;
	if (end-start <= 3) {
	  for (int j = start; j < end; j++) {
		for (int k = start; k < end; k++) {
		  if (j != k) {
			double d = calcSqDist(points[j], points[k]);
			if (d < l.d) {
				l.j = j;
				l.k = k;
				l.d = d;
			}
		  }
		}
	  }
	}
	else {
	  int split = (int) ceil((double)(start+end)/2);
	  Line left = recurDist(points, size, start, split);
	  Line right = recurDist(points, size, split, end);
	  double mdist; // MAX from line
	  if (left.d < right.d) {
		mdist = left.d;
		l = left;
      }
      else {
		mdist = right.d;
		l = right;
	  }
	  int start2 = split-1;
	  int end2 = split-1;
	  while (points[end2].x < (points[split-1].x + mdist) && end2 < size) {
		  end2++;
	  }
	  while (points[start2].x > (points[split-1].x - mdist) && start2 > 0) {
		  start2--;
	  }
	  //printf("%i %i\n", start2, end2);
	  for (int j = start2; j < end2; j++) {
		for (int k = start2; k < end2; k++) {
		  if (j != k) {
			double d = calcSqDist(points[j], points[k]);
			if (d < l.d) {
			  l.j = j;
			  l.k = k;
			  l.d = d;
			}
		  }
		}
	  }
	}
	return l;
}
void printKeys(Key* keys[], int size) {
	for (int k=0;k<size;k++) {
	  printf("%i", k);
	  Key* ky = keys[k];
	  while (ky != NULL) {
			printKey(ky);
			ky = ky->next;
	  }
	  printf("\n");
    }
}
// 0 = FALSE , 1 = TRUE
int checkMember(Key* keys[], int size, long long c, int j, int k) {
	int index = (11*j+k)%size;
	Key* ck = keys[index];
	while (ck != NULL) {
	  if (ck->j == j && ck->k == k) {
		return 1;
	  }
    ck = ck->next;
  }
  return 0;
}
// HASH FUNCTION IS HERE
void storeCell(Point p, Key* keys[], int size, double b, long long int c) { // size = # of points, b = cell side len, c = cells on side
  long long j = p.x/b;
  long long k = p.y/b;
  int index = (11*j+k)%size;
  Key* ck = keys[index]; // current key
  if (ck->j == -1 || ck->k == -1) {
	ck->j = j;
	ck->k = k;
	ck->s = 1;
  }
  else {
	while (ck->j != j || ck->k != k) {
		if (ck->next == NULL) {
			ck->next = new Key(j, k, NULL);
		}
		ck = ck->next;
	}
	ck->s += 1;
  }
}
// Finds all occupied cells
// Loops through all points and updates list
void filterKeys(Key* keys[], int size, long long c) {
    for (int k=0;k<size;k++) {
		Key* ky = keys[k];
		Key* prev = NULL;
		while (ky != NULL) {
			int hasNeighbor = 0;
			if (ky->j > -1 && ky->k > -1) {
				if (ky->s > 1) {
					hasNeighbor = 1;
				}
				else {
					for (int dx = -1; dx < 2; dx++) {
						int nx = ky->j + dx;
						for (int dy = -1; dy < 2; dy++) {
							int ny = ky->k + dy;
							if (!(dx == 0 && dy == 0)) {
								if (nx >= 0 && nx < c && ny >= 0 && ny < c) {
									hasNeighbor = checkMember(keys, size, c, nx, ny);
									if (hasNeighbor == 1) {
										goto foundNeighbor;
									}
								}
							}
						}
					}
				}
				foundNeighbor:
					if (hasNeighbor == 0) { // REMOVING KEYS
						if (prev == NULL) {
							if (ky->next == NULL) {
								keys[k] = new Key(-1, -1, NULL);
							}
							else {
								keys[k] = ky->next;
							}
						}
						else {
							prev->next = ky->next;
							ky = prev;
						}
					}
			}
			if (hasNeighbor == 1) {
				prev = ky;
			}
			ky = ky->next;
		}
    }
}
// Start with initial set of points
// Create grid, store map of occupied cells
// Loop through points afterwards to keep/discard
// repeat
Line khullerDist(Point points[], int size) {
	Line l = {0,0,2};
	double f = 1;
	// STORING OLD VARS FOR FINAL LOOP
	int osize = size;
	Point *opoints;
	//////////////////////////////////
	while (size > 0) {
		Line dx = brutePoint(points, size, 0);
		f = sqrt(dx.d);
		double b = f/3; //cell side length
		long long int c = ceil(1.0/b); // cells on one side
		//printf("%llu\n", c);
		//printf("filter mesh: %f %i %i\n", b, c, size);
		Key** keys = new Key*[size];
		for (int i = 0; i < size; i++) {
		  keys[i] = new Key(-1, -1, NULL);
		}
		for (int i = 0; i < size; i++) { // STORE EACH POINT
		  storeCell(points[i], keys, size, b, c);
		}
		// FILTERING POINTS
		//printKeys(keys,size);
		filterKeys(keys, size, c);
		int count = 0;
		for (int i = 0; i < size; i++) { // UPDATE POINTS
			Point p = points[i];
			int j = (int) (p.x/b);
			int k = (int) (p.y/b);
			if (checkMember(keys,size,c,j,k) == 1) {
				points[count] = p;
				count++;
			}
		}
		if (count > 0) {
			opoints = points;
			osize = count;
		}
		size = count;
	}
	// make final mesh with size f
	/*
	int g = (int) ceil(1.0/f);
	//printf("final mesh: %f %i %i\n", f, g, osize);
	Key** fkeys = new Key*[osize];
	for (int i = 0; i < osize; i++) {
		Key* k = new Key(-1, -1, NULL);
		fkeys[i] = k;
	}
	for (int i = 0; i < osize; i++) {
		storeCell(opoints[i], fkeys, osize, f, g);
	}
	filterKeys(fkeys, osize, g);
	int count = 0;
	for (int i = 0; i < osize; i++) { // UPDATE POINTS
		Point p = opoints[i];
		int j = (int) (p.x/f);
		int k = (int) (p.y/f);
		if (checkMember(fkeys,osize,g,j,k) == 1) {
			opoints[count] = p;
			count++;
		}
	}
	osize = count;
	*/
	l = bruteForce(opoints,osize);
	return l;
}
int main(int argc, char * argv[]) {
  printf("%d\n", time(0));
  srand (time(0));
  clock_t tStart = clock();
  // generate points or read in
  /*
  int n = atoi(argv[1]); // number of points
  Point* points = new Point[n];
  for (int i = 0; i < n; i++) {
	Point p;
	p.x = rand() / double(RAND_MAX);
	p.y = rand() / double(RAND_MAX);
	points[i] = p;
  }
  */
  // READ IN FILE
  /*
  int n = 1000000;
  Point* points = new Point[n];
  std::ifstream infile("points1m.dat");
  int count = 0;
  double a, b;
  while (infile >> a >> b) {
	Point p;
	p.x = a;
	p.y = b;
	points[count] = p;
	count++;
  }
  */
  qsort(points, n, sizeof(struct Point), comparex);
  Point p1;
  Point p2;
  // find shortest dist
  //p1 = points[l.j];
  //p2 = points[l.k];
  //Line l = bruteForce(po	ints,n);
  //Line l2 = recurDist(points, n, 0, n);
  Line l = khullerDist(points, n);
  printLine(l);
  clock_t tEnd = clock();
  double time = (double) (tEnd-tStart)/CLOCKS_PER_SEC;
  printf("%.2f\n", time);
  /*
  // DRAWING STUFF
  int y,x;
  int ipoints[M][M] = {{0}};
  for( y = 0 ; y < M; y++ )
  {
     for( x = 0 ; x < M ; x++)
     {
       ipoints[y][x] = 1;
     }
  }
  for (int i = 0; i < n; i++) {
    int x = (int) (points[i].x*M);
    int y = (int) (points[i].y*M);
    ipoints[y][x] = 0;
  }
  // draw line
  double dx = fabs(p2.x - p1.x);
  double dy = fabs(p2.y - p1.y);
  if (dx > dy) {
    int xstart, xend, ystart;
    if (p1.x < p2.x) {
      xstart = (int) (p1.x*M);
      xend = (int) (p2.x*M);
      ystart = (int) (p1.y*M);
    }
    else {
      xstart = (int) (p2.x*M);
      xend = (int) (p1.x*M);
      ystart = (int) (p2.y*M);
    }
    double d = dy/dx;
    double e = d;
    for (x = xstart; x < xend; x++) {
      e = e+d;
      ipoints[ystart][x] = 0;
      if (e > 1) {
	e = e-1;
	ystart = ystart+1;	
      }
    }
  }
  else {
    int ystart, yend, xstart;
    if (p1.y < p2.y) {
      ystart = (int) (p1.y*M);
      yend = (int) (p2.y*M);
      xstart = (int) (p1.x*M);
    }
    else {
      ystart = (int) (p2.y*M);
      yend = (int) (p1.y*M);
      xstart = (int) (p2.x*M);
    }
    double d = dx/dy;
    double e = d;
    for (y = ystart; y < yend; y++) {
      e = e+d;
      ipoints[y][xstart] = 0;
      if (e > 1) {
		e = e-1;
		xstart = xstart+1;	
      }
    }
  }
  // output image
  FILE* fout ;
  fout = fopen( "points.ppm" , "w" ) ;
  fprintf( fout , "P3  " ) ;
  fprintf( fout , "%i  %i  " , M , M) ;
  fprintf( fout , "1\n" ) ;
  for( y = 0 ; y < M; y++ ) {
     for( x = 0 ; x < M ; x++) {
        fprintf(fout, "%i %i %i ", ipoints[y][x], ipoints[y][x], ipoints[y][x]);
     }
     fprintf(fout, "\n");
  }
  fclose( fout );
  */
}
