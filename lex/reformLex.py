import sys

if len(sys.argv) != 3:
	print '--Help message--'
	print 'This program will generate 2 files'
	print 'Reform the lexical model from "zh en pr" to "zh zh 1"'
	print 'Input source-to-target_Lexical_model'
	print 'Output: '
	print '1. output-name.e2f - reformed_e2f_Lexical_model: zh zh 1'
	print '2. output-name.f2e - reformed_f2e_Lexical_model: zh zh 1\n'
	print 'You should use the following command to run this program:'
	print '$ python', sys.argv[0], 'input-lexicalModel_e2f output-name\n'
	exit()
# open file
fr_e2f = open(sys.argv[1],'r')
fw_e2f = open(sys.argv[2]+'.e2f','w')
fw_f2e = open(sys.argv[2]+'.f2e','w')

# e2f and f2e processing
totalCount = 0
pr_name = ''
print 'Parsing is started (reform lexical model)'
# input processing
for line in fr_e2f:
	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount

	sep = line.split(' ')
	if pr_name != sep[0]: # source different
		fw_e2f.write(sep[0] + ' ' + sep[0] + ' ' + str(float(1)) + '\n')
		fw_f2e.write(sep[0] + ' ' + sep[0] + ' ' + str(float(1)) + '\n') # write into f2e
	pr_name = sep[0]

print '\nParsing is finished (reform lexical model)'
print '\nTotal parse: ', totalCount, '	( 100% )'

fr_e2f.close()
fw_e2f.close()
fw_f2e.close()
