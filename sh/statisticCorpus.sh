corpus=$1
f=zh
e=pt

python ~/program/python/statistic/countCharacter.py $corpus.$f > statistic.$f
python ~/program/python/statistic/countSpace.py $corpus.$e > statistic.$e
