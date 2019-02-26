set title "Total Values"
set ylabel "Instances"
set xlabel "Number of Photons tested"
plot "scatter.out" u 1:2 w l title "N_{ref}", "scatter.out" u 1:3 w l title "N_{abs}", "scatter.out" u 1:4 w l title "N_{tra}"
pause -1

set title "Estimates of Physical Values"
set ylabel "Current Fraction"
plot "scatter.out" u 1:($2/$1) w l title "reflectivity", "scatter.out" u 1:($3/$1) w l title "absorbtion", "scatter.out" u 1:($4/$1) w l title "transmittance"
pause -1
