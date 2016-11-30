corpus=train.pat.tok.clean
rootdir=moses
f=zh
e=pt
lm=/home/mb45450/junk
firststep=4
laststep=9
~/mosesdecoder/scripts/training/train-model.perl -root-dir $rootdir -corpus $corpus -f $f -e $e -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:$lm:9 -first-step $firststep -last-step $laststep
