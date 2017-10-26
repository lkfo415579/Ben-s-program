import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input] [output] [chi/por]'
	exit(1)

import codecs
input_name = sys.argv[1]
output_name = sys.argv[2]
lang = sys.argv[3]

chi_enc = ['UTF-8', 'BIG5', 'GB18030']
por_enc = ['UTF-8', 'WINDOWS-1252', 'ISO-8859-1']

input_file_dict = {}

enc = chi_enc if lang == 'chi' else por_enc 

for e in enc:
	input_file = codecs.open(input_name, 'r', encoding=e)
	input_file_dict[e] = input_file

index = 0
fail_list = []
success = False
for e, input_file in input_file_dict.items():
	try:
		output_file = codecs.open(output_name + '.' + e, 'w', encoding='utf-8')
		for line in input_file:
			index += 1
			line = line.strip()
			output_file.write(line + '\n')
		output_file.close()
		input_file.close()
		success = True
	except UnicodeDecodeError:
		fail_list.append(output_name + '.' + e)

if not success:
	sys.stderr.write('No any output success: ' + input_name + '\n')

from os import remove
for fail in fail_list:
	remove(fail)
