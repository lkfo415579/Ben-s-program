echo 'Filtering equal files...'
for i in $(ls -d *); do python ../program/removeEqualFiles.py $i; done 

echo 'Created delete folder'
mkdir bak_delete

echo 'Finding chinese invalid documents...'
for i in $(ls */chi_*.out.*); do python ../program/checkValidRatio.py $i ../program/dict/chi.valid.200 >> bak_delete.log ; done

sed -e 's/.* /mv /g' -e 's/$/ bak_delete/g' bak_delete.log > bak_delete.sh
echo 'move files to bak_delete'
sh bak_delete.sh
rm bak_delete.sh


echo 'Finding portuguese invalid documents...'
for i in $(ls */por_*.out.*); do python ../program/checkInvalidRatio.py $i ../program/dict/por.invalid >> bak_delete.log ; done

sed -e 's/.* /mv /g' -e 's/$/ bak_delete/g' bak_delete.log > bak_delete.sh
echo 'move files to bak_delete'
sh bak_delete.sh
rm bak_delete.sh




