import sys

# help message
if len(sys.argv) != 2:
	print 'This file will generate 1 output files'
	print '1. output-name.count - the orignal align file with the crossing count'
	print 'You should use the following command to run this program:'
	print '$ python', sys.argv[0], '[input_align_file]\n'
	exit()
# open file
fr = open(sys.argv[1],'r')
fw = open(sys.argv[1] + '.count','w') # write nonlinear align rule

alignCount = 0
crossCount = 0
totalCount = 0
print 'Parsing is started:'
for line in fr: # each line in input file
	totalCount += 1
	if totalCount % 10000 == 0:
		sys.stdout.write("%d\r" % totalCount)
		sys.stdout.flush()

	if len(line) < 2 :
		continue	

	sep3 = line.split(' ')
	
	pos = 0 # reset old alignment
	alignCount += len(sep3)
	for align in sep3: # each alignment
		subAlign = align.split('-') 
		if pos > int(subAlign[0]): # if old align > new align, it is nonlinear
			fw.write(line) # it is nonlinear
			crossCount += 1 # count

		pos = int(subAlign[0]) # target side

print '\nTotal lines: ', totalCount, '	( 100% )'
print 'Total alignment: ', alignCount, '	( 100% )'
print 'Total cross: ', crossCount, '	(', float(crossCount)*100/alignCount, '% )'

fr.close()
fw.close()
