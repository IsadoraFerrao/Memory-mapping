set terminal postscript eps enhanced color
set boxwidth 1.9 relative
set style fill solid border -1
set style data histogram
set style histogram cluster gap 1.5

set ytics 10
set xtics 1
set terminal png size 1000,500

set grid ytics
set grid xtics
#set nokey

set yrange [0:150]
set xrange [-1:]

set title "MAPEAMENTO DE TAREFAS - PATH LOAD"

set ylabel "Ocupacao dos canais (%)"
set xlabel "Canais de Comunicacao (Origem, Destino)"

plot 'PathLoad.dat' using 2 linecolor rgb "red" title "Ocupacao do Canal"
replot 'PathLoad.dat' using 5 linecolor rgb "black" with lines title "Media"
replot 'PathLoad.dat' using 1:2:(sprintf("(%d,%d)", $3, $4)) with labels offset -4,0.5 notitle

set terminal png
set output 'PathLoadGrafico.png'
replot
