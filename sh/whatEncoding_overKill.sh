#!/usr/bin/env bash
[ $# -eq 0 ] && { echo "Usage: $0 [input] [output-all-encoding]"; exit 1; }
line=$(printf "=%.0s" {1..50})
for FMT in $(iconv -l | sed -e 's/\/\/$//'); do    
	echo "$line\nFormat $FMT:\n$line" > $2.$FMT
	iconv -f $FMT -t UTF8 < $1 >> $2.$FMT
done
#done > $2
#gedit all.txt
wc -l * | sed -e 's/^ \+//g' | sort -t ' ' -n
