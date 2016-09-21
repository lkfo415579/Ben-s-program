import sys
import os

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], 'input_file output_file skip_every_lines'
	exit()

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
skip_num = int(sys.argv[3])

input_file = open(input_file_name, 'r')
output_file = open(output_file_name, 'w')

index = 0
for line in input_file:
	if index % skip_num == 0:
		output_file.write(line)
	index += 1

input_file.close()
output_file.close()
