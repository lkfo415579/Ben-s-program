[ $# -eq 0 ] && echo "Usage: ./$0 [output-file] [echo-config]"

output=$1
shift
inputs=$@

echo $output
echo $inputs
perl ~/program/sh/mergeResult/LiNMT-obervation.pl $inputs > $output

