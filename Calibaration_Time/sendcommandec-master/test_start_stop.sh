#!/bin/bash

if [[ "x$1" == "x" ]]; then
	CARD="2L"
else
	CARD=$1
	shift
fi

if [[ "x$1" == "x" ]]; then
	DATA_TAKING_TIME=1200
else
	DATA_TAKING_TIME=$1
	shift
fi

echo "${DATA_TAKING_TIME} wait time set"

case $CARD in
	"0L")
		CARD_NUM=7
		;;
	"1L")
		CARD_NUM=3
		;;
	"2L")
		CARD_NUM=2
		;;
	"3L")
		CARD_NUM=5
		;;
	"0R")
		CARD_NUM=6
		;;
	"1R")
		CARD_NUM=9
		;;
	"2R")
		CARD_NUM=8
		;;
	"3R")
		CARD_NUM=4
		;;
	*)
		echo "CARD not defined"
		exit 1
esac

IP=192.168.7.20${CARD_NUM}

EXE=/data/ElectronicsCard/SendCommandEC/send_named_cmd_rob.py

i=0
while [[ 1 ]]; do
	echo "Starting card ${CARD} run #${i}"
	${EXE} ${IP} start_run --nevents 0
	sleep ${DATA_TAKING_TIME}
	${EXE} ${IP} stop_run
	sleep 60
	i=$((i+1))
done
