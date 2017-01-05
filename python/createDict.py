import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input-file] [output_dict]'
	exit()

import codecs
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

input_file = codecs.open(input_file_name, 'r', encoding='utf-8')

file_list = [input_file]

index = 0
dic = {}
for line in input_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rReading %d' % index)
		sys.stderr.flush()

	line = line.strip().split()
	for word in line:
		dic[word] = dic.get(word, 0) + 1

sys.stderr.write('\n%d line readed, %d size of dict is created.\n' % (index, len(dic)))
sys.stderr.write('Reformating ...\n')
'''
index = 0
new_dic = {}
for k, v in dic.items():
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rReformating %d' % index)
		sys.stderr.flush()
	space_word = '<w> ' + ' '.join([c for c in k]) + ' </w>'
	new_dic[space_word] = v
'''
sys.stderr.write('\nExporting ...\n')
import json
with open(output_file_name, 'w') as output_file:
	json.dump(dic, output_file, indent=2)

for f in file_list:
	f.close()
