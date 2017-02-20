import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input] [output] [lm]'
	exit()

input_name = sys.argv[1]
output_name = sys.argv[2]
lm_name = sys.argv[3]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

import kenlm
model = kenlm.LanguageModel(lm_name)

for line in input_file:
	s =  model.score(line.strip())
	output_file.write(str(s) + '\n')

for f in file_list:
	f.close()
