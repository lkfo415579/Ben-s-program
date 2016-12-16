[ $# -eq 0 ] && echo "Usage: sh $0 [input] [filterName] [model/mert]" && exit 1;
inputFile=$1
filterName=$2
model=$3

MOSES_INI=$model/moses.ini
FILTERED_MOSES_FILE=filter-$model-$filterName

cat $inputFile | sed -e 's/<[^>]*>//g' -e 's/^ *//g' -e 's/ *$//g' -e 's/  */ /g' > $filterName.input.sent

if [ ! -f $FILTERED_MOSES_FILE/moses.ini ]; then 
	~/mosesdecoder/scripts/training/filter-model-given-input.pl $FILTERED_MOSES_FILE $MOSES_INI $filterName.input.sent 
fi

cat $filterName.input.sent | ~/mosesdecoder/bin/moses \
	-f $FILTERED_MOSES_FILE/moses.ini \
	> output.$model.$filterName

rm $filterName.input.sent

