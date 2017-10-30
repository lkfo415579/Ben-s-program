import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [valid_set]'
	exit()

input_name = sys.argv[1]
valid_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
valid_file = codecs.open(valid_name, 'r', encoding='utf-8')

valid_set = set()
for line in valid_file:
	valid_set.add(line.strip())

input_set = set()
for line in input_file:
	line = line.strip()
	for c in line:
		input_set.add(c)
score = float(len(valid_set & input_set))/len(valid_set)
if score < 0.5:
	print score, input_name
	
input_file.close()
valid_file.close()
