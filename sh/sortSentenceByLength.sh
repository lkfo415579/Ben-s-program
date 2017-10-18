[ $# -eq 0 ] && echo "Usage: sh $0 [input-file] [output-file]" && exit 1;

input=$1
out=$2

cat $input | awk '{ print length, $0 }' | sort -n -s | cut -d" " -f2- > $out
