if [$3 != ""]; then
	echo "Usage: $0 nbest-size nbest-file ref-file"
	exit
fi

N_SIZE=$1
N_BEST=$2
REF=$3

echo "processing nbest file..."
python extractTestScore.py ${N_SIZE} ${N_BEST} test.${N_SIZE}.score test.${N_SIZE}.idsent
echo "creating reference..."
python createNBestReference.py ${REF} test.${N_SIZE}.idsent test.${N_SIZE}.ref test.${N_SIZE}.sent
echo "calculating sentence-bleu..."
~/mosesdecoder/bin/sentence-bleu test.${N_SIZE}.ref < test.${N_SIZE}.sent > test.${N_SIZE}.bleu
echo "selecting the best result..."
python extractBestSingleELM.py test.${N_SIZE}.bleu test.${N_SIZE}.idsent test.${N_SIZE}.best
echo "calculating multi-bleu..."
~/mosesdecoder/scripts/generic/multi-bleu.perl ${REF} < test.${N_SIZE}.best

# remove tmp file, only output test.X.best
#rm test.${N_SIZE}.score test.${N_SIZE}.idsent test.${N_SIZE}.sent test.${N_SIZE}.bleu test.${N_SIZE}.ref
