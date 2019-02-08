/* trap.c -- Parallel Trapezoidal Rule, first version
 *
 * Input: (char)fun, (double)a, (double)b, (int)n
 * ./trap
 * ./trap (char)fun
 * ./trap (int)n
 * ./trap (char)fun (int)n
 * ./trap (double)a (double)b
 * ./trap (char)fun (double)a (double)b
 * ./trap (double)a (double)b (int)n
 * ./trap (char)fun (double)a (double)b (int)n
 * The character (or string) "fun" prescribes the function. It must start 
 * with a letter (case insensitive). If it starts with 's' or 'S', then 
 * the function pi*sin(pi*x) is used. Otherwise, the function x^2 is used.
 *
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
 *    1.  None of f(x), a, b, and n is hardwired.
 *    2.  The number of processes (p) does not need to evenly 
 *        divide the number of trapezoids
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
    double      a = 0.0;   /* Left endpoint             */
    double      b = 1.0;   /* Right endpoint            */
    int         n = 16384; /* Number of trapezoids      */
    double      h;         /* Trapezoid base length     */
    double      local_a;   /* Left endpoint my process  */
    double      local_b;   /* Right endpoint my process */
    int         local_n;   /* Number of trapezoids for  */
                           /* my calculation            */
    int         residual;  /* the residual of n/p       */
    bool        if_sin = false;  /* which function      */
    double      true_value;      /* true value          */
    bool        set_fun = false; /* input function      */
    double      startTime, endTime, tsec;
    double      err;       /* true error                */
    double      integral;  /* Integral over my interval */
    double      total;     /* Total integral            */
    int         source;    /* Process sending integral  */
    int         dest = 0;  /* All messages go to 0      */
    int         tag = 0;
    MPI_Status  status;

    /* Change to False for main runs, True will give more information. */
    bool verbose = false;

    double Trap(double local_a, double local_b, int local_n,
                double h, bool if_sin);    /* Calculate local integral  */

    /* Let the system do what it needs to start up MPI */
    MPI_Init(&argc, &argv);

    /* Get the start time */
    MPI_Barrier(MPI_COMM_WORLD);
    startTime = MPI_Wtime();

    /* Get my process rank */
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    /* Find out how many processes are being used */
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    /* space allocated to store the local_n, local_a, local_b of all processes */
    int        global_n[p];
    double     global_a[p];
    double     global_b[p];

    /* Process command line arguments */
    if(my_rank==0) {
        /* which function to use */
        if(argc>1 && ((argv[1][0]>='a' && argv[1][0]<='z') || 
           (argv[1][0]>='A' && argv[1][0]<='Z'))) {
            set_fun = true;
            if(argv[1][0]=='s' || argv[1][0]=='S') { /* Use pi*sin(pi*x) */
                if_sin = true;
            }
        }
        /* use command inputs of a, b and/or n */
        if(argc>1+set_fun)
        {
            if(verbose) printf("Command Line Arguments:\n");
            switch(argc-set_fun) {
                case 2:
                    n = atoi(argv[set_fun+1]);
                    break;
                case 3:
                    a = atof(argv[set_fun+1]);
                    b = atof(argv[set_fun+2]);
                    break;
                default:
                    a = atof(argv[set_fun+1]);
                    b = atof(argv[set_fun+2]);
                    n = atoi(argv[set_fun+3]);
            }
        }
        else /* Otherwise we will use the standard arguments */
        {
            if(verbose) printf("Default Arguments:\n");
        }

        if(verbose)
        {
            printf("a is %5.3lf\n", a);
            printf("b is %5.3lf\n", b);
            printf("n is %d\n", n);
        }
        /* input error */
        if(n<=0) {
        printf("Error: n <= 0 or n is not a number.\n");
        MPI_Abort(MPI_COMM_WORLD,1); /* Here I prescribe error code 1 for inputs. */
        }
    }
   
    /* Broadcast input variables */
    MPI_Bcast(&a,1,MPI_DOUBLE,0,MPI_COMM_WORLD);
    MPI_Bcast(&b,1,MPI_DOUBLE,0,MPI_COMM_WORLD);
    MPI_Bcast(&n,1,MPI_INT,0,MPI_COMM_WORLD);
    MPI_Bcast(&if_sin,1,MPI_INT,0,MPI_COMM_WORLD);

    h = (b-a)/n;    /* h is the same for all processes                        */
    local_n = n/p;  /* the number of trapezoids is not necessarily the same   */
    residual = n%p; /* the first several processes will have 1 more trapezoid */

    /* Length of each process' interval of
     * integration = local_n*h.  So my interval
     * starts at: */
    local_a = a + my_rank*local_n*h;
    /* the first several processes will have 1 more trapezoid */
    if (my_rank < residual) {
        local_n ++;
        local_a += my_rank*h;
    } else {
        local_a += residual*h;
    }
    local_b = local_a + local_n*h;
    /* in addition to local_a, local_b and local_n, if_sin is another argument */
    integral = Trap(local_a, local_b, local_n, h, if_sin);

    /* report the number of trapezoids of each process */
    if(verbose) {
        MPI_Gather(&local_n,1,MPI_INT,global_n,1,MPI_INT,0,MPI_COMM_WORLD);
        MPI_Gather(&local_a,1,MPI_DOUBLE,global_a,1,MPI_DOUBLE,0,MPI_COMM_WORLD);
        MPI_Gather(&local_b,1,MPI_DOUBLE,global_b,1,MPI_DOUBLE,0,MPI_COMM_WORLD);
        if(my_rank == 0) {
            for(source = 0; source < p; source++) {
                printf("Process %d: %d subintervals from %24.16e to %24.16e\n",
                       source,global_n[source],global_a[source],global_b[source]);
            }
        }
    }

    /* Add up the integrals calculated by each process */
/*
    if (my_rank == 0) {
        total = integral;
        for (source = 1; source < p; source++) {
            MPI_Recv(&integral, 1, MPI_DOUBLE, MPI_ANY_SOURCE, tag,
                MPI_COMM_WORLD, &status);
            total = total + integral;
        }
    } else {  
        MPI_Send(&integral, 1, MPI_DOUBLE, dest,
            tag, MPI_COMM_WORLD);
    }
*/
    /* MPI_Reduce will simplify the code */
    MPI_Reduce(&integral,&total,1,MPI_DOUBLE,MPI_SUM,0,MPI_COMM_WORLD);

    /* Print the result */
    if (my_rank == 0) {
        printf("With n = %d trapezoids, our estimate of the integral\n", n);
        printf("from %5.3lf to %5.3lf = %24.16e\n", a, b, total);
        if(verbose) {
            if(if_sin) {
                true_value = cos(M_PI*a)-cos(M_PI*b);
            }
            else {
                true_value = (pow(b,3)-pow(a,3))/3.0;
            }
            err=fabs(total - true_value);
            printf("True Value: %24.16e\n", true_value);
            printf("True Error: %24.16e\n", err);
            printf("h^2 = %24.16e\n", h*h);
            printf("C = err/h^2 = %24.16e\n",err/h/h);
            printf("h = %24.16e\n", h);
            printf("n = %d\n", n);
            printf("p = %d\n", p);
        }
    }

    /* report the time used */
    MPI_Barrier(MPI_COMM_WORLD);
    endTime = MPI_Wtime();
    if (my_rank == 0) {
        tsec = endTime - startTime;
        printf("Observed wall clock time in seconds = %11.4e\n",tsec);
    }

    /* Shut down MPI */
    MPI_Finalize();
} /*  main  */


double Trap(
          double local_a   /* in */,
          double local_b   /* in */,
          int    local_n   /* in */,
          double h         /* in */,
          bool   if_sin) {

    double integral;   /* Store result in integral  */
    double x;
    int i;

    double x_squared(double x);   /* default function we're integrating */
    double pi_sin_pi_x(double x); /* alternative function */

    double (*f[])(double) = {x_squared, pi_sin_pi_x};

    x=local_a;
    integral = ((*f[if_sin])(local_a) + (*f[if_sin])(local_b))/2.0;
    for (i = 1; i <= local_n-1; i++) {
        x = x + h;
        integral = integral + (*f[if_sin])(x); }
    integral = integral*h;
    return integral;
} /*  Trap  */


double x_squared(double x) {
    double return_val;
    /* Calculate f(x) = x^2. */
    /* Store calculation in return_val. */
    return_val = x*x;
    return return_val;
} /* f */

double pi_sin_pi_x(double x) {
    double return_val;
    /* Calculate f(x) = pi * sin(pi * x). */
    /* Store calculation in return_val. */
    return_val = M_PI*sin(M_PI*x);
    return return_val;
} /* f */
