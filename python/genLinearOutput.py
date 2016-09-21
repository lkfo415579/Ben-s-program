import sys

# help message
if len(sys.argv) != 3:
	print '--Help message--'
	print 'This file will generate 1 output file'
	print '1. output-name.out - parent replaced string: the source sentence with the target parent node'
	print '	Example: a [NP] ||| one [TOP]  -->>  a[TOP]\n'
	print 'You should use the following command to run this program:'
	print '$ python', sys.argv[0], 'input-rule-table output-name\n'
	exit()

# open file
fr = open(sys.argv[1],'r')
fw = open(sys.argv[2] + '.out', 'w') # write source

totalCount = 0
print 'Parsing is started:'
for line in fr: # each line in input file
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount
	
	seplll = line.split(' ||| ')
	sep0 = seplll[0].split(' ')
	sep1 = seplll[1].split(' ')

	# replace parent node
	sep0[-1] = sep1[-1]
	fw.write(' '.join(sep0) + '\n')

print '\nTotal parse: ', totalCount, '	( 100% )'

fr.close()
fw.close()
