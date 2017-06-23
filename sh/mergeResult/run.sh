[ $# -eq 0 ] && echo "Usage: ./$0 [output-file] [echo-config]" && exit 1

output=$1
shift
inputs=$@

echo $output
echo $inputs
perl ~/program/sh/mergeResult/LiNMT-obervation.pl $inputs > $output

