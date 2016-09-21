import sys
import os

if len(sys.argv) != 4:
	print 'Usage: python', sys.argv[0], 'extract-count input-rule-table output-rule-table'
	exit()

extractCount = float(sys.argv[1])
fr = open(sys.argv[2], 'r')
fw = open(sys.argv[3], 'w')

for line in fr:
	seplll = line.split(' ||| ')
	#print seplll
	if float(seplll[4].split(' ')[2]) > extractCount:
		fw.write(line)

fr.close()
fw.close()
