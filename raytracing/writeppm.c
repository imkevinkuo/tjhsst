/*
* Shell code by Shane Torbert, 8 February 2016
* Kevin Kuo, 4 April 2018
*/
#include <stdio.h>
#include "initRay.c"

#define M 640
#define N 480
#define S 4
#define D 0.5

sphere a[S];
triple e = { 0.50 , 0.50 , -1.00 } ; // the eye
triple s = { 0.00 , 0.00 ,  1.00 } ; // the sight
triple g = { 0.00 , 1.25 , -0.50 } ; // the light


/*
*  Initiates all the scene objects, stored in array a.
*/
void init() {
   a[0].c.x =      0.50 ;
   a[0].c.y = -20000.00 ; // the floor
   a[0].c.z =      0.50 ;
   a[0].r   =  20000.25 ;
   a[0].h.r =    205    ; // color is Peru
   a[0].h.g =    133    ;
   a[0].h.b =     63    ;
   //
   a[1].c.x =      0.50 ;
   a[1].c.y =      0.50 ;
   a[1].c.z =      0.50 ;
   a[1].r   =      0.25 ;
   a[1].h.r =      0    ; // color is Blue
   a[1].h.g =      0    ;
   a[1].h.b =    255    ;
   //
   a[2].c.x =      1.00 ;
   a[2].c.y =      0.50 ;
   a[2].c.z =      1.00 ;
   a[2].r   =      0.25 ;
   a[2].h.r =      0    ; // color is Green
   a[2].h.g =    255    ;
   a[2].h.b =      0    ;
   //
   a[3].c.x =      0.00 ;
   a[3].c.y =      0.75 ;
   a[3].c.z =      1.25 ;
   a[3].r   =      0.50 ;
   a[3].h.r =    255    ; // color is Red
   a[3].h.g =      0    ;
   a[3].h.b =      0    ;
}

/*
*  Colors the entire .ppm file green.
*/
void green(int rgb[N][M][3], int x, int y) {
   rgb[y][x][0] = 0   ; // red
   rgb[y][x][1] = 255 ; // green
   rgb[y][x][2] = 0   ; // blue
}

/*
*  Projects a ray from the surface of a sphere towards the light source(s).
*  If any object blocks the ray, the corresponding pixel is darkened.
*/
int binary_shade(triple loc_contact) {
   int i;
   double dist_adj, dist_center;
   triple dir_light, dir_center;
   dir_light = diff(g, loc_contact);
   for (i = 0; i < S; i++) {
      dir_center = diff(a[i].c, loc_contact);
      dist_adj = dotp(dir_light, dir_center) / sqrt(mag_sqr(dir_light));
      if (dist_adj > 0) { // no looking backwards
         dist_center = sqrt(mag_sqr(dir_center) - dist_adj*dist_adj);
         if (dist_center < a[i].r) { // if ray is inside sphere
            return D; // shade = BLACK
         }
      }
   }
   return 1;
}

/*
*  If a point is not in shade (as defined by binary_shade), we still darken it
*  depending on its degree of exposure to the light source.
*
*  Pixel intensity is inversely proportional to the angle between
*  the surface normal and the surface->light source ray.
*  E.g. angle of 0 means maximum possible exposure.
*/
double gradient_shade(triple loc_contact, int min_i) {
   triple dir_normal, dir_light;
   double dotprod;
   if (binary_shade(loc_contact) == 0) return D;
   dir_normal = diff(loc_contact, a[min_i].c);
   dir_light = diff(g, loc_contact);
   dotprod = dotp(dir_normal, dir_light)
    / (sqrt(mag_sqr(dir_normal))*sqrt(mag_sqr(dir_light)));
    /* range of cos(theta): -1 to 1, normalize-> 0 to 1 */
   return (1 + dotprod)/2;
}

/*
*  Treats the floor as a flat surface and checkers the region based on x and z.
*/
int checkered_floor(triple loc_contact) {

}

/*
*  Main function that traces rays from the eye to objects in the scene.
*  Finds the first object each ray collides with and colors the
*  corresponding pixel accordingly, then calls shading function.
*/
void ray00(int rgb[N][M][3], int x, int y, triple c) {
   int i, min_i = -1;
   double min_dist = -1, dist_adj, dist_center, dist_inner, dist_contact, shade;
   triple dir_pixel, dir_center, loc_contact;

   /*
   *  min_i: index of sphere w/contact
   *  **distances**
   *  min_dist: distance from eye to closest sphere along ray
   *  dist_adj: distance from pixel until perp. to sphere center
   *  dist_center: perpendicular distance from ray to sphere center
   *  dist_inner: distance from dist_adj endpoint to dist_contact endpoint
   *  dist_contact: distance from eye to contact with sphere
   *
   *  **vectors/coordinates**
   *  dir_pixel: vector from eye through dir_pixel
   *  dir_center: vector from eye through sphere center
   *  loc_contact: location of contact with sphere
   */

   dir_pixel = diff(c, e);
   for (i = 0; i < S; i++) {
      dir_center = diff(a[i].c, e);
      dist_adj = dotp(dir_pixel, dir_center) / sqrt(mag_sqr(dir_pixel));
      if (dist_adj > 0) { // no looking backwards
         dist_center = sqrt(mag_sqr(dir_center) - dist_adj*dist_adj);
         if (dist_center <= a[i].r) { // if ray is inside sphere
            dist_inner = sqrt(a[i].r*a[i].r - dist_center*dist_center);
            dist_contact = dist_adj - dist_inner;
            if (min_dist == -1 || dist_contact < min_dist) {
               min_dist = dist_contact;
               min_i = i;
            }
         }
      }
   }
   shade = 0; // defaults to black if no object is hit
   if (min_i > -1) { // ray hits an object
      loc_contact = sum(e, multiply(normalize(dir_pixel), min_dist));
      shade = gradient_shade(loc_contact, min_i);
   }
   rgb[y][x][0] = a[min_i].h.r*shade;
   rgb[y][x][1] = a[min_i].h.g*shade;
   rgb[y][x][2] = a[min_i].h.b*shade;
}

void write(FILE* fout, int rgb[N][M][3], char* name) {
   int x, y;
   //
   fout = fopen( name , "w" );
   //
   fprintf( fout , "P3\n" ) ;
   fprintf( fout , "%d %d\n" , M , N ) ;
   fprintf( fout , "255\n" ) ;
   //
   for (y = 0; y < N; y++) {
      for (x = 0; x < M; x++) {
         fprintf(fout, "%d %d %d\n", rgb[N-y-1][x][0], rgb[N-y-1][x][1], rgb[N-y-1][x][2]);
      }
   }
   //
   fclose(fout);
}
//
int main(void) {
   init();
   int x, y;
   int rgb[N][M][3] ; // red-green-blue for each pixel
   FILE* fout ;
   // how are we gonna rotate screen
   for (y = 0; y < N; y++) {
      for (x = 0; x < M; x++) {
         triple loc_frame_center = sum(e, s);
         double true_x = (double) (x-M/2)*1.33 / M;
         double true_y = (double) (y-N/2) / N;
         triple true_c = {true_x, true_y, e.z};
         triple true_d = sum(loc_frame_center, true_c);
         ray00(rgb, x, y, true_d);
      }
   }
   write(fout, rgb, "ray00.ppm");
   return 0;
}
//
// end of file
//
