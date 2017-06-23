import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[source] [target]'
	exit()

source_name = sys.argv[1]
target_name = sys.argv[2]
output_source_name = source_name + '.bal'
output_target_name = target_name + '.bal'
output_delete_name = source_name + '.' + target_name + '.del'

import codecs
source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')

output_source_file = codecs.open(output_source_name, 'w', encoding='utf-8')
output_target_file = codecs.open(output_target_name, 'w', encoding='utf-8')
output_delete_file = codecs.open(output_delete_name, 'w', encoding='utf-8')

file_list = [source_file, output_source_file, target_file, output_target_file, output_delete_file]

gen_symbols = ['$number', '$date', '$time']
def countSent(sent):
	result = {}
	for word in sent.split(' '):
		if word in gen_symbols:
			result[word] = result.get(word, 0) + 1
	return result

index = 0
while True:
	source_line = source_file.readline()
	target_line = target_file.readline()

	if not source_line or not target_line:
		sys.stderr.write('\nDone at line %d' % (index))
		sys.stderr.flush()
		break
	
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rParsing line %d' % (index))
		sys.stderr.flush()

	source_line = source_line.strip()
	target_line = target_line.strip()

	source_count = countSent(source_line)
	target_count = countSent(target_line)

	if source_count == target_count:
		output_source_file.write(source_line + '\n')
		output_target_file.write(target_line + '\n')
	else:
		output_delete_file.write(source_line + '\t' + target_line + '\n')

for f in file_list:
	f.close()
