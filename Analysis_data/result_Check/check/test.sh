#!/bin/bash


#Simple for loop example
# python3 result_problem_confirm.py --CB 22 -ROB 15 --mode 2
# rob_num=(15)
# chan_num=(4 19 24 25 26 33 34 40 42 44 47 48 49 50 51 53 57 59 61 21 32 46)
# # chan_num=(10 14 15 29 35 36 39 50 51 52 58)
# # chan_num=(26 33 61 32)
# # for i in {5..5}
# for i in "${rob_num[@]}"
# do
#     echo "Iteration =========================ROB: $i"
#     for j in "${chan_num[@]}" 
#     do
#         echo "Iteration ===================================channel: $j"
#         #  ./RunFitter -led ./data/led_cCB-22_2023-12-18_18_12_hist.root -ped ./data/ped_cCB-22_2023-12-18_18_19_hist.root -ROB $i -channel_start 27 -channel_end 29  -sigma 3
#         # ./RunFitter -led ../TTtele/data/led_cCB-22_2023-12-18_18_18_hist.root -ped ../TTtele/data/ped_cCB-22_2023-12-18_18_20_hist.root -ROB $i -channel_start 53 -channel_end 54  -sigma 3
#         ./RunFitter -m 2 -q 90 -mu 1.0 -times 0 -led ../../result_GEN/Data/20240116/led_cCB-22_2024-01-16_20_37_hist.root -ped ../../result_GEN/Data/pedestal/ped_cCB-22_2024-01-09_17_40_hist.root  -ROB $i -channel $j
#         # ./RunFitter -led ../TTtele/data/led_cCB-22_2024-01-09_18_08_hist.root -ped ../TTtele/data/ped_cCB-22_2024-01-09_17_36_hist.root -ROB $i -channel_start 19 -channel_end 20  -sigma 3
#     done
# done


CB_id=22
ROB_id=15

filename="/home/lim/Desktop/TT/Analysis_data/result_Final/CB$CB_id/ROB$ROB_id/check_channel.txt"
echo $filename
readarray -t lines < <(awk '!$2 && $2 != 0 {print}' "$filename")

for CH_id in "${lines[@]}"
# sed 1d "$filename" | while IFS= read -r line
do
    echo $CH_id
    ./RunFitter -m 2 -q 100 -mu 2 -times -2 -led ../../result_GEN/Data/20240116/led_cCB-22_2024-01-16_20_37_hist.root -ped ../../result_GEN/Data/pedestal/ped_cCB-22_2024-01-09_17_40_hist.root  -ROB $ROB_id -channel $CH_id

done

echo "Problem channel should be check---------------------"
for CH_id in "${lines[@]}"
# sed 1d "$filename" | while IFS= read -r line
do
    echo $CH_id
done
