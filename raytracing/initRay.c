//
// Torbert, March 2015
//
#include <math.h>
typedef struct {
   double x;
   double y;
   double z;
} triple;
typedef struct {
   int r;
   int g;
   int b;
} color;
typedef struct {
   triple c; // center
   color h; // color
   double r; // radius
} sphere;
//
double dotp(triple u, triple v) {
   return u.x * v.x + u.y * v.y + u.z * v.z;
}
double mag_sqr(triple t) {
   return dotp(t, t);
}
triple multiply(triple t, double s) {
   triple u;
   u.x = t.x * s;
   u.y = t.y * s;
   u.z = t.z * s;
   return u;
}
triple normalize(triple t) {
   triple u;
   double mag = sqrt(mag_sqr(t));
   u.x = t.x / mag;
   u.y = t.y / mag;
   u.z = t.z / mag;
   return u;
}
triple diff(triple u, triple v) { // t = u - v
   triple t;
   t.x = u.x - v.x;
   t.y = u.y - v.y;
   t.z = u.z - v.z;
   return t;
}
triple sum(triple u, triple v) {
   triple t;
   t.x = u.x + v.x;
   t.y = u.y + v.y;
   t.z = u.z + v.z;
   return t;
}
//
// end of file
//
