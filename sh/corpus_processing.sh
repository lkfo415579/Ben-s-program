#!/bin/bash
[ $# -eq 0 ] && { echo "Usage: $0 [corpus_name] [source_lang] [target_lang]"; exit 1; }

corpus=$1
f=$2
e=$3
test_folder=test
dev_folder=dev
ts=2000
ds=2000

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
cat $test_folder/$corpus.test.$f $dev_folder/$corpus.dev.$f > group.$f
cat $test_folder/$corpus.test.$e $dev_folder/$corpus.dev.$e > group.$e
python ~/program/python/cleanTrainByTestData.py $corpus group $f $e group.id

# clean training set based on the check result
python ~/program/python/removeParallexById.py $corpus.$f $corpus.$e group.id
for i in *.r; do mv $i `echo $i | sed -e 's/\.r$//g'`; done

# create deleted folder store the previous result
mkdir deleted
for i in *.del; do mv $i deleted/`echo $i | sed -e 's/\.del$//g'`; done

rm group.$f group.$e group.id

# show current corpus lines
wc -l $corpus.* $test_folder/* $dev_folder/* deleted/*
