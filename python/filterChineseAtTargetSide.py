import sys

fr_pt = open(sys.argv[1], 'r')
fw_notFound = open(sys.argv[2], 'w')
fw_found = open(sys.argv[3], 'w')

lineCount = 0
failCount = 0
while 1:
	line = fr_pt.readline()
	if not line:
		break

	lineCount += 1
	target = line.split(' ||| ')[1]
	if len(target) != len(target.decode('utf8')):
		failCount += 1
		fw_found.write(str(lineCount) + '\t' + line)
	else:
		fw_notFound.write(line)

print 'Fail No.', failCount, '(', float(failCount)*100/lineCount, '%', failCount, '/', lineCount, ')'
fr_pt.close()
fw_notFound.close()
fw_found.close()

