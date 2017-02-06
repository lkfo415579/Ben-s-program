import sys

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[source-nl] [target-nl]'
	exit()

import codecs
source_name = sys.argv[1]
target_name = sys.argv[2]

source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')

file_list = [source_file, target_file]

index = 0
while True:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('Scanning the line %d ... \r' % index)
		sys.stderr.flush()
	
	source_line = source_file.readline()
	target_line = target_file.readline()

	if not source_line or not target_line:
		print '\nBreak at line', index
		break

	source_id = source_line.split('\t')[0]
	target_id = target_line.split('\t')[0]

	if not source_id == target_id:
		print '\nFound!!'
		print 'Difference at line', index
		break

for f in file_list:
	f.close()
