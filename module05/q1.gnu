#!/usr/bin/gnuplot

#If the program will not run as a script, then the gnuplot program is in a different location.
#It should run using 'gnuplot q1.gnu' as well.

set terminal X enhanced

set title  "Relationship between {/Symbol t}_c and Reflectance for varying {/Symbol w}"
set xlabel "{/Symbol t}_c"
set ylabel "Reflectance"
set key left

plot for [i=0:*] 'question_1.dat' index i w l title columnheader(1)
pause -1

set terminal png enhanced size 1200, 900
set output "q1.png"
replot

