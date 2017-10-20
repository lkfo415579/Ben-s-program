import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input] [encoding] [output]'
	exit(1)

import codecs
input_name = sys.argv[1]
en = sys.argv[2]
output_name = sys.argv[3]

input_file = codecs.open(input_name, 'r', encoding=en)
output_file = codecs.open(output_name, 'w', encoding='UTF-8')

file_list = [input_file, output_file]

index = 0
success = True
try:
	for line in input_file:
		index += 1
		line = line.strip()
		output_file.write(line + '\n')
except:
	sys.stderr.write(input_name + '\tError at line ' + str(index) + '\n')
	success = False

for f in file_list:
	f.close()

from os import remove
if not success:
	remove(output_name)
else:
	remove(input_name)
