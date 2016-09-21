import sys
import os
import collections
import codecs

if len(sys.argv) != 2:
	print 'Print the statistic for how many Character in one line.'
	print 'Usage: $ python', sys.argv[0], '[inputFile]'
	exit()

fr = codecs.open(sys.argv[1], 'r', encoding='utf-8')

words = {}

for line in fr:
	length = len(line)
	if length in words:
		words[length] = words[length] + 1
	else:
		words[length] = 1

od = collections.OrderedDict(sorted(words.items()))
for k, v in od.iteritems(): 
	print str(k) + ',' + str(v)

fr.close()
