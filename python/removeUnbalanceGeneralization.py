import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

valid_list = ['$number', '$date', '$day', '$time', '$psn', '$loc']

input_name = sys.argv[1]
output_name = sys.argv[2]

import codecs
input_file = codecs.open(input_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

def init_list():
	result = []
	for ele in valid_list:
		result.append(0)
	return result

index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rProcessing line %d' % index)
		sys.stderr.flush()
	line = line.strip()
	line_sep = line.split('\t')

	source_list = init_list() 
	for word in line_sep[3].split(' '):
		if word in valid_list:
#			print index
			id = valid_list.index(word)
			source_list[id] += 1

	target_list = init_list()
	for word in line_sep[4].split(' '):
		if word in valid_list:
			id = valid_list.index(word)
			target_list[id] += 1
	
	if source_list == target_list:
#		if sum(source_list) > 0:
#		print source_list, target_list
		output_file.write(line + '\n')

for f in file_list:
	f.close()
