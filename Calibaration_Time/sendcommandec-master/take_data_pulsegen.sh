#!/usr/bin/bash

NEVENTS=625
IP=192.168.7.205
PORT=5005

for HOLD_DELAY in 0 4 8 12 16;
do
	nc -k -l ${PORT} > timeScan_holdDelay_${HOLD_DELAY}.data &
	NC_PID=$!

	./configFPGA.py ${IP} --hold_delay ${HOLD_DELAY}

	./send_named_cmd_rob.py ${IP} reconnect

	./send_named_cmd_rob.py ${IP} set_run_type --run_type PED
	./send_named_cmd_rob.py ${IP} start_run --nevents ${NEVENTS}
	sleep $(( ${NEVENTS}*16/2000 + 2 ));
	./send_named_cmd_rob.py ${IP} stop_run

	./send_named_cmd_rob.py ${IP} set_run_type --run_type Norm
	for dt in `seq -300 20 -50` `seq -49 1 399` `seq 400 5 1000`; do
		./set_pulse_generator_time.py $dt
		sleep 1;
		./send_named_cmd_rob.py ${IP} start_run --nevents ${NEVENTS}
		sleep $(( ${NEVENTS}*16/1000 + 2 ));
		./send_named_cmd_rob.py ${IP} stop_run
	done

	./send_named_cmd_rob.py ${IP} set_run_type --run_type PED
	./send_named_cmd_rob.py ${IP} start_run --nevents ${NEVENTS}
	sleep $(( ${NEVENTS}*16/2000 + 2 ));
	./send_named_cmd_rob.py ${IP} stop_run

	sleep 1;
	kill -9 ${NC_PID}
	ps aux |grep ${NC_PID}
	netstat -tanpu |grep 5005
	sleep 120;
done
