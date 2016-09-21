# encoding=utf-8
import sys
if len(sys.argv) != 6:
	print 'Usage: python', sys.argv[0], '[train_name] [test_name] [f] [e] [output_id]'
	exit()

import os
import codecs

train_name = sys.argv[1]
test_name = sys.argv[2]
lang_s = sys.argv[3]
lang_t = sys.argv[4]
output_name = sys.argv[5]

train_s_file = codecs.open(train_name + '.' + lang_s, 'r', encoding='utf-8')
train_t_file = codecs.open(train_name + '.' + lang_t, 'r', encoding='utf-8')
test_s_file = codecs.open(test_name + '.' + lang_s, 'r', encoding='utf-8')
test_t_file = codecs.open(test_name + '.' + lang_t, 'r', encoding='utf-8')
output_file = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [train_s_file, train_t_file, test_s_file, test_t_file, output_file]

test_set = set()
for s, t in zip(test_s_file, test_t_file):
	test_set.add(s + ' ||||| ' + t)

index = 0
while True:
	s = train_s_file.readline()
	t = train_t_file.readline()
	if not s or not t:
		print 'Searching end at line %d' % index
		break

	index += 1
	if index % 10000 == 0:
		sys.stdout.write('%d\r' % index)
		sys.stdout.flush()
	if (s + ' ||||| ' + t) in test_set:
		output_file.write('%d\n' % index)

for f in file_list:
	f.close()
