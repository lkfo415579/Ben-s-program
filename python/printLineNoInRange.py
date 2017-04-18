import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[1], '[input_file] [from] [to]'
	exit()

input_name = sys.argv[1]
f = int(sys.argv[2])
t = int(sys.argv[3])

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')

index = 0
for line in input_file:
	index += 1
	if f <= line.count(' ') + 1 <= t:
		print index

input_file.close()
