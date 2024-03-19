#!/bin/bash
#Simple for loop example
numbers=(15)
for i in "${numbers[@]}"
do
    echo "Iteration: $i"
      # ./RunFitter -mode 2 -cb 22 -ROB $i -time 6 -led ./Data/20240116/led_cCB-22_2024-01-16_20_37_hist.root -ped ./Data/pedestal/ped_cCB-22_2024-01-09_17_40_hist.root -channel_start 0 -channel_end 64
      # ./RunFitter -mode 1 -cb 22 -ROB $i -led ../../Data/20240305/Wilki_led_22C4_cCB-22_2024-03-06_10_48_hist.root -ped ../../Data/20240305/Wilki_ped_cCB-22_2024-03-05_16_35_hist.root -channel_start 0 -channel_end 64
      ./RunFitter -mode 2 -cb 22 -ROB $i -time 6 -led ./Data/20240116/led_cCB-22_2024-01-16_20_37_hist.root -ped ./Data/pedestal/ped_cCB-22_2024-01-09_17_40_hist.root -channel_start 0 -channel_end 64
      # ./RunFitter -mode 1 -cb 22 -ROB $i -led ../../Data/20240305/Wilki_led_22C4_cCB-22_2024-03-06_10_48_hist.root -ped ../../Data/20240305/Wilki_ped_cCB-22_2024-03-05_16_35_hist.root -channel_start 0 -channel_end 64
done
