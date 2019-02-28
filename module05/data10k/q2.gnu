#!/usr/bin/gnuplot

#If the program will not run as a script, then the gnuplot program is in a different location.
#It should run using 'gnuplot q2.gnu' as well.

binwidth=0.1
bin(x,width)=width*floor(x/width)

set xlabel "Maximum Depth"
set ylabel "Number of Photons in each Range"
set xrange [0:10]
set yrange [0:500]

do for [omega in "1.0 0.96 0.92 0.88"] {
    set terminal X
    set output

    set title  "Histogram of Maximum Depths of Reflected Photons: Omega = ".omega
    plot 'question_2_omega_'.omega.'.dat' using (bin($1,binwidth)):(1.0) smooth freq with boxes title ""
    pause -1

    set terminal png enhanced size 1200, 900
    set output "q2_omega_".omega.".png"
    replot
}
