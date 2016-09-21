import sys

# help message
if len(sys.argv) != 3:
	print 'this file will generate 2 output files'
	print '1. output-name.linear - linear align file: the alignment is linearly match. such as: 0-0 1-1 2-3 3-4'
	print '2. output-name.nonlinar - nonlinear align file: the alignment is non-linearly match (crossing). such as: 0-1 1-0\n'
	print 'You should use the following command to run this program:'
	print '$ python', sys.argv[0], 'input-rule-table output-result\n'
	exit()
# open file
fr = open(sys.argv[1],'r')
fw_nonLinear = open(sys.argv[2] + '.nonlinear','w') # write nonlinear align rule
fw_linear = open(sys.argv[2] + '.linear', 'w') # write linear align rule

nonLinearAlignCount = 0
linearAlignCount = 0
totalCount = 0
print 'Parsing is started:'
for line in fr: # each line in input file
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount
	
	seplll = line.split(' ||| ')
	sep3 = seplll[3].split(' ')
	# left = 0 # reset old alignment # left is sorted
	right = 0 # reset old alignment
	nonLinearFlag = False # if it become to true, it is nonlinear
	for align in sep3: # each alignment
		subAlign = align.split('-') 
		if right > int(subAlign[1]): # if old align > new align, it is nonlinear
			fw_nonLinear.write(line) # it is nonlinear
			nonLinearFlag = True # mark as found
			nonLinearAlignCount += 1 # count
			break # no need to search next alignment

		#left = int(subAlign[0]) # source side
		right = int(subAlign[1]) # target side

	if not(nonLinearFlag): # if no nonlinear is found
		fw_linear.write(line) # it is linear
		linearAlignCount += 1

print '\nTotal parse: ', totalCount, '	( 100% )'
print 'Linear     : ', linearAlignCount, '	(', float(linearAlignCount)*100/totalCount, '%)'
print 'Non-linear : ', nonLinearAlignCount, '	(', float(nonLinearAlignCount)*100/totalCount, '%)'

fr.close()
fw_nonLinear.close()
fw_linear.close()
