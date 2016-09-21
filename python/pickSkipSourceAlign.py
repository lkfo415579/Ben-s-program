
import sys

# help message
if len(sys.argv) != 3:
	print '--Help message--'
	print 'This program will generate two output file'
	print '1. output-name.normal - the normal align file: all word from the source side are aligned'
	print '2. output-name.skip - skip align file: some word from the source side is skipped, such as: 0-0 2-1 (1 is skip)\n'
	print 'You should use the following command to run this program:'
	print '$ python', sys.argv[0],'input-rule-table output-name\n'
	exit()
# open file
fr = open(sys.argv[1],'r')
fw_normal = open(sys.argv[2] + '.normal' , 'w')
fw_skip = open (sys.argv[2] + '.skip', 'w')

totalCount = 0
skipCount = 0
print 'Parsing is started:'
for line in fr: # each line in input file
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount
	
	seplll = line.split(' ||| ')
	sep3 = seplll[3].split(' ')
	left = 0 # reset old alignment # left is sorted
	right = 0 # reset old alignment
	skipFlag = False # if it become to true, it is skip
	for align in sep3: # each alignment
		subAlign = align.split('-') 
		if not(skipFlag) and int(subAlign[0]) - left > 1:
			skipFlag = True
			skipCount += 1		

		left = int(subAlign[0]) # source side
		right = int(subAlign[1]) # target side

	if not(skipFlag): # if no skip is found
		fw_normal.write(line)
	else:
		fw_skip.write(line)

normalCount = totalCount - skipCount
print '\nTotal parse: ', totalCount, '	( 100% )'
print 'Normal     : ', normalCount, '	(', float(normalCount)*100/totalCount, '%)'
print 'Skip Align : ', skipCount, '	(', float(skipCount)*100/totalCount, '%)'

fr.close()
fw_normal.close()
fw_skip.close()
