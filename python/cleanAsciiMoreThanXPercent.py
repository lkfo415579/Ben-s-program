import sys
if len(sys.argv) != 5:
	print 'Clena the single file by the ascii/noascii percentage.'
	print 'If the input file is Chinese, use clean ascii mode, otherwise is noascii mode.'
	print 'Usage: python', sys.argv[0], '[input] [output] [percent] [ascii/noascii]'
	exit()

import codecs
input_name = sys.argv[1]
output_name = sys.argv[2]
delete_name = output_name + '.deleted'
percent = float(sys.argv[3])
mode = sys.argv[4]
id_flag = '.id' == output_name[-3:]

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')
delete_file = codecs.open(delete_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

index = 0
for line in input_file:
	line = line.strip()
	output = line
	line.replace(' ', '')
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\r%d' % index)
		sys.stderr.flush()
	
	if mode == 'ascii':
		result = sum([1 if not (48 <= ord(w) <= 57) and  ord(w) < 256 else 0 for w in line])
	elif mode == 'noascii':
		result = sum([1 if 48 <= ord(w) <=57 or ord(w) > 256 else 0 for w in line])

	if id_flag:
		output = str(index)

	if len(line) > 0 and (float(result) / len(line)) < percent:
		output_file.write(output + '\n')
	else:
		delete_file.write(output + '\n')
	
print 'End at line %d' % index

for f in file_list:
	f.close()
	
	
