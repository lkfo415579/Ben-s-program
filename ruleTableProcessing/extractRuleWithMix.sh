#!/bin/bash

if [$4 = ""]; then
	echo "Usage: $0 rule-table source-lm #linear #nonlinear clear(optional)"
	exit
fi

RULE_TABLE_FILE=$1
LM_FILE=$2
NUM_LINEAR=$3
NUM_NONLINEAR=$4

echo "picking nonlinear align..."
python pickNonLinearAlign.py ${RULE_TABLE_FILE} ${RULE_TABLE_FILE} 

echo "picking count larger than ${NUM_LINEAR} from linear file..."
python pickLargeThenCount.py ${NUM_LINEAR} ${RULE_TABLE_FILE}.linear ${RULE_TABLE_FILE}.linear.${NUM_LINEAR}

echo "picking count larger than ${NUM_NONLINEAR} from nonlinear file..."
python pickLargeThenCount.py ${NUM_NONLINEAR} ${RULE_TABLE_FILE}.nonlinear ${RULE_TABLE_FILE}.nonlinear.${NUM_NONLINEAR}

echo "# of line of extracted file"
wc -l ${RULE_TABLE_FILE}.*

echo "combining linear (${NUM_LINEAR}) with nonlinear (${NUM_NONLINEAR}) to one file"
cat ${RULE_TABLE_FILE}.linear.${NUM_LINEAR} ${RULE_TABLE_FILE}.nonlinear.${NUM_NONLINEAR} > ${RULE_TABLE_FILE}.mix.${NUM_LINEAR}.${NUM_NONLINEAR}

echo "main processing..."
python main.py ${RULE_TABLE_FILE}.mix.${NUM_LINEAR}.${NUM_NONLINEAR} ${RULE_TABLE_FILE}.mix.${NUM_LINEAR}.${NUM_NONLINEAR} ${LM_FILE}
 
if [ $5 = "clear" ]; then
	echo "removing mid-file..."
	rm ${RULE_TABLE_FILE}.linear ${RULE_TABLE_FILE}.linear.${NUM_LINEAR} ${RULE_TABLE_FILE}.nonlinear ${RULE_TABLE_FILE}.nonlinear.${NUM_NONLINEAR} ${RULE_TABLE_FILE}.mix.${NUM_LINEAR}.${NUM_NONLINEAR}
fi
echo "output file: ${RULE_TABLE_FILE}.mix.${NUM_LINEAR}.${NUM_NONLINEAR}.uni"
