import sys
import collections

fr = open(sys.argv[1], 'r')

words = {}
lineCount = 0
for line in fr:
	lineCount += 1
	sep = line.split(' ')
	length = len(sep)
	if length in words:
		words[length] = words[length]+ 1
	else:
		words[length] = 1
#	if length > 200:
#		print lineCount ,line

od = collections.OrderedDict(sorted(words.items()))
for k, v in od.iteritems(): print str(k) + ',' + str(v)	

fr.close()
