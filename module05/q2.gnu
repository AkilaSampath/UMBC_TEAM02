#!/usr/bin/gnuplot

binwidth=0.1
bin(x,width)=width*floor(x/width)


set title  "Question 2: Histogram of Maximum Depths of Reflected Photons"
set xlabel "Maximum Depth"
set ylabel "Number of Photons in each Range"
plot 'question_2_omega_0.88.dat' using (bin($1,binwidth)):(1.0) smooth freq with boxes title ""
pause -1

set terminal png enhanced size 1200, 900
set output "q2.png"
replot
