import sys
import collections
import codecs

fr = codecs.open(sys.argv[1], 'r', encoding='utf-8')

words = {}
lineCount = 0
for line in fr:
	lineCount += 1
	if lineCount % 10000 == 0:
		sys.stdout.write('%d\r' % lineCount)
		sys.stdout.flush()

	sep = line.split(' ')
	length = len(sep)
	if length in words:
		words[length] = words[length]+ 1
	else:
		words[length] = 1

od = collections.OrderedDict(sorted(words.items()))
for k, v in od.iteritems(): 
	print str(k) + ',' + str(v)	

fr.close()
