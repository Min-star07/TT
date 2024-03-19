#!/bin/bash

#!/bin/bash
#Simple for loop example
# rob_num=(15)
# chan_num=(4 19 24 25 26 33 34 40 42 44 47 48 49 50 51 53 57 59 61 21 32 46)
# # for i in {5..5}
# for i in "${rob_num[@]}"
# do
#     echo "Iteration =========================ROB: $i"
#     for j in "${chan_num[@]}" 
#     do
#         echo "Iteration ===================================channel: $j"
#          ./Run_Getfigure -ROB $i -CH $j
#         done
# done


CB_id=22
ROB_id=15

filename="/home/lim/Desktop/TT/Analysis_data/result_Final/CB$CB_id/ROB$ROB_id/check_channel.txt"
echo $filename
readarray -t lines < <(awk '!$2 && $2 != 0 {print}' "$filename")
for CH_id in "${lines[@]}"
# sed 1d "$filename" | while IFS= read -r line
do
    echo "ROB$ROB_id ---------CHANNRL$CH_id----------------------"
    ./Run_Getfigure -ROB $ROB_id -CH $CH_id
done

echo "Problem channel should be check---------------------"
for CH_id in "${lines[@]}"
# sed 1d "$filename" | while IFS= read -r line
do
    echo $CH_id
done
