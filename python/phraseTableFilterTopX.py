import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input] [tmp_folder/] [top-k]'
	exit()

import codecs
input_name = sys.argv[1]
dir_name = sys.argv[2]
if dir_name[-1] != '/':
	dir_name += '/'
output = dir_name + 'phrase-table'
topk = int(sys.argv[3])

import os
os.system('mkdir -p ' + dir_name)

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output, 'w', encoding='utf-8')

file_list = [input_file, output_file]

# read content into dict
index = 0
parse_key = set()
parse_dict = {}
for line in input_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rReading phrase table: %d' % index)
		sys.stderr.flush()

	line = line.strip()
	sep = line.split(' ||| ')

	count_part = sep[4]
	source = sep[0]
	together_count = int(sep[4].split()[2])

	if source in parse_key:
		parse_dict[source].append([together_count, line])
	else:
		parse_dict[source] = [[together_count, line]]
		parse_key.add(source)
		
print '\nReading done at %d' % index

index = 0
# generate files
for key, value in parse_dict.items():
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rGenerating phrases: %d' % index)
		sys.stderr.flush()

	topk_result = sorted(value, key=lambda x: x[0], reverse=True)[:topk]
	for k in topk_result:
		st = k[1].split(' ||| ')
		ts_align = ' '.join(['-'.join([x.split('-')[1], x.split('-')[0]]) for x in st[3].split()])
		for times in range(int(k[0])):
			output_file.write(k[1] + '\n')

print '\nGenerating done at %d' % index

for f in file_list:
	f.close()
