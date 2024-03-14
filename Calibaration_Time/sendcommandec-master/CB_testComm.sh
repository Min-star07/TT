#!/usr/bin/zsh

CB_ID=$1

if [[ "x$CB_ID" == "x" ]]; then
	echo "Usage: $0 <CBid>"
	exit 1
fi

i=0
i_err=0
while [ 1 ]; do
	CMD_REPLY=`./send_named_cmd_cb.py CB${CB_ID} recv_udp`
	if [[ ${CMD_REPLY} != "23130 [0x5a5a]" ]]; then
		i_err=$((i_err+1))
		echo "Try $i [err=${i_err}] | ${CMD_REPLY}"
	else
		printf "Try $i [err=${i_err}] | ${CMD_REPLY}\r"
	fi
	i=$((i+1))
	sleep 1
done

