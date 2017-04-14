import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input-align] [input-source-gen] [output]'
	exit()

in_align_name = sys.argv[1]
in_gen_name = sys.argv[2]
out_name = sys.argv[3]

valid_list = ['$number', '$date', '$day', '$time']

import codecs
in_align_file = codecs.open(in_align_name, 'r', encoding='utf-8')
in_gen_file = codecs.open(in_gen_name, 'r', encoding='utf-8')
out_file = codecs.open(out_name, 'w', encoding='utf-8')

file_list = [in_align_file, in_gen_file, out_file]

def oprint(string):
	out_file.write(string)

import math

source_id = 0
target_id = 0
source = ''
target = ''
length = ''
source_len = 0
target_len = 0
gen_line = ''
attention = []
for line in in_align_file:
	line = line.strip()
	line_sep = line.split(' ||| ')
	if len(line_sep) > 1: # sentence
		source_id, source, target_id, target, length = line_sep
		source_len, target_len = map(int, length.split(' '))
		gen_line = in_gen_file.readline().strip()
		continue

	if len(line) > 0: # attention
		sep_attention = map(float, line.split(' '))
		attention.append(sep_attention)

	else: # empty line
#		print source
#		print target
#		print gen_line
#		print attention
		gen_sep = gen_line.split(' |||| ')
		output_string = ''
		if len(gen_sep) > 1:
			gen_part_sep = gen_sep[1][1:-1].split('}{')
			result = []
			index = 0
			for ele in source.split(' '):
#				print 'index =', index
				if ele in valid_list:
					# match the max attention
					target_index = 0
					max_index = -1
					v = -1
					for g in gen_part_sep:
#						print 'i =', target_index
						g_sep = g.split(' ||| ') 
						if g_sep[3] == ele:
							if attention[index][int(g_sep[0])] > v:
								max_index = target_index
								v = attention[index][int(g_sep[0])]
						target_index += 1
					# end of match, i is index, v in attention wegiht

#					print target_index, v, max_index
#					print gen_part_sep 
					if max_index > -1:
						#result.append('_' + gen_part_sep[max_index].split(' ||| ')[2] + '_')
						result.append(gen_part_sep[max_index].split(' ||| ')[2])
						del gen_part_sep[max_index]
				else:
					result.append(ele)
				index += 1
			output_string = ' '.join(result)
		else: 
			output_string = source	
		oprint(output_string + '\n')
		attention = []

for f in file_list:
	f.close()
