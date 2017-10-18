[ $# -eq 0 ] && echo "Usage: sh $0 [input-file]" && exit 1
input_file=$1

sed \
-i \
-e 's/&/\&amp;/g' \
-e 's/"/\&quot;/g' \
-e 's/</\&lt;/g' \
-e 's/>/\&gt;/g' \
$input_file
