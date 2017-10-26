echo 'processing unzip'
for i in $(ls ../subtitle/*/*.gz); do gzip -d $i; done
