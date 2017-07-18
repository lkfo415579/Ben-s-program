# -*- encoding: utf-8 -*-
import sys
if len(sys.argv) != 3:
	print ('Usage python {} [input] [output]'.format(sys.argv[0]))
	exit()

import codecs
import t_date 
import t_time
import t_number

dateTranslator = t_date.DateTranslator()
timeTranslator = t_time.TimeTranslator()
numberTranslator = t_number.NumberTranslator()

def do_translate(line):
	if line.count(' |||| ') == 0: # no generalize part
		return line
	else:
		sent, gen = line.split(' |||| ')
		gen_sep = gen.split('}{')
		gen_sep[0] = gen_sep[0][1:]
		gen_sep[-1] = gen_sep[-1][:-1]

		# translate each gen element
		result = []
		for ele in gen_sep:
			ele_sep = ele.split(' ||| ')
			gen_symbol = ele_sep[3]
			if gen_symbol == '$date':
				gen_trans = dateTranslator.doTranslate(ele_sep)
				result.append(' ||| '.join(gen_trans))
			#if gen_symbol == '$number':
			#	print line
			#	gen_trans = numberTranslator.doTranslate(ele_sep)
			#	result.append(' ||| '.join(gen_trans))
			#elif gen_symbol == '$time':
			#	gen_trans = timeTranslator.doTranslate(ele_sep)
			#	result.append(' ||| '.join(gen_trans))
			else:
				result.append(' ||| '.join(ele_sep))

		tmp = '}{'.join(result)
		return sent + ' |||| {' + tmp + '}'

def process_lines():
	# input from files
	input_name = sys.argv[1]
	output_name = sys.argv[2]
	
	input_file = codecs.open(input_name, 'r', encoding='utf-8')
	output_file = codecs.open(output_name, 'w', encoding='utf-8')
	
	file_list = [input_file, output_file]

	# main process
	for line in input_file:
		line = line.strip()
		line_trans = do_translate(line) # do translate
		output_file.write(line_trans + '\n')

	for f in file_list:
		f.close()

if __name__ == '__main__':
	process_lines()
