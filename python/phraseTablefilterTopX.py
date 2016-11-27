import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input] [tmp_folder/] [top-k]'
	exit()

import codecs
input_name = sys.argv[1]
dir_name = sys.argv[2]
if dir_name[-1] != '/':
	dir_name += '/'
output_st = dir_name + 'extract.sorted'
output_ts = dir_name + 'extract.inv.sorted'
topk = int(sys.argv[3])

import os
os.system('mkdir -p ' + dir_name)

input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_st_file = codecs.open(output_st, 'w', encoding='utf-8')
output_ts_file = codecs.open(output_ts, 'w', encoding='utf-8')

file_list = [input_file, output_st_file, output_ts_file]

# read content into dict
parse_key = set()
parse_dict = {}
for line in input_file:
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
		
# generate files
for key, value in parse_dict.items():
	topk_result = sorted(value, key=lambda x: x[0], reverse=True)[:topk]
	for k in topk_result:
		st = k[1].split(' ||| ')
		ts_align = ' '.join(['-'.join([x.split('-')[1], x.split('-')[0]]) for x in st[3].split()])
		for times in range(int(k[0])):
			output_st_file.write(' ||| '.join([st[0], st[1], st[3]]) + '\n')
			output_ts_file.write(' ||| '.join([st[1], st[0], ts_align]) + '\n')

for f in file_list:
	f.close()
