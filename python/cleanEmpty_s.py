import sys

if len(sys.argv) != 6:
	print 'Please use the following command to run this program:'
	print '$ python',sys.argv[0],'name s t clean.s clean.t'
	exit()
name = sys.argv[1]
fr_s = open(name+'.'+sys.argv[2], 'r')
fr_t = open(name+'.'+sys.argv[3], 'r')
fw_s = open(name+'.'+sys.argv[4], 'w')
fw_t = open(name+'.'+sys.argv[5], 'w')

totalCount = 0
failCount = 0

while 1:
	s = fr_s.readline()
	t = fr_t.readline()
	if not s or not t:
		break;

	totalCount += 1
	if totalCount % 10000 == 0:
		print totalCount, '\r',

	if len(s.strip()) != 0 and len(t.strip()) != 0:
		fw_s.write(s)
		fw_t.write(t)
	else:
		failCount += 1
		print 'find empty in line:', totalCount

print 'Empty No.', failCount, '(', float(failCount)*100/totalCount, '%', failCount, '/', totalCount, ')' 

fr_s.close()
fr_t.close()
fw_s.close()
fw_t.close()
