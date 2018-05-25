//
// Kevin Kuo
//
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
//
typedef struct Node
{
	char symbol ;
	//
	int frequency ;
	//
	struct Node* left ;
	struct Node* right ;
	//
} TreeNode ;
void printNode(TreeNode* node) {
	printf("%c", node -> symbol);
	printf("%s", " freq: ");
	printf("%i", node -> frequency);
	printf("\n");
}
void generateCodes(TreeNode* node, char pcode[], char* codes[], FILE *scheme) {
	if (node -> symbol == '*') {
		char lcode[20] = {'\0'};
		char rcode[20] = {'\0'};
		strcat(lcode, pcode);
		strcat(rcode, pcode);
		for (int i = 0; i < 20; i++) {
			if (pcode[i] == '\0') {
				lcode[i] = '0';
				rcode[i] = '1';
				break;
			}
		}
		generateCodes(node -> left, lcode, codes, scheme);
		generateCodes(node -> right, rcode, codes, scheme);
	}
	else {
		char *fp;
		fp = (char*)malloc(21 * sizeof(char));
		strcpy(fp, pcode);
		fprintf(scheme, "%c%s\n", node -> symbol, pcode);
		// STORE IN CODES
		codes[(int) node -> symbol] = fp;
	}
}
float calcShannon(int freq[], int z) {
	float shn = 0;
	for (int i = 0; i < 256; i++) {
		if (freq[i] > 0) {
			float prob =  (float) freq[i]/z;
			float a = -log(prob)*freq[i]/log(2);
			shn += a;
		}
	}
	return shn;
}
int encode(char* name) { // return msg len
	char dec[60];
	strcpy(dec, "Parallel\\Huffman\\decoded.");
	strcat(dec, name);
	strcat(dec, ".txt");
	char mes[60];
	strcpy(mes, "Parallel\\Huffman\\message.");
	strcat(mes, name);
	strcat(mes, ".txt");
	char sch[60];
	strcpy(sch, "Parallel\\Huffman\\scheme.");
	strcat(sch, name);
	strcat(sch, ".txt");
	// READ IN THE UNCOMPRESSED MESSAGE
	FILE* decoded = fopen(dec, "r" );
	char msg[12000] = {'\0'};
	int n = 0; // # of codewords /unique chars
	int z = 0; // # of characters /message size
	int numbytes;
	char ch;
	int freq[256] = {0};
	while(1) {
		numbytes = fread( &ch , sizeof(char) , 1 , decoded);
		if (numbytes == 0) {
			break;
		}
		msg[z] = ch;
		if (freq[(int)ch] == 0) {
			n++;
		}
		freq[(int)ch]++;
		z++;
	}
	TreeNode* nodes[n];
	int sum = 0;
	int p = 0; //position
	for (int a = 0; a < 256; a++) {
		if (freq[a] > 0) {
			TreeNode* t = NULL ;
			//
			t = (TreeNode*)malloc( sizeof(TreeNode));
			//
			(*t).symbol = (char) a;
			t -> frequency = freq[a];
			t -> left = NULL;
			t -> right = NULL;
			nodes[p] = t;
			p++;
		}
	}
	//
	// TAKE SMALLEST TWO FREQUENCIES AND MAKE A PARENT OF THOSE TWO LEAVES SUMMED
	// LOOP UNTIL NO MORE FREQUENCIES
	//
	int pindex = 0;
	for (int a = 1; a < n; a++) { // a is not used
		// Find smallest nodes
		TreeNode* l = NULL;
		TreeNode* r = NULL;
		int x;
		for (x = 0; x < n; x++) {
			if (nodes[x] != NULL) {
				if (l == NULL) {
					l = nodes[x];
				}
				else if (r == NULL) {
					r = nodes[x];
				}
				else if (nodes[x] -> frequency < l -> frequency) {
					l = r;
					r = nodes[x];
				}
				else if (nodes[x] -> frequency < r -> frequency) {
					r = l;
					l = nodes[x];
				}
			}
		}
		TreeNode* parent = (TreeNode*)malloc( sizeof(TreeNode));
		parent -> symbol = '*';
		parent -> frequency = l -> frequency + r -> frequency;
		parent -> left = l;
		parent -> right = r;
		// loop through to replace and remove
		for (x = 0; x < n; x++) {
			if (nodes[x] == r) {
				nodes[x] = NULL;
			}
			if (nodes[x] == l) {
				nodes[x] = parent;
				pindex = x;
			}
		}
		//printNode(parent);
	}
	// GENERATE CODES
	FILE *scheme = fopen(sch, "w+");
	if (scheme == NULL) {
		printf("Error opening file!\n");
		exit(1);
	}
	fprintf(scheme, "%i\n", n);
	//
	char code[20] = {'\0'};
	char *codes[256];
	for (int c = 0; c < 256; c++) {
		codes[c] = NULL;
	}
	//
	generateCodes(nodes[pindex], code, codes, scheme);
	// WRITE MESSAGE
	FILE *message = fopen(mes, "w");
	if (message == NULL) {
		printf("Error opening file!\n");
		exit(1);
	}
	int m = 0;
	int hlen = 0;
	while (msg[m] != '\0') {
		char* cw = codes[(int)msg[m]];
		fprintf(message, "%s", cw);
		hlen += strlen(cw);
		m++;
	}
	// CALCULATE SHANNON
	//
	float s = calcShannon(freq, z);
	printf("%s", name);
	printf(" |");
	printf("%i", (int) s);
	if ((int)s < 1000) {
		printf("%s", " ");
	}
	if ((int)s < 10000) {
		printf("%s", " ");
	}
	printf("|");
	printf("%f", 1 - (float)s/(z*8));
	printf("|");
	printf("%f", 1 - (float)hlen/(z*8));
	printf("|");
	printf("%i", z);
	printf("\n");
	//
	fclose(scheme);
	fclose(decoded);
	fclose(message);
	return z;
}
//
int main(int argc , char* argv[] )
{
	printf("%s\n", "Name|SMin |SCR     |HCR     |z"); // name, shannon min, shannon ratio, huffman ratio, message len
	char* name;
	if (argc == 2) {
		name = argv[1];
		encode(name);
	}
	if (argc == 1) {
		int highz = 0;
		for (int fz = 1; fz < 28; fz++) {
			char name[20];
			strcpy(name, "a");
			if (fz < 10) {
				strcat(name, "0");
			}
			char buffer[3];
			strcat(name, itoa(fz,buffer,10));
			int z = encode(name);
			if (z > highz) {
				highz = z;
			}
		}
		printf("%i\n", highz);
	}
	return 0;
}
//
// end of file
//
