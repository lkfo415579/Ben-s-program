[ $# -eq 0 ] && echo "Usage: sh $0 [input-text] [output-vectorModel]" && exit 1;

input=$1
output=$2

time ~/program/word2vec/word2vec -train $input -output $output -cbow 1 -size 500 -window 20 -negative 40 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
