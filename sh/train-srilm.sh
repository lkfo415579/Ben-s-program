[ $# -eq 0 ] && echo "Usage: sh $0 [input] [output] [n-gram]" && exit 1;

SRILM_BINDIR=/home/mb55417/tool/srilm-1.7.1/bin/i686-m64

input=$1
output=$2
ngram=$3

${SRILM_BINDIR}/ngram-count -order $ngram -text $input -lm $output -interpolate -kndiscount -unk

