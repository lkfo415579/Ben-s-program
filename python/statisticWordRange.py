import sys
import os

if len(sys.argv) != 7:
	print 'Using: $ python',sys.argv[0], 'input cn en range_from range_to output'

fr_s = open(sys.argv[1]+'.'+sys.argv[2], 'r')
fr_t = open(sys.argv[1]+'.'+sys.argv[3], 'r')
fw = open(sys.argv[6], 'w')

range_from = int(sys.argv[4])
range_to = int(sys.argv[5])

totalCount = 0
eventCount = 0

while 1:
	s = fr_s.readline()
	t = fr_t.readline()
	if not s or not t:
		break

	totalCount += 1
	s_n = len(s.split(' '))
	t_n = len(t.split(' '))
	if (s_n >= range_from and s_n <= range_to) or (t_n >= range_from and t_n <= range_to):
		fw.write(' ||| '.join([str(totalCount), str(s_n), str(t_n), s.strip(), t]))
		eventCount += 1


print 'Output No.', eventCount, '(', float(eventCount)*100/totalCount, '%', eventCount, '/', totalCount, ')' 

fr_s.close()
fr_t.close()
fw.close()

