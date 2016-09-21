import sys
import os

if len(sys.argv) != 3:
	print 'Usage: python2.7', sys.argv[0], 'input_rule_table output_rule_table'
	exit()

fr_name = sys.argv[1]
fw_name = sys.argv[2]

fr = open(fr_name, 'r')
fw = open(fw_name, 'w')

index = 0
for line in fr:
	index += 1
	if index % 1000 == 0:
		sys.stdout.write('%d\r' % index)
		sys.stdout.flush()

	sep = line.split(' ||| ')

	source = sep[0].split('[')
	target = sep[1].split('[')
	sep[1] = '['.join([source[0], target[1]])

	pr_list = sep[2].split(' ')
	pr_list[1], pr_list[3] = '1', '1'
	sep[2] = ' '.join(pr_list)

	align = ''
	for i in range(0, len(sep[0].split(' '))-1):
		align = align + str(i) + '-' + str(i) + ' '
	sep[3] = align.strip()

	sep[4] = '1 1 1'


	fw.write(' ||| '.join(sep))

fr.close()
fw.close()
