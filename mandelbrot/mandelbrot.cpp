//
// Kevin Kuo, 1/23, P5
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//
#include <GL/gl.h>
#include <GL/glut.h>
//
#define Nx 800
#define Ny 600
int MAXSTEPS = 30;
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
   yscr = Ny-yscr;
   double xsize = xmax - xmin;
   double ysize = ymax - ymin;
   if(button==GLUT_LEFT_BUTTON)
   {
      if(state==GLUT_DOWN)
      {
         xcenter = (xscr*xsize/Nx) + xmin;
         ycenter = (yscr*ysize/Ny) + ymin;
         // shrink
         xmin = xcenter - xsize/4;
         xmax = xcenter + xsize/4;
         ymin = ycenter - ysize/4;
         ymax = ycenter + ysize/4;
      }
   }
   if(button==GLUT_RIGHT_BUTTON)
   {
      if(state==GLUT_UP)
      {
         xcenter = (xscr*xsize/Nx) + xmin;
         ycenter = (yscr*ysize/Ny) + ymin;
         // shrink
         xmin = xcenter - xsize;
         xmax = xcenter + xsize;
         ymin = ycenter - ysize;
         ymax = ycenter + ysize;
      }
   }
}
void keyfunc(unsigned char key,int xscr,int yscr)
{
   if( key == 'q' ) {
      exit( 0 ) ;
   }
   if(key == 'w') {
      MAXSTEPS++;
   }
   if(key == 's') {
      MAXSTEPS--;
  }
}
void idlefunc() {
  glutPostRedisplay(); // calls displayfunc
}
int main(int argc,char* argv[])
{
   glutInit(&argc,argv);
   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
   glutInitWindowSize(Nx,Ny);
   glutInitWindowPosition(100,50);
   glutCreateWindow("");
   glClearColor(1.0,1.0,1.0,0.0);
   glShadeModel(GL_SMOOTH);
   //
   glutIdleFunc(idlefunc);
   glutDisplayFunc(displayfunc);
   glutReshapeFunc(reshapefunc);
   glutMouseFunc(mousefunc);
   glutKeyboardFunc(keyfunc);
   //
   glutMainLoop();
   //
   return 0;
}
//
// end of file
//
