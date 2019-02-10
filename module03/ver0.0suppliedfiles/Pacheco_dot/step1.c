#include <stdio.h>
#include <mpi.h>

double parallel_dot(double*,double*,long,MPI_Comm);
double parallel_norm2(double*,long,MPI_Comm);

int main(int argc, char* argv[]) {
  long n=atoi(argv[1]),i,l_n,r;
  double x[n],y[n],dp,norm2;
  int id,p;
  double *l_x,*l_y;

  for(i=0;i<n;i++) {
    x[i]=atof(argv[i+2]);
//    y[i]=atof(argv[i+n+2]);
  }

  MPI_Init(&argc,&argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &id);
  MPI_Comm_size(MPI_COMM_WORLD, &p);

  l_n=n/p;
  r=n%p;
  l_x=x+n/p*id;
  l_y=y+n/p*id;
  if(id>=p-r) {
    l_n++;
    l_x+=id+r-p;
    l_y+=id+r-p;
  }
//  dp=parallel_dot(l_x,l_y,l_n,MPI_COMM_WORLD);
//  if(id==0) printf("%lf\n",dp);

  norm2=parallel_norm2(l_x,l_n,MPI_COMM_WORLD);
  if(id==0) printf("%lf\n",norm2);

  MPI_Finalize();
  return 0;
}
