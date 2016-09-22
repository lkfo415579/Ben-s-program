import os
import sys
import codecs

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[source-file] [target-file] [id-file]'
	exit()

source_name = sys.argv[1]
target_name = sys.argv[2]
id_name = sys.argv[3]
source_output_name = source_name+'.r'
target_output_name = target_name+'.r'
source_delete_name = source_name+'.del'
target_delete_name = target_name+'.del'

source_file = codecs.open(source_name, 'r', encoding='utf-8')
target_file = codecs.open(target_name, 'r', encoding='utf-8')
id_file = codecs.open(id_name, 'r', encoding='utf-8')
source_output_file = codecs.open(source_output_name, 'w', encoding='utf-8')
target_output_file = codecs.open(target_output_name, 'w', encoding='utf-8')
source_delete_file = codecs.open(source_delete_name, 'w', encoding='utf-8')
target_delete_file = codecs.open(target_delete_name, 'w', encoding='utf-8')

file_list = [source_file, target_file, id_file, source_output_file, target_output_file, source_delete_file, target_delete_file]

index = 0
id_line = id_file.readline()
while 1:
	source_line = source_file.readline()
	target_line = target_file.readline()

	if not source_line or not target_line:
		break

	index += 1
	if index % 10000 == 0:
		sys.stdout.write('\r' + str(index))
		sys.stdout.flush()

	if not id_line:
		id_line = '0'

	if int(id_line) != index:
		source_output_file.write(source_line)
		target_output_file.write(target_line)
	else:
		source_delete_file.write(source_line)
		target_delete_file.write(target_line)
		id_line = id_file.readline()

print
for f in file_list:
	f.close()


