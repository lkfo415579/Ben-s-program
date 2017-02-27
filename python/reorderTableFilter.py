import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[phrase-table] [extract.o.sorted]'
	exit()

import codecs

pt_input_name = sys.argv[1]
ex_input_name = sys.argv[2]
ex_output_name = ex_input_name + '.new'

pt_input_file = codecs.open(pt_input_name, 'r', encoding='utf-8')
ex_input_file = codecs.open(ex_input_name, 'r', encoding='utf-8')
ex_output_file = codecs.open(ex_output_name, 'w', encoding='utf-8')

file_list = [pt_input_file, ex_input_file, ex_output_file]

pt_set = set()

index = 0
for line in pt_input_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rGenerating %d ...' % index)
		sys.stderr.flush()
	pt_set.add(' ||| '.join(line.split(' ||| ')[:2]))

index = 0
for line in ex_input_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rGenerating %d ...' % index)
		sys.stderr.flush()
	if ' ||| '.join(line.split(' ||| ')[:2]) in pt_set:
		ex_output_file.write(line)

for f in file_list:
	f.close()
