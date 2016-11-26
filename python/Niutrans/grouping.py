import sys
if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], '[count_table] [phrase_table] [output_grouped_table]'
	exit()

import codecs
count_name = sys.argv[1]
phrase_name = sys.argv[2]
output_name = sys.argv[3]

count_file = codecs.open(count_name, 'r', encoding='utf-8')
phrase_file = codecs.open(phrase_name, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [count_file, phrase_file, output_file]

index = 0
# read count_table
count_dict = {}
for line in count_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rReading count table: %d' % index)
		sys.stderr.flush()

	sep = line.strip().split(' ||| ')
	key = ' ||| '.join(sep[:2]) # use 'source ||| target' as key
	value = map(int, sep[-1].split()) # count(last column) int list as value
	count_dict[key] = [sum(x) for x in zip(count_dict.get(key, [0, 0, 0]), value)] # element-wise addition

print '\nDone %d' % index

index = 0
# merge count into phrase table
for line in phrase_file:
	index += 1
	if index % 10000 == 0:
		sys.stderr.write('\rReformat table: %d' % index)
		sys.stderr.flush()

	sep = line.strip().split(' ||| ')
	key = ' ||| '.join(sep[:2]) # use 'source ||| target' as key
	prob = sep[2] # probability
	count_string = ' '.join(map(str, count_dict.get(key, [0, 0, 0])))
	output_file.write(' ||| '.join([key, prob, count_string]) + '\n') # add count to last column

print '\nDone %d' % index

for f in file_list:
	f.close()
