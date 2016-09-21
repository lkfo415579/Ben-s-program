import sys
import os
import codecs

if len(sys.argv) != 7:
	print 'Output the corpus within length length, together with the index and the length of corpus.'
	print 'Using: python',sys.argv[0], '[input_name] [f] [e] [range_from] [range_to] [output_file]'
	exit()

input_name = sys.argv[1]
f = sys.argv[2]
e = sys.argv[3]
range_from = int(sys.argv[4])
range_to = int(sys.argv[5])
output_name = sys.argv[6]

source_file_name = input_name + '.' + f
target_file_name = input_name + '.' + e

fr_s = codecs.open(source_file_name, 'r', encoding='utf-8')
fr_t = codecs.open(target_file_name, 'r', encoding='utf-8')
fw = codecs.open(output_name, 'w', encoding='utf-8')

file_list = [fr_s, fr_t, fw]

totalCount = 0
eventCount = 0

while 1:
	s = fr_s.readline()
	t = fr_t.readline()
	if not s or not t:
		break

	totalCount += 1
	if totalCount % 10000 == 0:
		sys.stdout.write('%d \r' % totalCount)
		sys.stdout.flush()
	
	s_n = len(s.split(' '))
	t_n = len(t.split(' '))
	if (s_n >= range_from and s_n <= range_to) or (t_n >= range_from and t_n <= range_to):
		fw.write(' ||| '.join([str(totalCount), str(s_n), str(t_n), s.strip(), t]))
		eventCount += 1

print 'Output No.', eventCount, '(', float(eventCount)*100/totalCount, '%', eventCount, '/', totalCount, ')' 

for f in file_list:
	f.close()
