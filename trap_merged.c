/* trap.c -- Parallel Trapezoidal Rule, first version
 *
 * Input: None.
 * Output:  Estimate of the integral from a to b of f(x)
 *    using the trapezoidal rule and n trapezoids.
 *
 * Algorithm:
 *    1.  Each process calculates "its" interval of
 *        integration.
 *    2.  Each process estimates the integral of f(x)
 *        over its interval using the trapezoidal rule.
 *    3a. Each process != 0 sends its integral to 0.
 *    3b. Process 0 sums the calculations received from
 *        the individual processes and prints the result.
 *
 * Notes:  
 *    1.  f(x), a, b, and n are all hardwired.
 *    2.  The number of processes (p) should evenly divide
 *        the number of trapezoids (n = 1024)
 *
 * See Chap. 4, pp. 56 & ff. in PPMPI.
 */
#include <stdio.h>
#include <math.h>
/* We'll be using MPI routines, definitions, etc. */
#include "mpi.h"

/* Define bool type */
typedef int bool;
enum { false, true };

main(int argc, char** argv) {
    int         my_rank;   /* My process rank           */
    int         p;         /* The number of processes   */
    float       a = 0.0;   /* Left endpoint             */
    float       b = 1.0;   /* Right endpoint            */
    int         n = 1024;  /* Number of trapezoids      */
    float       h;         /* Trapezoid base length     */
    float       local_a;   /* Left endpoint my process  */
    float       local_b;   /* Right endpoint my process */
    int         local_n;   /* Number of trapezoids for  */
                           /* my calculation            */
//mengxi
    int         residual;  /* to be described           */
    bool        if_sin = false;
    float       true_value;
//mengxi
    float       integral;  /* Integral over my interval */
    float       total;     /* Total integral            */
    int         source;    /* Process sending integral  */
    int         dest = 0;  /* All messages go to 0      */
    int         tag = 0;
    MPI_Status  status;

    /* Change to False for main runs, True will give more information. */
    bool verbose = true;

    float Trap(float local_a, float local_b, int local_n,
              float h, bool if_sin);    /* Calculate local integral  */

    /* Let the system do what it needs to start up MPI */
    MPI_Init(&argc, &argv);

    /* Get my process rank */
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    /* Find out how many processes are being used */
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    int        global_n[p];
    float      global_a[p];
    float      global_b[p];

    /*Process command line arguments */
    if(my_rank==0) {
        if((argc==2 || argc==5) && argv[1][0]=='s') { /* Use pi*sin(pi*x) */
        if_sin = true;
        }
        if(argc>3)
        {
            if(verbose) printf("Command Line Arguments:\n");
            a = atof(argv[argc-3]);
            b = atof(argv[argc-2]);
            n = atoi(argv[argc-1]);
        }
        else /* Otherwise we will use the standard arguments */
        {
            if(verbose) printf("Default Arguments:\n");
        }

        if(verbose)
        {
            printf("a is %5.3f\n", a);
            printf("b is %5.3f\n", b);
            printf("n is %d\n", n);
        }
//mengxi
        if(n<=0) {
        printf("Error: n <= 0 or n is not a number.\n");
        MPI_Abort(MPI_COMM_WORLD,1); /* Here I prescribe error code 1 for inputs. */
        }
    }
   
    MPI_Bcast(&a,1,MPI_FLOAT,0,MPI_COMM_WORLD);
    MPI_Bcast(&b,1,MPI_FLOAT,0,MPI_COMM_WORLD);
    MPI_Bcast(&n,1,MPI_INT,0,MPI_COMM_WORLD);
    MPI_Bcast(&if_sin,1,MPI_INT,0,MPI_COMM_WORLD);
//mengxi
    /* Otherwise we will use the standard arguments*/

    h = (b-a)/n;    /* h is the same for all processes */
    local_n = n/p;  /* So is the number of trapezoids */

//mengxi
    residual =  n%p;
//mengxi

    /* Length of each process' interval of
     * integration = local_n*h.  So my interval
     * starts at: */
    local_a = a + my_rank*local_n*h;
//mengxi
    if (my_rank < residual) {
        local_n ++;
        local_a += my_rank*h;
    } else {
        local_a += residual*h;
    }
    local_b = local_a + local_n*h;
//mengxi
    integral = Trap(local_a, local_b, local_n, h, if_sin);

//mengxi
    if(verbose) {
        MPI_Gather(&local_n,1,MPI_INT,global_n,1,MPI_INT,0,MPI_COMM_WORLD);
        MPI_Gather(&local_a,1,MPI_FLOAT,global_a,1,MPI_FLOAT,0,MPI_COMM_WORLD);
        MPI_Gather(&local_b,1,MPI_FLOAT,global_b,1,MPI_FLOAT,0,MPI_COMM_WORLD);
        if(my_rank == 0) {
            for(source = 0; source < p; source++) {
                printf("Process %d: %d subintervals from %f to %f\n",
                       source,global_n[source],global_a[source],global_b[source]);
            }
        }
    }
//mengxi

    /* Add up the integrals calculated by each process */
/*
    if (my_rank == 0) {
        total = integral;
        for (source = 1; source < p; source++) {
            MPI_Recv(&integral, 1, MPI_FLOAT, MPI_ANY_SOURCE, tag,
                MPI_COMM_WORLD, &status);
            total = total + integral;
        }
    } else {  
        MPI_Send(&integral, 1, MPI_FLOAT, dest,
            tag, MPI_COMM_WORLD);
    }
*/
    MPI_Reduce(&integral,&total,1,MPI_FLOAT,MPI_SUM,0,MPI_COMM_WORLD);
    /* Print the result */

    if (my_rank == 0) {
        printf("With n = %d trapezoids, our estimate of the integral\n", n);
        printf("from %5.3f to %5.3f = %5.3f\n", a, b, total);
        /*Other things to print:
         * True Value
         * True Error
         * h^2
         * h
         * n - number of intervals
         * p - number of processes */
        if(if_sin) {
            true_value = cos(M_PI*a)-cos(M_PI*b);
        }
        else {
            true_value = (pow(b,3)-pow(a,3))/3.0;
        }
        printf("True Value: %5.3f\n", true_value);
    }
    /* Shut down MPI */
    MPI_Finalize();
} /*  main  */


float Trap(
          float  local_a   /* in */,
          float  local_b   /* in */,
          int    local_n   /* in */,
          float  h         /* in */,
          bool   if_sin) {

    float integral;   /* Store result in integral  */
    float x;
    int i;

    float x_square(float x); /* function we're integrating */
    float pi_sin_pi_x(float x);

    float (*f[])(float) = {x_square, pi_sin_pi_x};

    x=local_a;
    integral = ((*f[if_sin])(local_a) + (*f[if_sin])(local_b))/2.0;
    for (i = 1; i <= local_n-1; i++) {
        x = x + h;
        integral = integral + (*f[if_sin])(x); }
    integral = integral*h;
    return integral;
} /*  Trap  */


float x_square(float x) {
    float return_val;
    /* Calculate f(x). */
    /* Store calculation in return_val. */
    return_val = x*x;
    return return_val;
} /* f */

float pi_sin_pi_x(float x) {
    float return_val;
    /* Calculate f(x). */
    /* Store calculation in return_val. */
    return_val = M_PI*sin(M_PI*x);
    return return_val;
} /* f */
