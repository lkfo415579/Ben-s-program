#!/bin/bash

[ $# -eq 0 ] && { echo "Usage: $0 sep_line_no sep_file"; exit 1; }
#[ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }


_SEP_LINE=$1
_SEP_FILE=$2


_CP_FILE=$_SEP_FILE.thisIsTmpFileForSep
echo "Copy a tmp file: $_CP_FILE"
cp $_SEP_FILE $_CP_FILE


echo "Separate tmp file:"
_file=$_CP_FILE
i=0
 
while [ -s "$_file" ]	
do
	echo "$_file has some data, processing part $i"
	j=$(($_SEP_LINE-1))
	head -$_SEP_LINE $_file > $_SEP_FILE.$i && sed -i "1,+$j d" $_file
	i=$(($i+1))
done

echo "$i files are generated!"

echo "Delete tmp file: $_CP_FILE"
rm $_CP_FILE
