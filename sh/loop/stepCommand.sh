[ $# -eq 0 ] && echo "sh $0 [from] [to] [step] [command]" && exit 1

from=$1
to=$2
step=$3

shift 3
for i in $(seq $from $step $to); do
	eval $@;
done
