[ $# -eq 0 ] && echo "Usage: sh $0 [input-file] [output-file]" && exit 1
input_file=$1
output_file=$2

sed \
-e 's/&/\&amp;/g' \
-e 's/"/\&quot;/g' \
-e 's/</\&lt;/g' \
-e 's/>/\&gt;/g' \
$input_file > $output_file
