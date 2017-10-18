#!/usr/bin/env bash
[ $# -eq 0 ] && { echo "Usage: $0 [input] [output-all-encoding]"; exit 1; }
line=$(printf "=%.0s" {1..50})
for FMT in $(iconv -l | sed -e 's/\/\/$//'); do    
	echo "$line\nFormat $FMT:\n$line"
	iconv -f $FMT -t UTF8 < $1 | head -10
done > $2
#gedit all.txt
