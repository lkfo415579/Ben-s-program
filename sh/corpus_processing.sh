

corpus=$1
f=$2
e=$3
test_folder=test
dev_folder=dev
ts=5000
ds=5000

mkdir -p $test_folder
mkdir -p $dev_folder

# extract testing set
python ~/program/python/extractTestSet.py --s $corpus.$f --t $corpus.$e --o tmp --num $ts

for i in *.tmp; do mv $i `echo $i | sed -e 's/\.tmp$//g'`; done
mv test_source $test_folder/$corpus.test.$f
mv test_target $test_folder/$corpus.test.$e

# remove duplicate in testing set
cd $test_folder
python ~/program/python/cleanDuplicateOrderParallax.py $corpus.test.$f $corpus.test.$e
for i in *.uni; do mv $i `echo $i | sed -e 's/\.uni$//g'`; done
cd ..

# extract development set
python ~/program/python/extractTestSet.py --s $corpus.$f --t $corpus.$e --o tmp --num $ds

for i in *.tmp; do mv $i `echo $i | sed -e 's/\.tmp$//g'`; done
mv test_source $dev_folder/$corpus.dev.$f
mv test_target $dev_folder/$corpus.dev.$e

# remove duplicate in development set
cd $dev_folder
python ~/program/python/cleanDuplicateOrderParallax.py $corpus.dev.$f $corpus.dev.$e
for i in *.uni; do mv $i `echo $i | sed -e 's/\.uni$//g'`; done
cd ..

# check training set contain testing set or development set
python ~/program/python/cleanTrainByTestData.py $corpus $test_folder/$corpus.test $f $e test.id
python ~/program/python/cleanTrainByTestData.py $corpus $dev_folder/$corpus.dev $f $e dev.id

# clean training set based on the check result
cat test.id dev.id | sort -n | uniq > group.id
python ~/program/python/removeParallexById.py $corpus.$f $corpus.$e group.id
for i in *.r; do mv $i `echo $i | sed -e 's/\.r$//g'`; done

# create deleted folder store the previous result
mkdir deleted
for i in *.del; do mv $i deleted/`echo $i | sed -e 's/\.del$//g'`; done

rm test.id dev.id group.id

# show current corpus lines
wc -l $corpus.* $test_folder/* $dev_folder/* deleted/*
