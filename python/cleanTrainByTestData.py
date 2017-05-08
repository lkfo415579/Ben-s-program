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

id = 0
test_set = set()
for s, t in zip(test_s_file, test_t_file):
	id += 1
	if id % 10000 == 0:
		sys.stderr.write('\rReading testing set %d ...' % id)
		sys.stderr.flush()
	test_set.add(s + ' ||||| ' + t)

id = 0
index = 0
while True:
	id += 1
	if id % 10000 == 0:
		sys.stderr.write('\rOutput %d ...' % id)
		sys.stderr.flush()
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
