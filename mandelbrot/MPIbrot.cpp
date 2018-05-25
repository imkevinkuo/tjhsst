//
// to compile type... make
// uses file named... Makefile
//
// a.out: fireGL.c
// 	gcc -lGL -lGLU -lglut fireGL.c
//
// tab character '\t' before gcc
//
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//
#include <GL/gl.h>
#include <GL/glut.h>
//
#define Nx 800
#define Ny 600
#define MAXSTEPS 30
//int MAXSTEPS = 30;
double xmin = -2;
double xmax = 2;
double xcenter = 0;
double ymin = -1.5;
double ymax = 1.5;
double ycenter = 0;
int iterate(double a0, double b0, double c1, double c2) {
  int steps = 0;
  while (steps < MAXSTEPS) {
    steps++;
    double olda = a0;
    double oldb = b0;
    a0 = (olda*olda) - (oldb*oldb) + c1;
    b0 = (2*olda*oldb) + c2;
    if ((a0*a0 + b0*b0) > 4) {
      return steps;
    }
  }
  return steps;
}
void displayfunc()
{
   glClear(GL_COLOR_BUFFER_BIT); // white
   //
   int x,y;
   for( x = 0 ; x < Nx ; x++ )
   {
      for( y = 0 ; y < Ny ; y++ )
      {
	double xsize = xmax - xmin;
	double ysize = ymax - ymin;
	// convert to complex number
	double c1 = (x*xsize/Nx) + xmin;
	double c2 = (y*ysize/Ny) + ymin;
	int steps = iterate(0,0,c1,c2);
	if (steps < MAXSTEPS) {
	  double pc = (double)steps/MAXSTEPS;
	  glColor3f( 0.0 , pc , 0.0 ) ; // scale shade
	}
	else {
	  glColor3f( 1.0 , 1.0 , 1.0 ) ; // white
	}
        glBegin(GL_POINTS);
        glVertex2f(x,y);
        glEnd();
      }
   }
   //
   glutSwapBuffers(); // single buffering... call glFlush();
}
void reshapefunc(int wscr,int hscr)
{
   glViewport(0,0,(GLsizei)Nx,(GLsizei)Ny);
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();
   gluOrtho2D(0.0,1.0*Nx,0.0,1.0*Ny);
   glMatrixMode(GL_MODELVIEW);
}
void mousefunc(int button,int state,int xscr,int yscr)
{
   if(button==GLUT_LEFT_BUTTON)
   {
      if(state==GLUT_DOWN)
      {
	 yscr = Ny-yscr;
         double xsize = xmax - xmin;
         double ysize = ymax - ymin;
         xcenter = (xscr*xsize/Nx) + xmin;
         ycenter = (yscr*ysize/Ny) + ymin;
         // shrink
         xmin = xcenter - xsize/4;
         xmax = xcenter + xsize/4;
         ymin = ycenter - ysize/4;
         ymax = ycenter + ysize/4;
	 //MAXSTEPS = MAXSTEPS+10;
      }
   }
}
void keyfunc(unsigned char key,int xscr,int yscr)
{
   if( key == 'q' )
   {
      exit( 0 ) ;
   }
}
void idlefunc() {
  glutPostRedisplay(); // calls displayfunc
}
int main(int argc,char* argv[])
{
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
   int        k , j  ;
   double     prob , nbt ;
   //
   // boilerplate
   //
   MPI_Init(      &argc          , &argv ) ;
   MPI_Comm_size( MPI_COMM_WORLD , &size ) ; // same
   MPI_Comm_rank( MPI_COMM_WORLD , &rank ) ; // different
   //
   // manager has rank = 0
   //
   if( rank == 0 ) {
      // manager draws stuff
      glutInit(&argc,argv);
      glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
      glutInitWindowSize(Nx,Ny);
      glutInitWindowPosition(100,50);
      glutCreateWindow("");
      glClearColor(1.0,1.0,1.0,0.0);
      glShadeModel(GL_SMOOTH);
      //
      // SEND PIXELS
      // RECV STEPS
      //
      glutIdleFunc(idlefunc);
      glutDisplayFunc(displayfunc);
      glutReshapeFunc(reshapefunc);
      glutMouseFunc(mousefunc);
      glutKeyboardFunc(keyfunc);
      //
      glutMainLoop();
      //
   }
   else {
      MPI_Recv( &prob , 1 , MPI_DOUBLE , 0 , tag , MPI_COMM_WORLD , &status ) ;
      //
      // RECV PIXEL
      // SEND # STEPS
      //
      MPI_Send( &nbt , 1 , MPI_DOUBLE , 0 , tag , MPI_COMM_WORLD ) ;
   }
   //
   // boilerplate
   //
   MPI_Finalize() ;
   //
   }
   return 0;
}
//
// end of file
//
