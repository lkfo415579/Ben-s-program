import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[source] [target]'
	print 'This program will output the *.noeq file appended the name of input.'
	exit()

import codecs

source_name = sys.argv[1]
target_name = sys.argv[2]
source_out_name = source_name + '.noeq'
target_out_name = target_name + '.noeq'
delete_line_name = source_name + '_' + target_name + '.noeq.delete.sent'

source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')
source_output_file = codecs.open(source_out_name, 'w', encoding='utf-8')
target_output_file = codecs.open(target_out_name, 'w', encoding='utf-8')
delete_line_file = codecs.open(delete_line_name, 'w', encoding='utf-8')

file_list = [source_file, target_file, source_output_file, target_output_file, delete_line_file]

index = 0
while True:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\r%d' % index)
		sys.stderr.flush()

	source_line = source_file.readline()
	target_line = target_file.readline()

	if not source_file or not target_line:
		break

	if source_line == target_line:
		delete_line_file.write('%s\n' % source_line.strip())
	else:
		source_output_file.write(source_line)
		target_output_file.write(target_line)
	
print 'End of line', index


for f in file_list:
	f.close()
