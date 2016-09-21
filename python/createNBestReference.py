import sys
import os

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[input-ref] [input-nbest] [output-ref]'
	exit()

fr_ref = open(sys.argv[1], 'r')
fr_nbest = open(sys.argv[2], 'r')
fw_ref = open(sys.argv[3], 'w')

# init value
oldIndex = 0
ref_sent = fr_ref.readline().strip()

currentProgram = sys.argv[0]
print currentProgram, ': extracting the n-best reference...'
while True:
	line_nbest = fr_nbest.readline()

	if not ref_sent or not line_nbest:
		break

	sep = line_nbest.split(' ||| ')

	index = int(sep[0])

	# new sentence is found
	if index != oldIndex:
		ref_sent = fr_ref.readline().strip()
		oldIndex = index
	fw_ref.write(ref_sent+'\n')

fr_ref.close()
fr_nbest.close()
fw_ref.close()

print currentProgram, ': end of program'
