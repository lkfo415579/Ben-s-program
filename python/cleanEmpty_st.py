import sys

if len(sys.argv) != 10:
	print 'Please use the following command to run this program:'
	print '$ python',sys.argv[0],'name s t moses.s moses.t clean.s clean.t clean.moses.s clean.moses.t'
	exit()
name = sys.argv[1]
fr_s = open(name+'.'+sys.argv[2], 'r')
fr_t = open(name+'.'+sys.argv[3], 'r')
fr_ms = open(name+'.'+sys.argv[4], 'r')
fr_mt = open(name+'.'+sys.argv[5], 'r')
fw_s = open(name+'.'+sys.argv[6], 'w')
fw_t = open(name+'.'+sys.argv[7], 'w')
fw_ms = open(name+'.'+sys.argv[8], 'w')
fw_mt = open(name+'.'+sys.argv[9], 'w')

totalCount = 0
failCount = 0

while 1:
	s = fr_s.readline()
	t = fr_t.readline()
	ms = fr_ms.readline()
	mt = fr_mt.readline()
	if not s or not t or not ms or not mt:
		break;

	totalCount += 1
	if totalCount % 100000 == 0:
		print totalCount, '\r',

	if len(ms.strip()) != 0 and len(mt.strip()) != 0:
		fw_s.write(s)
		fw_t.write(t)
		fw_ms.write(ms)
		fw_mt.write(mt)
	else:
		failCount += 1

print 'Fail No.', failCount, '(', float(failCount)*100/totalCount, '%', failCount, '/', totalCount, ')' 

fr_s.close()
fr_t.close()
fr_ms.close()
fr_mt.close()
fw_s.close()
fw_t.close()
fw_ms.close()
fw_mt.close()
