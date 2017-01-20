import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

input_name = sys.argv[1]
output_name = sys.argv[2]

input_file = open(input_name, 'r')
output_file = open(output_name, 'w')

file_list = [input_file, output_file]

for line in input_file:
	line = line.strip()
	if line[0] == '-':
		output_file.write(line[:5] + '\n')
	else:
		output_file.write(line[:4] + '\n')
		

for f in file_list:
	f.close()
