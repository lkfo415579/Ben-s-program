import sys
import codecs

if len(sys.argv) != 5:
	print 'Output the line id if that line of corpus length ratio larger than given value.'
	print 'Usage: python', sys.argv[0], '[source] [target] [ratio] [line_id]'
	exit()

source_name = sys.argv[1]
target_name = sys.argv[2]
ratio = float(sys.argv[3])
lineid_name = sys.argv[4]

source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')
lineid_file = codecs.open(lineid_name, 'w', encoding='utf-8')

file_list = [source_file, target_file, lineid_file]

index = 0
while True:
	source_line = source_file.readline().strip()
	target_line = target_file.readline().strip()

	if not source_line or not target_line:
		break
	
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('%d\r' % index)
		sys.stderr.flush()
	
	source_len = float(len(source_line.split(' ')))
	target_len = float(len(target_line.split(' ')))

	if source_len / target_len > ratio or target_len / source_len > ratio:
		lineid_file.write('%d\n' % index)

for f in file_list:
	f.close()
