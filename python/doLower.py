import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

import codecs
input_name = sys.argv[1]
output_name = sys.argv[2]

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

index = 0
while True:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rline %d' % index)
		sys.stderr.flush()
	
	line = input_file.readline()
	if not line:
		sys.stderr.write('done line %d' % index)
		break
	line = line.strip()
	output_file.write(line.lower() + '\n')

for f in file_list:
	f.close()
