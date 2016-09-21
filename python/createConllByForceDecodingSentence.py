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

def groupByRange(group_list, source_line):
	try:
		output = source_line.split(' ')
		for ele in group_list:
			sep_ele = ele.split('-')
			start, end = int(sep_ele[0]), int(sep_ele[1])
			if start == end:
				output[start] = 'O'
				continue
			for i in range(start, end + 1):
				if i == start:
					output[i] = 'B'
				else:
					output[i] = 'I'
	except:
		print ' '.join(group_list), source_line
	return output

def createConll(result_BIO, source_line):
	output = []
	source_list = source_line.split(' ')
	for word, label in zip(source_list, result_BIO):
		output.append(word + '\t' + label)
	return output

for force_line, source_line in zip(force_file, source_file):

	force_line = force_line.strip()
#	print force_line

	if len(force_line) > 0:
		source_line = source_line.strip()
		group_range_list = re.findall('\|([0-9]+-[0-9]+)\|', force_line)
		result_BIO = groupByRange(group_range_list, source_line)
		result = createConll(result_BIO, source_line)
		output_file.write('\n'.join(result) + '\n\n')
	else:
		continue


for f in file_list:
	f.close()
