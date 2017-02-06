[ $# -eq 0 ] && echo "Usage: sh $0 [source] [target]" && exit 1

d=$(date +"%Y%m%d%H%M%S")
src=$1
tgt=$2

echo "Generate id file ... "
cat $src | nl | sed -e 's/^ \+//g' > $src.$d
cat $tgt | nl | sed -e 's/^ \+//g' > $tgt.$d
echo "done"

echo "Scanning ... "
python ~/program/python/scanIdEqual.py $src.$d $tgt.$d
echo "done"

rm $src.$d $tgt.$d
