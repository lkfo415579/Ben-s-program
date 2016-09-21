# -*- encoding: utf-8 -*-
import sys
import os
import time

from collections import OrderedDict

if len(sys.argv) != 3:
	print 'This program only design for two separated files'
	print 'Input: source, target parallax corpus'
	print 'Output: unique source, target parallax corpus (*.uni file)\n\nUsage:'
	print '$ python', sys.argv[0], "input_source input_target"
	exit()

inputFile_s = sys.argv[1]
inputFile_t = sys.argv[2]
outputFile_s = inputFile_s+'.uni'
outputFile_t = inputFile_t+'.uni'
startTime = time.time()
count = 0

fr_s = open(inputFile_s, 'r')
fr_t = open(inputFile_t, 'r')
fw_s = open(outputFile_s, 'w')
fw_t = open(outputFile_t, 'w')

# refrom the input and store into set
inputList = []
while True:
	s = fr_s.readline()
	t = fr_t.readline()

	if not s or not t:
		break
	count += 1
	if count % 10000 == 0:
		print count 

	tmp = s.strip() + ' ||||| ' + t.strip()

	inputList.append(tmp)

#outputList = sorted(set(inputList), key=inputList.index)

outputList = list(OrderedDict.fromkeys(inputList))

for line in outputList:
	sep = line.split(' ||||| ')
	fw_s.write(sep[0]+'\n')
	fw_t.write(sep[1]+'\n')

#for line in inputList:
#	fw.write(line + '\n')

fr_s.close()
fr_t.close()
fw_s.close()
fw_t.close()

print 'End with', time.time() - startTime, 'seconds.'
