#!/bin/bash

[ $# -eq 0 ] && { echo "Usage: $0 [sep_line_no] [sep_file] [max_line]"; exit 1; }
#[ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }


_SEP_LINE=$1
_SEP_FILE=$2
_MAX_LINE=$3

_file=$_SEP_FILE
i=0
_start=1
_end=$_SEP_LINE
 
while [ $_end -lt $_MAX_LINE ]	
do
	echo "$_file has some data, processing part $i, from $_start to $_end"
	sed -n ${_start},${_end}p $_file > $_file.$i 
	i=$(($i+1))
	_start=$(($_start+$_SEP_LINE))
	_end=$(($_end+$_SEP_LINE))
done

echo "$i files are generated!"

find ./ -size 0 -print0 |xargs -0 rm

