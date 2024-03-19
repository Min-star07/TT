#!/bin/bash
conda activate
# Run the Python script
numbers=(15)
# for i in {5..5}
for i in "${numbers[@]}"
do 
    python merge.py 22 $i 2
    ./Run_Getfigure -CB 22 -ROB $i -MODE 2
done

python3 main.py --CB 22 --ROB 15 --mode 2

# Run the Python script
# numbers=(15)
# # for i in {5..5}
# for i in "${numbers[@]}"
# do 
#     python3 analysis_Q1.py 22 $i 2
#     python analysis_check.py 22 $i 2
#     # python analysis_Q1_compare.py 22 15 /CB22_ROB15_final_result_mode_1.txt /CB22_ROB15_final_result_mode_2.txt
# done
