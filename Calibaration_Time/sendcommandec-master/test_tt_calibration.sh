#!/bin/bash
echo "Bash version ${BASH_VERSION}..."

##################################hold delay test################################
# for i in {2..30..1}
# do 
#   echo "Delay time is  $i ns"
#   ./set_pulse_generator_time.py $i
#   ./send_named_cmd_cb.py CB22  hold_dly_set --dst_rob 13 --value 0
#   ./send_named_cmd_cb.py CB22  launch_acq  --nevents 50000 
#   sleep 50
#   ./send_named_cmd_cb.py CB22  stop_acq 
# done
##############################################hold delay tes ###########################
# for i in {-100..200..10}
# do 
#   echo "Delay time is  $i ns"
#   ./send_named_cmd_cb.py CB22  hold_dly_set --dst_rob 13 --value $i
#   ./send_named_cmd_cb.py CB22  launch_acq  --nevents 50000 
#   sleep 30
#   ./send_named_cmd_cb.py CB22  stop_acq 
# done
###############################################gain calibration test####################
for i in {48..60..2}
do
  echo "Attenuator value is $i"
  ./set_attenuator_value.py $i --debug
  ./send_named_cmd_cb.py CB22  hold_dly_set --dst_rob 13 --value 0
  ./send_named_cmd_cb.py CB22  launch_acq  --nevents 50000 
  sleep 50
  ./send_named_cmd_cb.py CB22  stop_acq 
done
