# -*- encoding: utf-8 -*-
import sys
import os
import time

if len(sys.argv) != 2:
	print 'This program only design for umcorpus processing'
	print '$ python', sys.argv[0], "input"
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
	t = fr.readline()

	if not s or not t:
		break
	count += 1
	if count % 10000 == 0:
		print count 

	tmp = s.strip() + ' ||||| ' + t.strip()

	inputList.append(tmp)

outputList = list(set(inputList))
#outputList = sorted(set(inputList), key=inputList.index)


for line in outputList:
	fw.write(line.replace(' ||||| ', '\n') + '\n')

#for line in inputList:
#	fw.write(line + '\n')

fr.close()
fw.close()

print 'End with', time.time() - startTime, 'seconds.'
