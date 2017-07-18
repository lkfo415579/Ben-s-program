import re
import sys

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], '[source] [output_id]'
	exit()

fr_s = open(sys.argv[1], 'r')
fw = open(sys.argv[2], 'w')

linecount = 0
failcount = 0
while 1:
	s = fr_s.readline()
	if not s:
		break
	if len(s) != len(s.decode('utf8')):
#   		fw.write(' ||| '.join([str(linecount), s.strip(), t]))
		fw.write(str(linecount) + ' ' + s)
		failcount += 1

	linecount += 1

print 'Fail No.', failcount, '(', float(failcount)*100/linecount, '%', failcount, '/', linecount, ')'

fr_s.close()
fw.close() 
