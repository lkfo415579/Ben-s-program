import os
import sys

if len(sys.argv) != 3:
	print 'Usage: python2.7', sys.argv[0], 'input_rule_table output_rule_table'
	exit()

inputName_rt = sys.argv[1]
outputName_hasTerminal = sys.argv[2] + '.ter'
outputName_notTerminal = sys.argv[2] + '.nter'

fr_rt = open(inputName_rt, 'r')
fw_hasTer = open(outputName_hasTerminal, 'w')
fw_notTer = open(outputName_notTerminal, 'w')

index = 0
while True:
	line = fr_rt.readline()
	if not line:
		break

	index += 1
	if index % 100 == 0:
		sys.stdout.write('%d\r' % index)
		sys.stdout.flush()

	sep = line.split(' ||| ')
	if len(sep[0].split('[')) > 2:
		fw_hasTer.write(line)
	else:
		fw_notTer.write(line)

fr_rt.close()
fw_hasTer.close()
fw_notTer.close()
