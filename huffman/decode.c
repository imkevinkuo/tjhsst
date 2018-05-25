//
// Kevin Kuo
//
#include <stdio.h>
#include <math.h>
//
int main() {
	// INPUT
	char name[20];
	printf("Enter file name in folder txtfiles (include .txt): ");
  	scanf("%s", name);
	char dec[60];
	strcpy(dec, "decoded.");
	strcat(dec, name);
	// Just a single file for both scheme and message
	char sch[60];
	strcpy(sch, "txtfiles\\");
	strcat(sch, name);
	//
	// READ SCHEME
    //
	FILE* scheme = fopen(sch, "r" );
    char ch;
    int n = 0;
    int numbytes;
    int codes[10];
    // READ NUMBER OF CODE WORDS
    while(1) {
		numbytes = fread( &ch , sizeof(char) , 1 , scheme );
		if (numbytes == 0 || ch == '\n') break;
		codes[n] = ch - '0';
		n++ ;
    }
    int a;
    int lines = 0;
    for (a = 0; a < n; a++) {
		lines += codes[a] * pow(10, (n - a) - 1);
    }
    //
    // READ CODE WORDS
    //
    int l;
    char tree[10000] = {'\0'};
    for (l = 0; l < lines; l++) {
		n = 0;
		char line[24] = {'\0'};
		while(1) {
			numbytes = fread( &ch , sizeof(char) , 1 , scheme );
			//
			if (numbytes == 0 || (n > 1 && ch == '\n')) break;
			//
			line[n] = ch;
			n++;
		}
		int count = 1;
		int index = 1;
		while (line[count] != '\0') {
			if (line[count] == '0') {
				index = (index * 2);
			}
			if (line[count] == '1') {
				index = (index * 2) + 1;
			}
			count++;
		}
		tree[index] = line[0];
    }
	//
	// READ MESSAGE
	//
	char msg[12000] = {'\0'};
	char rawmsg[4000] = {'\0'};
	n = 0;
	while(1) {
		numbytes = fread( &ch , sizeof(char) , 1 , scheme);
		if (numbytes == 0 || ch == '\n') break;
		msg[n] = ch;
		n++ ;
    }
    close( scheme );
    //
	// WRITE DECODED MESSAGE
	//
	FILE *decoded = fopen(dec, "w");
	int index = 1;
	int count = 0;
	int dcount = 0;
	while (msg[count] != '\0') {
		if (msg[count] == '0') {
			index = (index * 2);
		}
		if (msg[count] == '1') {
			index = (index * 2) + 1;
		}
		if (tree[index] != '\0') {
			rawmsg[dcount] = tree[index];
			dcount++;
			index = 1;
		}
		count++;
	}
	int c2 = 0;
	while (rawmsg[c2] != '\0') {
		printf("%c", rawmsg[c2]);
		fprintf(decoded, "%c", rawmsg[c2]);
		c2++;
	}
	close(decoded);
}
//
// end of file
//
