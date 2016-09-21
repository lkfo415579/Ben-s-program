# -*- encoding: utf-8 -*-
import sys
import os
import time

from collections import OrderedDict

if len(sys.argv) != 2:
	print 'This program will output the file names [input].uni'
	print '$ python', sys.argv[0], "[input]"
	exit()

inputFile = sys.argv[1]
outputFile = inputFile+'.uni'
startTime = time.time()
count = 0

fr = open(inputFile, 'r')
fw = open(outputFile, 'w')

# refrom the input and store into set
inputList = []
while True:
	s = fr.readline()

	if not s:
		break
	count += 1
	if count % 10000 == 0:
		print count 

	tmp = s.strip()

	inputList.append(tmp)

#outputList = sorted(set(inputList), key=inputList.index)

outputList = list(OrderedDict.fromkeys(inputList))

for line in outputList:
	fw.write(line + '\n')

#for line in inputList:
#	fw.write(line + '\n')

fr.close()
fw.close()

print 'End with', time.time() - startTime, 'seconds.'
