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

source_skip = 0
target_skip = 0

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

	source_fail = False
	target_fail = False

	try:
		source_id = int(source_line.split('\t')[0])
	except:
		source_id = -1
		source_fail = True

	try:
		target_id = int(target_line.split('\t')[0])
	except:
		target_id = -1
		target_fail = True

	if not source_id + source_skip == target_id + target_skip:
		print '\nFound!! source_id =', source_id, '\ttarget_id =', target_id, '\tDifference at line', index
	
	if source_fail:
		source_skip += 1
	if target_fail:
		target_skip += 1
		

for f in file_list:
	f.close()
