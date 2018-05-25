// 
// Kevin Kuo, 12/12/2016
//
// mpicc mpiDemo.c -std=c99
// time mpirun -np 4 a.out
// time mpirun -np 6 -machinefile hosts.txt a.out
// 
// work on main method

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include "mpi.h"

#define W 240
#define H 180

typedef struct Node {
    int x;
    int y;
	int len; // only accurate for the head node
	struct Node* next;
} ListNode;

double gettime() {
	double t ;
	struct timeval* ptr = (struct timeval*)malloc( sizeof(struct timeval) ) ;
	gettimeofday( ptr , NULL ) ; // second argument is time zone... NULL
	t = ptr->tv_sec * 1000000.0 + ptr->tv_usec ;
	free(ptr);
	return t / 1000000.0 ;
}
double myrand() {
	return ( rand() % 100 ) / 100.0 ;
}

void printGrid(char grid[][W]) {
	for (int h = 0; h < H; h++) {
		for (int w = 0; w < W; w++) {
			printf("%c ", grid[h][w]);
		}
		printf("\n");
	}
	printf("\n");
}
void addNode(ListNode* head, int w, int h) {
	// sets values on the head node if it is undefined
	if (head -> len == 0) {
		head -> x = w;
		head -> y = h;
		head -> next = NULL;
	}
	// otherwise appends a node
	else {
		ListNode* nfire = malloc(sizeof(ListNode));
		nfire -> x = w;
		nfire -> y = h;
		nfire -> next = NULL;
		// iterate to end
		ListNode* ifire = head;
		while (ifire -> next != NULL) {
			ifire = ifire -> next;
		}
		ifire -> next = nfire;
	}
	head -> len += 1;
}
ListNode* spreadFire(char grid[][W], ListNode* fire) {
	ListNode* ffire = malloc(sizeof(ListNode));
	ffire -> len = 0;
	while (fire != NULL) {
		int w = fire -> x;
		int h = fire -> y;
		grid[h][w] = '-';
		if (h > 0) {
			if (grid[h-1][w] == 'T') { 
				grid[h-1][w] = '*';
				addNode(ffire,w,h-1);
			}
		}
		if (w > 0) {
			if (grid[h][w-1] == 'T') { 
				grid[h][w-1] = '*';
				addNode(ffire,w-1,h);
			}
		}
		if (h < (H-1)) {
			if (grid[h+1][w] == 'T') { 
				grid[h+1][w] = '*';
				addNode(ffire,w,h+1);
			}
		}
		if (w < (W-1)) {
			if (grid[h][w+1] == 'T') { 
				grid[h][w+1] = '*';
				addNode(ffire,w+1,h);
			}
		}
		fire = fire -> next;
	}
	return ffire;
}
int runTrial(double prob) {
	int steps = 0;
	int fires = 0;
	char grid[H][W];
	for (int h = 0; h < H; h++) {
		for (int w = 0; w < W; w++) {
			if (myrand() < prob) {
				grid[h][w] = 'T';
			}
			else {
				grid[h][w] = '-';
			}
		}
	}
	ListNode* ffire = malloc(sizeof(ListNode));
	ffire -> len = 0;
	for (int h = 0; h < H; h++) {
		if (grid[h][0] == 'T') {
			grid[h][0] = '*';
			addNode(ffire,0,h);
		}
	}
	while (ffire -> len > 0) {
		steps += 1;
		ffire = spreadFire(grid, ffire);
	}
	return steps;
}
double runTrials(double prob, int T) { // T = # of trials
	int steptotal = 0;
	for (int t = 0; t < T; t++) {
		steptotal += runTrial(prob);
	}
	double nbt = (double)steptotal/(T*W); // normalized burnout time;
	return nbt;
}

int main (int argc , char* argv[] ) {
	//
	// MPI variables
	//
	int        rank    ;
	int        size    ;
	MPI_Status status  ;
	int        tag = 0 ;
	//
	// other variables
	//
	int        k, j, rseed;
	double     prob, s[2];
	MPI_Init(      &argc          , &argv ) ;
	MPI_Comm_size( MPI_COMM_WORLD , &size ) ; // same
	MPI_Comm_rank( MPI_COMM_WORLD , &rank ) ; // different
	if (rank == 0 ) { // MANAGER
		printf("\n");
		double tic, toc;
		tic = gettime();
		// Generating and sending seed
		rseed = time(NULL);
		printf("%s %i\n", "Seed: ", rseed);
		for (j = 1 ; j < size ; j++ ) {
			MPI_Send( &rseed , 1 , MPI_INT , j , tag , MPI_COMM_WORLD ) ;
		}
		// Programs will define the probabilities themselves, based on rank
		for (k = 1 ; k < size ; k++ ) {
			MPI_Recv( &s , 2 , MPI_DOUBLE , MPI_ANY_SOURCE , tag , MPI_COMM_WORLD , &status ) ;
			j = status.MPI_SOURCE ;
			printf( "%d %d %f %f\n" , j , size , s[0], s[1] ) ;
		}
		toc = gettime();
		printf( "%f\n", toc-tic);
	}
	else { // WORKER
		int T = 200;
		MPI_Recv( &rseed , 1 , MPI_INT , 0 , tag , MPI_COMM_WORLD , &status );
		srand(rseed+j); // unique seed for each worker
		double peakprob = 0.5;
		double peaknbt = 0;
		for (int i = 0; i < 25; i++) {
			if ((i%(size-1) + 1) == rank) {
				prob = 0.01*i + 0.5;
				double nbt = runTrials(prob, T);
				if (nbt > peaknbt) {
					peaknbt = nbt;
					peakprob = prob;
				}
			}
		}
		double s[2] = {0};
		s[0] = peakprob;
		s[1] = peaknbt;
		//printf("%f %f\n", s[0], s[1]);
		MPI_Send( &s , 2 , MPI_DOUBLE , 0 , tag , MPI_COMM_WORLD ) ;
	}
	MPI_Finalize() ;
	//
	return 0;
}