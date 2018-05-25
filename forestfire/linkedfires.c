//
// Kevin Kuo, 12/12/2016, Torbert Pd 5
//
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//
#define W 40
#define H 30
#define T 100

typedef struct Node {
    int x;
    int y;
	int len; // only accurate for the head node
	struct Node* next;
} ListNode;

double myrand()
{
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
void printNode(ListNode* node) {
	printf("%i \n", node -> len);
	/*
	printf("%i %i\n", node -> x, node -> y);
	if (node -> next != NULL) {
		printNode(node -> next);
	}
	*/
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
int runTrials() {
	double peakprob = 0;
 	float peaknbt = 0;
	double prob = 0.5;
	while (prob < 0.75) {
		prob += 0.05;
		int steptotal = 0;
		for (int t = 0; t < T; t++) {
			steptotal += runTrial(prob);
		}
		float nbt = (float)steptotal/(T*W); // normalized burnout time;
		if (nbt > peaknbt) {
			peaknbt = nbt;
			peakprob = prob;
		}
	}
	printf("%i %f %f\n", W*H, peakprob, peaknbt);
	return peaknbt;
}

int main(int argc, char **argv) {
	int rseed;
	if (argc <= 1) {
		rseed = time(NULL);
	}
	else {
		rseed = atoi(argv[1]);
	}
	printf("%i\n", rseed);
	srand(rseed);
	//
	int peaknbt = runTrials();
	return 0;
}