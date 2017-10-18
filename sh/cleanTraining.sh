[ $# -eq 0 ] && echo "Usage: sh $0 [source] [target] [outputDir]" && exit 1;

curLoc=$(pwd)
source=$1
target=$2
dir=$3
mkdir -p $dir
mkdir -p $dir/delete

cp $source $target $dir
cd $dir

echo 'Original: '
wc -l $source $target

python ~/program/python/cleanDuplicateOrderParallax.py $source $target
mv $source.uni $source
mv $target.uni $target

echo 'After remove duplicate: '
wc -l $source $target

python ~/program/python/removeParallexEqual.py $source $target
mv $source.noeq $source
mv $target.noeq $target
mv $source\_$target.noeq.delete.sent delete/delete.noeq.sent

echo 'After remove Equal: '
wc -l $source $target

python ~/program/python/cleanAsciiMoreThanXPercent.py $source $source.id 0.7 ascii
python ~/program/python/cleanAsciiMoreThanXPercent.py $target $target.id 0.7 noascii
cat *.id.deleted | sort -n | uniq > delete/delete.asc.id
python ~/program/python/removeParallexById.py $source $target delete/delete.asc.id
mv $source.r $source
mv $target.r $target
rm $source.id* $target.id*
mv *.del delete/

cd $curLoc
