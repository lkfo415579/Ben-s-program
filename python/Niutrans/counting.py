import sys
import codecs
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[input_table] [output_table_count]'
	exit()

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
input_file = codecs.open(input_file_name, 'r', encoding='utf-8')
output_file = codecs.open(output_file_name, 'w', encoding='utf-8')

file_list = [input_file, output_file]

count_source_set = set()
count_source_dict = {}
count_target_set = set()
count_target_dict = {}
count_all_set = set()
count_all_dict = {}

index = 0
for line in input_file:
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rBuilding %d'%index)
		sys.stderr.flush()

	s, t, a = line.split(' ||| ')
	# source count
	if not s in count_source_set:
		count_source_set.add(s)
		count_source_dict[s] = 1
	else:
		count_source_dict[s] += 1
	
	# target count
	if not t in count_target_set:
		count_target_set.add(t)
		count_target_dict[t] = 1
	else:
		count_target_dict[t] += 1

	# all count
	if not line in count_all_set:
		count_all_set.add(line)
		count_all_dict[line] = 1
	else:
		count_all_dict[line] += 1

print '\nDone %d'%index

index = 0
for l in count_all_set:
	v = count_all_dict[l]
	index += 1
	if index % 1000 == 0:
		sys.stderr.write('\rGenerating %d'%index)
		sys.stderr.flush()

	s, t, a = l.split(' ||| ')
	output_file.write(l.strip() + ' ||| ' + ' '.join([str(count_target_dict[t]), str(count_source_dict[s]), str(v)]) + '\n')

print '\nDone %d'%index

for f in file_list:
	f.close()
