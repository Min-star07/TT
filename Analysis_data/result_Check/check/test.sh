#!/bin/bash
#Simple for loop example
rob_num=(15)
# chan_num=(4 5 9 10 11 14 18 19 21 22 28 31 32 35 36 40 42 43 45 50 51 53 56 59 60 61)
# chan_num=(10 14 15 29 35 36 39 50 51 52 58)
chan_num=(26 33 61 32)
# for i in {5..5}
for i in "${rob_num[@]}"
do
    echo "Iteration =========================ROB: $i"
    for j in "${chan_num[@]}" 
    do
        echo "Iteration ===================================channel: $j"
        #  ./RunFitter -led ./data/led_cCB-22_2023-12-18_18_12_hist.root -ped ./data/ped_cCB-22_2023-12-18_18_19_hist.root -ROB $i -channel_start 27 -channel_end 29  -sigma 3
        # ./RunFitter -led ../TTtele/data/led_cCB-22_2023-12-18_18_18_hist.root -ped ../TTtele/data/ped_cCB-22_2023-12-18_18_20_hist.root -ROB $i -channel_start 53 -channel_end 54  -sigma 3
        ./RunFitter -m 2 -q 12 -led ../../Data/20240119/led_cCB-22_2024-01-18_09_36_hist.root -ped ../../Data/pedestal/ped_cCB-22_2024-01-09_17_40_hist.root  -ROB $i -channel $j  -sigma 3
        # ./RunFitter -led ../TTtele/data/led_cCB-22_2024-01-09_18_08_hist.root -ped ../TTtele/data/ped_cCB-22_2024-01-09_17_36_hist.root -ROB $i -channel_start 19 -channel_end 20  -sigma 3
    done
done
