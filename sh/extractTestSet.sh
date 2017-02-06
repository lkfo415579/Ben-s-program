[ $# -eq 0 ] && echo "Usage: sh $0 [source] [target] [output_name] [number]" && exit 1

src=$1
tgt=$2
out=$3
num=$4

time python ~/program/python/extractTestSet.py --s $1 --t $2 --o $3 --num $4
