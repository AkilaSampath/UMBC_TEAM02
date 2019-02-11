#include "Ax.h"
#include <stdio.h>

void Ax(double *l_v, double *l_u, long l_n, long l_N, long N,
        int id, int idleft, int idright, int np, MPI_Comm comm,
        double *gl, double *gr) {

  long i, l_j;
  double tmp;
  MPI_Status statuses[4];
  MPI_Request requests[4];

  /* code needed here */
  if(np>1) {
    MPI_Irecv(gl,           N,MPI_DOUBLE,idleft, 1,MPI_COMM_WORLD,requests);
    MPI_Irecv(gr,           N,MPI_DOUBLE,idright,2,MPI_COMM_WORLD,requests+1);
    MPI_Isend(l_u+N*(l_N-1),N,MPI_DOUBLE,idright,1,MPI_COMM_WORLD,requests+2);
    MPI_Isend(l_u,          N,MPI_DOUBLE,idleft, 2,MPI_COMM_WORLD,requests+3);
  }

  for(l_j=1;l_j<l_N-1;l_j++) {
    for(i=0;i<N;i++) {
      tmp = 4.0*l_u[i+N*l_j] - l_u[i+N*(l_j-1)] - l_u[i+N*(l_j+1)];
      if(i>0)  tmp -= l_u[i-1+N*l_j];
      if(i<N-1)  tmp -= l_u[i+1+N*l_j];
      l_v[i+N*l_j] = tmp;
    }
  }

  if(np>1)
    MPI_Waitall(4,requests,statuses);

  if(l_N==1) {
    l_j=0;
    for(i=0;i<N;i++) {
      tmp = 4.0*l_u[i+N*l_j];
      if(id>0)   tmp -= gl[i];
      if(id<np)  tmp -= gr[i];
      if(i>0)    tmp -= l_u[i-1+N*l_j];
      if(i<N-1)  tmp -= l_u[i+1+N*l_j];
      l_v[i+N*l_j] = tmp;
    }
  }
  else {
    l_j=0;
    for(i=0;i<N;i++) {
      tmp = 4.0*l_u[i+N*l_j] - l_u[i+N*(l_j+1)];
      if(id>0)   tmp -= gl[i];
      if(i>0)    tmp -= l_u[i-1+N*l_j];
      if(i<N-1)  tmp -= l_u[i+1+N*l_j];
      l_v[i+N*l_j] = tmp;
    }

    l_j=l_N-1;
    for(i=0;i<N;i++) {
      tmp = 4.0*l_u[i+N*l_j] - l_u[i+N*(l_j-1)];
      if(id<np-1)  tmp -= gr[i];
      if(i>0)    tmp -= l_u[i-1+N*l_j];
      if(i<N-1)  tmp -= l_u[i+1+N*l_j];
      l_v[i+N*l_j] = tmp;
    }
  }
//  printf("Process %d: %x %2.0lf %x %2.0lf\n",id,l_v,l_v[0],l_v+l_n-1,l_v[l_n-1]);
}
