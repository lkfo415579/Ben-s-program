import sys
import codecs

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input_id] [number] [output_file]'
	exit()

input_id_name = sys.argv[1]
number = int(sys.argv[2])
output_file_name = sys.argv[3]

input_file = codecs.open(input_id_name, 'r', encoding='utf-8')
output_file = codecs.open(output_file_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('%d\r' % index)
		sys.stderr.flush()
	line_number = int(line.strip())
	output_file.write('%d\n' % (line_number + number))

for f in file_list:
	f.close()

