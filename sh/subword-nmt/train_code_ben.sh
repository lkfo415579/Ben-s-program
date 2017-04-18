[ $# -eq 0 ] && echo "Usage: sh $0 [size] [input] [code-model]" && exit 1;
python ~/program/python/subword-nmt/learn_bpe_ben.py -s $1 < $2 > $3
