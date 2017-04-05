import sys
import collections
import codecs

if len(sys.argv) != 3:
	print 'Print out the statistic information for how many token in number of lines.'
	print 'Usage: python', sys.argv[0], '[input_file] [none/id/noid]'
	exit()

mode = sys.argv[2]

fr = codecs.open(sys.argv[1], 'r', encoding='utf-8')

words = {}
lineCount = 0
for line in fr:
	lineCount += 1
	if lineCount % 10000 == 0:
		sys.stderr.write('%d\r' % lineCount)
		sys.stderr.flush()

	sep = line.strip().split(' ')
	length = len(sep)
	if length in words:
		words[length] = words[length]+ 1
	else:
		words[length] = 1

od = collections.OrderedDict(sorted(words.items()))
totalLen = 0
totalLine = 0
curLine = 0
for k, v in od.iteritems():
	while curLine+1 < k:
		curLine += 1
		if mode == 'id':
			print str(curLine) + ',' + str(0)
		elif mode == 'noid':
			print str(0)
			
	curLine = k
	totalLine += int(v)
	totalLen += int(v) * int(k)
	if mode == 'id':
		print str(k) + ',' + str(v)	
	elif mode == 'noid':
		print str(v)

print 'totalLen/totalLine:', totalLen, '/', totalLine, '=', float(totalLen)/totalLine

fr.close()
