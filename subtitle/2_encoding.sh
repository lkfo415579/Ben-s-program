cd ../subtitle/
echo 'processing Chinese to UTF-8'
for i in $(ls */chi_*); do python ~/program/python/changeEncoding.py $i $i.out chi; done
echo 'processing Portuguese to UTF-8'
for i in $(ls */por_*); do python ~/program/python/changeEncoding.py $i $i.out por; done

#mkdir -p output
#rm output/*

#echo 'processing lines append (part 1)'
#for i in $(ls */chi_*.out.*); do cp -R $i output/$i\_$(wc -l $i | cut -f1 -d ' '); done
#echo 'processing lines append (part 2)'
#for i in $(ls */por_*.out.*); do cp -R $i output/$i\_$(wc -l $i | cut -f1 -d ' '); done
