#!/bin/bash

if [[ "x$1" == "x" ]]; then
	CARD="2L"
else
	CARD=$1
	shift
fi

if [[ "x$1" == "x" ]]; then
	HV=700
else
	HV=$1
	shift
fi

if [[ "x$1" == "x" ]]; then
	DATE_TAG=`date +%Y-%m-%d_%H:%M`
else
	DATE_TAG=$1
	shift
fi

LED_BIAS=520

case $CARD in
	"0L")
		CARD_NUM=7
		;;
	"1L")
		CARD_NUM=3
		LED_BIAS=440
		;;
	"2L")
		CARD_NUM=2
		LED_BIAS=440
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
PORT=500${CARD_NUM}

EXE=/data/ElectronicsCard/SendCommandEC/send_any_rob.py

RUNLED=/data/ElectronicsCard/decodemuontelescope/run_LED.sh

OUTPUT_FILE=/data/ElectronicsCard/data/ped_hv${HV}_c${CARD}_${DATE_TAG}.data

CACHE=/data/ElectronicsCard/cache
ROOT_CACHE=/data/ElectronicsCard/root_cache

echo "Setting up data taking for ${CARD} @ ${HV} V"

# LED bias set
${EXE} ${IP} --command 0x50 --payload ${LED_BIAS}

# HV set
${EXE} ${IP} --command 0x10 --payload ${HV}

# HV update
${EXE} ${IP} --command 0x60

# Set PED run mode
${EXE} ${IP} --command 0x03 --payload 0x1

nc -l ${PORT} > ${OUTPUT_FILE} &
NC_PID=$!

sleep 20

# reconnect to server
${EXE} ${IP} --command 0xe1

echo "Starting PED data taking for ${CARD} @ ${HV} V"

# start acquisition
${EXE} ${IP} --command 0x05 --payload 6250

sleep 10

FILE_SIZE=`du -b ${OUTPUT_FILE} | awk '{ print $1 }'`
while [[ 1 ]]; do
	sleep 1
	FILE_SIZE_NEW=`du -b ${OUTPUT_FILE} | awk '{ print $1 }'`
	if [[ ${FILE_SIZE} -eq ${FILE_SIZE_NEW} ]]; then
		break
	fi
	FILE_SIZE=${FILE_SIZE_NEW}
done

kill ${NC_PID}

echo "PED data for ${CARD} @ ${HV} V taken"

${RUNLED} ${OUTPUT_FILE} ${CACHE} ${ROOT_CACHE} &


OUTPUT_FILE=/data/ElectronicsCard/data/led_hv${HV}_c${CARD}_${DATE_TAG}.data

# Set LED run mode
${EXE} ${IP} --command 0x03 --payload 0x3

nc -l ${PORT} > ${OUTPUT_FILE} &
NC_PID=$!

sleep 20

# reconnect to server
${EXE} ${IP} --command 0xe1

echo "Starting LED data taking for ${CARD} @ ${HV} V"

# start acquisition
${EXE} ${IP} --command 0x05 --payload 62500

sleep 10

FILE_SIZE=`du -b ${OUTPUT_FILE} | awk '{ print $1 }'`
while [[ 1 ]]; do
	sleep 1
	FILE_SIZE_NEW=`du -b ${OUTPUT_FILE} | awk '{ print $1 }'`
	if [[ ${FILE_SIZE} -eq ${FILE_SIZE_NEW} ]]; then
		break
	fi
	FILE_SIZE=${FILE_SIZE_NEW}
done

kill ${NC_PID}

echo "LED data for ${CARD} @ ${HV} V taken"

${RUNLED} ${OUTPUT_FILE} ${CACHE} ${ROOT_CACHE} &
