#!/bin/bash

[ $# -eq 0 ] && { echo "Usage: $0 moses_ini input_name output_name mode start_from"; exit 1; }
#[ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }

_MOSES_INI=$1
_INPUT_NAME=$2
_OUTPUT_NAME=$3
_MODE=$4
_ID=$5
_CMD=""
 
if [ "$_MODE" == "1" ]; then
	while [ -s "$_INPUT_NAME.$_ID" ]	
	do
		_CMD="nohup nice ~/mosesdecoder/bin/moses_chart -f $_MOSES_INI < $_INPUT_NAME.$_ID > $_OUTPUT_NAME.$_ID 2> log"
		echo $_CMD
		eval $_CMD
		_ID=$(($_ID+1))
	done
else
	while [ -s "$_INPUT_NAME.$_ID.tmp" ]	
	do
		_CMD="nohup nice ~/mosesdecoder/bin/moses_chart -f $_MOSES_INI < $_INPUT_NAME.$_ID.tmp > $_OUTPUT_NAME.$_ID.tmp 2> log"
		echo $_CMD
		eval $_CMD
		_ID=$(($_ID+1))
	done
fi
