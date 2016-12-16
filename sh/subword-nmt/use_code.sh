[ $# -eq 0 ] && echo "Usage: sh $0 [code-model] [input] [output]" && exit 1;
python ~/program/python/subword-nmt/apply_bpe.py -c $1 < $2 > $3
