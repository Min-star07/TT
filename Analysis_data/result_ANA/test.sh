#!/bin/bash

# Run the Python script
numbers=(5)
# for i in {5..5}
for i in "${numbers[@]}"
do 
    python merge.py 22 $i 2
    ./Run_Getfigure -CB 22 -ROB $i -MODE 2
done