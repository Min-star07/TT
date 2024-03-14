#!/bin/bash

#!/bin/bash
#Simple for loop example
rob_num=(15)
# chan_num=(4 5 9 10 11 14 18 19 21 22 28 31 32 35 36 40 42 43 45 50 51 53 56 59 60 61)
chan_num=(26 33 61 32)
# for i in {5..5}
for i in "${rob_num[@]}"
do
    echo "Iteration =========================ROB: $i"
    for j in "${chan_num[@]}" 
    do
        echo "Iteration ===================================channel: $j"
         ./Run_Getfigure -ROB $i -CH $j
        done
done
