import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [invalid_set]'
	exit()

input_name = sys.argv[1]
invalid_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
invalid_file = codecs.open(invalid_name, 'r', encoding='utf-8')

invalid_set = set()
for line in invalid_file:
	invalid_set.add(line.strip())

input_set = set()
for line in input_file:
	line = line.strip()
	for c in line:
		input_set.add(c)
score = float(len(invalid_set & input_set))/len(invalid_set)
if score > 0.1:
	print score, input_name
	
input_file.close()
invalid_file.close()
