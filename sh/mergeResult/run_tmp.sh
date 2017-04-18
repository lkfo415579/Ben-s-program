[ $# -eq 0 ] && echo "Usage: ./$0 [output-file] [input-file-*]"

output=$1
shift
inputs=$@

perl LiNMT-obervation.pl \
src src-tok \
ref ref-tok \
mose-base moses.1best \
nsmt-base smt-baseline \
nematus8-bpe ben.neu-nematus-e6.dev-nb8.zh \
nematus3-bpe ben.neu-nematus-e6.dev-nb3.zh \
nmt-base-14 nmt-baseline-14 \
nmt-bpe-12 nmt-bpe-12 \
nmt-bpe-14 nmt-bpe-14 \
> observation.04142017.txt

