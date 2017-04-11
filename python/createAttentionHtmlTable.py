import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input-align] [output-table]'
	exit()

input_name = sys.argv[1]
output_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

def oprint(string):
	output_file.write(string)

import math

index = 0 # counting source id
source_id = 0
target_id = 0
source = ''
target = ''
length = ''
source_len = 0
target_len = 0
oprint('<html> <head> <style> table,tr,td{border: none;} td{width:20px} </style> </head> <body>\n')
for line in input_file:
	line = line.strip()
	line_sep = line.split(' ||| ')
	if len(line_sep) > 1: # sentence
		source_id, source, target_id, target, length = line_sep
		source = source + ' eos'
		target = target + ' eos'
		source_len, target_len = map(int, length.split(' '))
		oprint('<table>\n<tr><td>'+source_id+'-'+target_id+'</td>')
		for word in target.split(' '):
			oprint('<td>' + word + '</td>\n')
		oprint('</tr>\n')
		continue

	if len(line) > 0: # attention
		sep_attention = map(float, line.split(' '))
		oprint('<tr><td>' + source.split(' ')[index] + '</td>\n')
		for attention in sep_attention:
			color = str(int(255-math.floor(attention * 255)))
			oprint('<td style="background:rgb('+color+','+color+','+color+')"></td>\n')
			#oprint('<td style="background-color:'+color+'">&nbsp;</td>\n')

		oprint('</tr>')
		index += 1
	else: # empty line
		index = 0
		oprint('</table>\n')

oprint('</body> </html>\n')


for f in file_list:
	f.close()
