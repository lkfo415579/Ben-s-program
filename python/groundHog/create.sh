#!/bin/bash

[ $# -eq 0 ] && { echo "Usage: $0 [input_source] [input_target] [output_dir]"; exit 1; }
#[ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }


INPUT_SOURCE=$1
INPUT_TARGET=$2
OUTPUT_DIR=$3
OUTPUT_NAME=$OUTPUT_DIR/train

mkdir -p $OUTPUT_DIR

python preprocess.py $INPUT_SOURCE -d $OUTPUT_NAME.source.wordid.pkl -v 50000 -b $OUTPUT_DIR/binarized_text.source.pkl -p
python preprocess.py $INPUT_TARGET -d $OUTPUT_NAME.target.wordid.pkl -v 50000 -b $OUTPUT_DIR/binarized_text.target.pkl -p

python invert-dict.py $OUTPUT_NAME.source.wordid.pkl $OUTPUT_NAME.source.idword.pkl
python invert-dict.py $OUTPUT_NAME.target.wordid.pkl $OUTPUT_NAME.target.idword.pkl

python convert-pkl2hdf5.py $OUTPUT_DIR/binarized_text.source.pkl $OUTPUT_DIR/binarized_text.source.h5
python convert-pkl2hdf5.py $OUTPUT_DIR/binarized_text.target.pkl $OUTPUT_DIR/binarized_text.target.h5

python shuffle-hdf5.py $OUTPUT_DIR/binarized_text.source.h5 $OUTPUT_DIR/binarized_text.target.h5 $OUTPUT_DIR/binarized_text.shuffled.source.h5 $OUTPUT_DIR/binarized_text.shuffled.target.h5


