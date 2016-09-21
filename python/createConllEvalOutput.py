import sys
import os

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], 'gold_file test_file output_file'
	exit()

sep_symbol = '\t'

gold_name = sys.argv[1]
test_name = sys.argv[2]
output_name = sys.argv[3]

gold_file = open(gold_name, 'r')
test_file = open(test_name, 'r')
output_file = open(output_name, 'w')

file_list = [gold_file, test_file, output_file]

index = 0
for gold, test in zip(gold_file, test_file):
	index += 1
	if index % 10000 == 0:
		sys.stdout.write('line: %d\r' % index)
		sys.stdout.flush()
	
	gold = gold.strip()
	test = test.strip()

	if len(test) > 0:
		sep_gold = gold.split(sep_symbol)
		sep_test = test.split(sep_symbol)

		if sep_gold[0] != sep_test[0]:
			print 'Two word is not equals at line %d, program stop!' % index
			break
	
		output_file.write('%s %s %s %s\n' %(sep_gold[0], sep_gold[1], sep_gold[-1], sep_test[-1]))
	else:
		output_file.write('\n')


for f in file_list:
	f.close()
