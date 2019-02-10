#include "Ax.h"

void Ax(double *l_v, double *l_u, long l_n, long l_N, long N,
        int id, int idleft, int idright, int np, MPI_Comm comm,
        double *gl, double *gr) {

  /*long i, l_j;*/
  long l_j;
  double tmp;

  MPI_Status status;

  /* code needed here */

  long i, j;
  for(j = 0; j<N; j++){
    for(i = 0; i<N; i++) {
      tmp = 4.0*l_u[i+N*(j-1)];
      if(j>0  ) tmp = tmp - l_u[i     + N*(j - 1)];
      if(i>0  ) tmp = tmp - l_u[i - 1 + N*(j    )];
      if(i<N-1) tmp = tmp - l_u[i + 1 + N*(j    )];
      if(j<N-1) tmp = tmp - l_u[i     + N*(j + 1)];
      l_v[i+N*j] = tmp;
    }
  }
}
