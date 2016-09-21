import sys
import os
import codecs
import re

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[force_decoding_file] [source_file] [output_file]'
	exit()

force_name = sys.argv[1]
source_name = sys.argv[2]
output_name = sys.argv[3]

force_file = codecs.open(force_name, 'r', encoding='utf-8')
source_file = codecs.open(source_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [force_file, source_file, output_file]

index = 0
for force_line, source_line in zip(force_file, source_file):
	index += 1
	if index % 1000 == 0:
		sys.stdout.write(str(index)+'\r')
		sys.stdout.flush()

	force_line = force_line.strip()
#	print force_line, '\t', source_line.strip()

	if len(force_line) > 0:
		sep_source_line = source_line.strip().split(' ')
		group_range_list = re.findall('[^|]+\|\d+-\d+\|', force_line)
#		print group_range_list
		for ele in group_range_list:
			sep_ele = ele.strip().split('|')
			s_sent, s_range = sep_ele[0], sep_ele[1]
			s_range_from = int(s_range.split('-')[0])
			s_range_to = int(s_range.split('-')[1])+1
			s_source = ' '.join(sep_source_line[s_range_from:s_range_to])
			output_file.write(s_source + '\t|||\t' + s_sent + '\n')
	else:
		continue


for f in file_list:
	f.close()
