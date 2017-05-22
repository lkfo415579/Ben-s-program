import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[words.json] [input] [output]'
	exit()

word_name = sys.argv[1]
input_name = sys.argv[2]
output_name = sys.argv[3]

import json
from pprint import pprint

data = {}
with open(word_name) as data_file:    
    data = json.load(data_file)

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')
file_list = [input_file, output_file]
	#pprint(data)

while True:
	line = input_file.readline()
	if not line:
		break
	line = line.strip()
	result = [x if data.get(x, 1) > 1 else 'UNK' for x in line.split(' ')]
	output_file.write(' '.join(result) + '\n')

for f in file_list:
	f.close()
