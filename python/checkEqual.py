import sys
import codecs

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input_fileA] [input_fileB] [output_same]'
	exit()

fileA_name = sys.argv[1]
fileB_name = sys.argv[2]
output_name = sys.argv[3]

fileA_file = codecs.open(fileA_name, 'r', encoding='utf-8')
fileB_file = codecs.open(fileB_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [fileA_file, fileB_file, output_file]

print 'Parsing file: %s' % fileA_name

index = 0
while True:
	index += 1
	lineA = fileA_file.readline()
	lineB = fileB_file.readline()

	if not lineA or not lineB:
		break
	
	if index % 1000 == 0:
		sys.stdout.write('\r %d' % index)
		sys.stdout.flush()

	if lineA == lineB:
		output_file.write('%d\t\t%s' % (index, lineA))

sys.stdout.write('\n')
for f in file_list:
	f.close()
