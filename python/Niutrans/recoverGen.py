import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

input_name = sys.argv[1]
output_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

for line in input_file:
	line_sep = line.strip().split(' |||| ')
	if len(line_sep) > 1:
		#print line
		sentence_sep = line_sep[0].split(' ')
		gen_sep = line_sep[1].split('}{')
		gen_sep[0] = gen_sep[0][1:]
		gen_sep[-1] = gen_sep[-1][:-1]
		for ele in gen_sep:
			ele_sep = ele.split(' ||| ')
			sentence_sep[int(ele_sep[0])] = ele_sep[-1]
		output_file.write(' '.join(sentence_sep) + '\n')
	else:
		output_file.write(line_sep[0] + '\n')

for f in file_list:
	f.close()
