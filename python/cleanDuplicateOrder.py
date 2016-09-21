# -*- encoding: utf-8 -*-
import sys
import os
import time
import codecs

from collections import OrderedDict

if len(sys.argv) != 2:
	print 'This program for cleaning line in single file'
	print 'Output file is named as [input].uni'
	print '$ python', sys.argv[0], "[input]"
	exit()

inputFile = sys.argv[1]
outputFile = inputFile+'.uni'
startTime = time.time()
count = 0

fr = codecs.open(inputFile, 'r', encoding='utf-8')
fw = codecs.open(outputFile, 'w', encoding='utf-8')

# refrom the input and store into set
print 'Loading corpus into memory...'
inputList = []
while True:
	s = fr.readline()
	if not s:
		break
	count += 1
	if count % 10000 == 0:
		sys.stdout.write('%d\r' % count)
		sys.stdout.flush()
		
	inputList.append(s.strip())

print 'Cleaning...'
outputList = list(OrderedDict.fromkeys(inputList))

print 'Exporting result...'
for line in outputList:
	fw.write(line + '\n')

fr.close()
fw.close()

print 'End with', time.time() - startTime, 'seconds.'
