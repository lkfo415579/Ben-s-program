#!/bin/bash

[ $# -eq 0 ] && { echo "Usage: $0 input_name mode"; exit 1; }
#[ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }

_INPUT_NAME=$1
_ID=0
_CMD="cat "
_MODE=$2
 
if [ $_MODE -eq 1 ]
then
	while [ -s "$_INPUT_NAME.$_ID" ]	
	do
		_CMD="$_CMD $_INPUT_NAME.$_ID"
		_ID=$(($_ID+1))
	done
else
	while [ -s "$_INPUT_NAME.$_ID.tmp" ]	
	do
		_CMD="$_CMD $_INPUT_NAME.$_ID.tmp"
		_ID=$(($_ID+1))
	done
fi
	

if [ $_ID > 0 ]
then
	_CMD="$_CMD > $_INPUT_NAME.out"
	echo $_CMD
	eval $_CMD
fi
