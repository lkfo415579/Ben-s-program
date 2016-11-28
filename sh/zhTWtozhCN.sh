if [ $# -eq 0 ]
then
	echo "Usage: $0 [input] [output]"
else
	cat $1 | cconv -f utf-8 -t utf8-cn > $2
fi
