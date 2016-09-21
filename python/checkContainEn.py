import re
import sys

fr_s = open(sys.argv[1], 'r')
fr_t = open(sys.argv[2], 'r')
fw = open(sys.argv[3], 'w')

linecount = 0
failcount = 0

while 1:
	s = fr_s.readline()
	t = fr_t.readline()
	if not s or not t:
		break
	if len(s) == len(s.decode('utf8')):
   		fw.write(' ||| '.join([str(linecount), s.strip(), t]))
		failcount += 1

	linecount += 1

print 'Fail No.', failcount, '(', float(failcount)*100/linecount, '%', failcount, '/', linecount, ')' 

fr_s.close()
fr_t.close()
fw.close()
