import sys
import os

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], 'input-name output-name alignemnt'
	exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
align_file = sys.argv[3]

fr_source = open(input_file, 'r')
fr_align = open(align_file, 'r')
fw_source = open(output_file, 'w')

index = 0
while True:
	line_source = fr_source.readline().strip()
	line_align = fr_align.readline().strip()

	if not line_source or not line_align:
		break

	# separate space
	sep_source = line_source.split(' ')
	sep_align = line_align.split(' ')

	# extract the source alignment index from the alignment file
	# since the alignment is sorted in the target side
	ol = []
	for ele in sep_align:
		if ele.split('-')[0] not in ol:
			ol.append(ele.split('-')[0])

	# insert the missing alignment into list
	max_index = len(sep_source)
	for ele in range(0, max_index):
		if str(ele) not in ol:
			ol.insert(ol.index(str(ele - 1)) + 1 if ele > 0 else 0, str(ele))
	
	# debug print
	index += 1
#	print ' '.join(ol)
#	if index > 48620:
#		print index, max_index, ol	
#		print line_source

	# preorder the source language
	output = []
	for ele in ol:
		output.append(sep_source[int(ele)])

	fw_source.write(' '.join(output) + '\n')

fr_source.close()
fr_align.close()
fw_source.close()
