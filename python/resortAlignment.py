import sys
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input] [output]'
	exit()

input_name = sys.argv[1]
output_name = sys.argv[2]

input_file = open(input_name, 'r')
output_file = open(output_name, 'w')

file_list = [input_file, output_file]

import collections
index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\r%d' % index)
		sys.stderr.flush()
	d = {}
	line = line.strip()
	for ele in line.split(' '):
		b, a = map(int, ele.split('-'))
		d[a] = d.get(a, []) + [b]
	od = collections.OrderedDict(sorted(d.items()))
	result = []
	for l, v in od.items():
		for e in sorted(v):
			result.append(str(e) + '-' + str(l))
#	print ' '.join(result)
	output_file.write(' '.join(result) + '\n')

for f in file_list:
	f.close()

