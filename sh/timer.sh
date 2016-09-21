#!/bin/ksh

[ $# -eq 0 ] && { echo "Usage: $0 display_seconds file_RE"; exit 1; }

time=$1
time="${time:-1}"

while (true); do
  date
  for i in ${@:2}
  do
    wc -l $i
  done
  sleep $time
  wait
done
