MOSES_INI=model/moses.ini
FILTERED_MOSES_FILE=filter_$1

cat $1 > tmp.$1.input && \
cat tmp.$1.input | sed -e 's/<[^>]*>//g' -e 's/^ *//g' -e 's/ *$//g' -e 's/  */ /g' > tmp.$1.input.sent

if [ ! -f $FILTERED_MOSES_FILE/moses.ini ]; then 
	~/mosesdecoder/scripts/training/filter-model-given-input.pl $FILTERED_MOSES_FILE $MOSES_INI tmp.$1.input.sent 
fi

cat tmp.$1.input | ~/mosesdecoder/bin/moses \
	-f $FILTERED_MOSES_FILE/moses.ini \
	-dl $2 \
	-alignment-output-file tmp.$1.align \
	> tmp.$1.output.dl$2 && \
python ~/program/kendall_tau.py tmp.$1.align 
#python latexAlignFormating_oneSent.py tmp.$1.input.sent tmp.$1.output tmp.$1.align 0 #&& \
#rm tmp.$1.*

