# encoding: utf-8
import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input-sent] [valid-chars] [output-id]'
	exit()

import codecs
input_name = sys.argv[1]
char_name = sys.argv[2]
output_name = sys.argv[3]

input_file = codecs.open(input_name, 'r', encoding='utf-8')
char_file = codecs.open(char_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, char_file, output_file]

# load character file
char_set = set()
for line in char_file:
	char_set.add(line.strip())

index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\r%d' % index)
		sys.stderr.flush()
	
	line = line.strip().replace(' ', '')
	isInvalid = False
	for c in line:
		if not c in char_set:
			isInvalid = True
			break
	
	if isInvalid:
		output_file.write(str(index) + '\n')

for f in file_list:
	f.close()

