# this program will generate 1 output file

import sys

# help message
if len(sys.argv) != 3:
	print '--Help message--'
	print 'This program will generate 1 output file'
	print '1. output-name.rst - Rsyntax Tree format file: [TOP [NP I]]\n'
	print 'You should use the following command to run this program:'
	print '$ python', sys.argv[0],'input-moses-tree output-name\n'
	exit()
# open file
fr = open(sys.argv[1],'r')
fw = open(sys.argv[2]+'.rst','w')

totalCount = 0
for line in fr:
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount
	output = line.replace('<tree label="', '[').replace('">', '').replace(' </tree>', ']').replace('&amp;apos;', '\'')
	fw.write(output)

print '\nTotal parse: ', totalCount, '	( 100% )'

fr.close()
fw.close()

