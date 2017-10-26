for i in $(ls */*.GBK_*); do python ~/program/python/createTimeSeqenceJson.py $i line $i.raw; done
for i in $(ls */*.WINDOWS1252_*); do python ~/program/python/createTimeSeqenceJson.py $i line $i.raw; done

mkdir -p output
rm -rf output/*
#for i in $(ls */*.raw); do mv $i output/$(echo $i | sed -e 's;/;-;g'); done
for i in $(ls -d *); do 
	mkdir -p output/$i;
	mv $i/*.raw output/$i/;
done
