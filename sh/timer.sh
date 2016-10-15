#!/bin/ksh

if [ $# -eq 0 ]
then
	echo "Usage: $0 [display_seconds] [command]"
else
	time=$1
	time="${time:-1}"
	shift
	while (true); do
	  date
		eval $@
		sleep $time
		wait
	done;
fi
