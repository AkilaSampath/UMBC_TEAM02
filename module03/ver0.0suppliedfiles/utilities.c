#include "utilities.h"

/* 09/12/02-10/10/02, updated 02/21/08 and 02/25/09 by Matthias K. Gobbert */

double serial_dot (double *x, double *y, long n)
{
  double dp;
  long i;

  dp = 0.0;

  /* code needed here */

  return dp;
}

double parallel_dot(double *l_x, double *l_y, long l_n, MPI_Comm comm) {

  double l_dot=0.0;
  double dot=0.0;

  l_dot=serial_dot(l_x,l_y,l_n);

  /* code needed here */

  return dot;

}

